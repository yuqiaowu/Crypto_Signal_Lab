from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import time
from typing import Any, Dict, Iterable, List, Optional

import ccxt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
# Configure fonts to support CJK glyphs when available
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
import os


def build_exchange(proxy_url: Optional[str] = None) -> ccxt.okx:
    """
    Create an OKX exchange instance configured with an optional HTTP proxy.
    Clash 默认监听 127.0.0.1:7890，可以通过 proxy_url 覆盖。
    """
    settings: Dict[str, object] = {
        "enableRateLimit": True,
    }
    # 自动识别代理：优先使用传入的 proxy_url；否则读取环境变量
    if not proxy_url:
        env_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
        if env_proxy:
            proxy_url = env_proxy.strip()
        else:
            use_local = os.environ.get("USE_LOCAL_PROXY", "0").lower() in {"1", "true", "yes"}
            if use_local:
                proxy_url = "http://127.0.0.1:7890"
    if proxy_url:
        settings["proxies"] = {
            "http": proxy_url,
            "https": proxy_url,
        }
    return ccxt.okx(settings)


def fetch_daily_ohlcv(
    exchange: ccxt.okx,
    symbol: str = "ETH/USDT",
    days: int = 730,
) -> pd.DataFrame:
    """
    分批拉取最近指定天数的 OKX 日线数据。
    OKX 单次请求有数量限制，这里循环分页，覆盖约两年历史。
    返回列包括 open/high/low/close/volume，索引为北京时区的日期。
    """
    timeframe = "1d"
    limit = 200  # OKX 对日线最多返回 200 根
    timeframe_ms = exchange.parse_timeframe(timeframe) * 1000
    since_dt = datetime.now(timezone.utc) - timedelta(days=days)
    since = int(since_dt.timestamp() * 1000)

    all_ohlcv: list[list[float]] = []
    while True:
        batch = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        if not batch:
            break

        all_ohlcv.extend(batch)
        last_ts = batch[-1][0]
        next_since = last_ts + timeframe_ms
        if len(batch) < limit or next_since <= since:
            break
        since = next_since

        # 避免过度请求服务器
        time.sleep(exchange.rateLimit / 1000)

    if not all_ohlcv:
        raise RuntimeError("无法获取 OKX 日线数据，请检查网络或代理设置。")

    raw_ohlcv = all_ohlcv
    df = pd.DataFrame(
        raw_ohlcv,
        columns=["timestamp", "open", "high", "low", "close", "volume"],
    )

    df = df.drop_duplicates(subset="timestamp")
    df["datetime"] = (
        pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        .dt.tz_convert("Asia/Shanghai")
    )
    df = df.set_index("datetime").drop(columns=["timestamp"])
    df = df.sort_index()
    return df


def add_bollinger_bands(
    df: pd.DataFrame,
    window: int = 20,
    num_std: float = 2.0,
) -> pd.DataFrame:
    """
    计算布林带、下轨斜率百分比及其 5 日均值，并添加到 DataFrame。
    """
    rolling_mean = df["close"].rolling(window=window, min_periods=window).mean()
    rolling_std = df["close"].rolling(window=window, min_periods=window).std(ddof=0)

    df["bb_mid"] = rolling_mean
    df["bb_upper"] = rolling_mean + num_std * rolling_std
    df["bb_lower"] = rolling_mean - num_std * rolling_std
    df["bb_lower_slope"] = df["bb_lower"].pct_change() * 100
    df["bb_lower_slope_ma_5"] = df["bb_lower_slope"].rolling(window=5, min_periods=5).mean()
    return df


def compute_rsi(series: pd.Series, period: int) -> pd.Series:
    """
    采用 Wilder 平滑方法计算 RSI。
    """
    delta = series.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)

    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def add_rsi_indicators(df: pd.DataFrame, periods: Iterable[int]) -> pd.DataFrame:
    """
    为 DataFrame 添加多个 RSI 列。
    """
    for period in periods:
        df[f"rsi_{period}"] = compute_rsi(df["close"], period)
    return df


def add_macd_indicators(
    df: pd.DataFrame,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> pd.DataFrame:
    """
    计算 MACD 线、Signal 线、柱状图以及不同位置的金叉/死叉信号。
    """
    ema_fast = df["close"].ewm(span=fast_period, adjust=False).mean()
    ema_slow = df["close"].ewm(span=slow_period, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    hist = macd_line - signal_line

    df["macd_line"] = macd_line
    df["macd_signal"] = signal_line
    df["macd_hist"] = hist

    window = 180
    q90 = signal_line.rolling(window=window, min_periods=window).quantile(0.95)
    q10 = signal_line.rolling(window=window, min_periods=window).quantile(0.05)
    df["macd_signal_q90_180"] = q90
    df["macd_signal_q10_180"] = q10
    df["macd_signal_top_180"] = (signal_line > q90) & q90.notna()
    df["macd_signal_bottom_180"] = (signal_line < q10) & q10.notna()

    return df


def add_price_moving_averages(df: pd.DataFrame, windows: Iterable[int]) -> pd.DataFrame:
    """
    根据收盘价计算多条移动平均线。
    """
    for window in windows:
        df[f"ma_{window}"] = df["close"].rolling(window=window, min_periods=window).mean()
    return df


def add_dmi_indicators(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    计算 Directional Movement (DMI) 指标：+DI、-DI、ADX。
    """
    high = df["high"]
    low = df["low"]
    close = df["close"]

    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    tr_components = pd.concat(
        [
            high - low,
            (high - close.shift(1)).abs(),
            (low - close.shift(1)).abs(),
        ],
        axis=1,
    )
    tr = tr_components.max(axis=1)

    tr_series = pd.Series(tr, index=df.index)
    atr = tr_series.ewm(alpha=1 / period, adjust=False).mean()

    plus_smoothed = pd.Series(plus_dm, index=df.index).ewm(alpha=1 / period, adjust=False).mean()
    minus_smoothed = pd.Series(minus_dm, index=df.index).ewm(alpha=1 / period, adjust=False).mean()
    atr_safe = atr.replace(0, np.nan)
    plus_di = 100 * plus_smoothed / atr_safe
    minus_di = 100 * minus_smoothed / atr_safe

    dm_sum = (plus_di + minus_di).replace(0, np.nan)
    dx = 100 * (plus_di - minus_di).abs() / dm_sum
    adx = dx.ewm(alpha=1 / period, adjust=False).mean()

    plus_di.iloc[:period] = np.nan
    minus_di.iloc[:period] = np.nan
    adx.iloc[: period * 2] = np.nan

    df["+di"] = plus_di
    df["-di"] = minus_di
    df["adx"] = adx
    return df


def add_atr_indicator(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    计算 ATR 及 ATR%（ATR / close * 100）。
    使用 Wilder 平滑，与 add_dmi_indicators 中的 ATR 一致。
    """
    high = df["high"]
    low = df["low"]
    close = df["close"]
    prev_close = close.shift(1)

    tr_components = pd.concat(
        [
            (high - low).abs(),
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    )
    tr = tr_components.max(axis=1)
    atr = tr.ewm(alpha=1 / period, adjust=False).mean()

    df[f"atr_{period}"] = atr
    df[f"atr_pct_{period}"] = (atr / close.replace(0, np.nan)) * 100
    return df


def add_volume_indicators(df: pd.DataFrame, ma_window: int = 20) -> pd.DataFrame:
    """
    计算成交量的移动均值，以及上一日和当日成交量对均值的占比。
    """
    ma_col = f"volume_ma_{ma_window}"
    df[ma_col] = df["volume"].rolling(window=ma_window, min_periods=ma_window).mean()
    df[f"prev_volume_ratio_ma_{ma_window}"] = df["volume"].shift(1) / df[ma_col]
    df[f"volume_ratio_ma_{ma_window}"] = df["volume"] / df[ma_col]
    return df


def add_price_percentile(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    计算收盘价在近 window 天内的百分位。
    """
    close = df["close"]
    percentile = (
        close.rolling(window=window, min_periods=window).apply(
            lambda x: pd.Series(x).rank(pct=True).iloc[-1],
            raw=False,
        )
    )
    df[f"price_percentile_{window}"] = percentile
    return df


def compute_signal_info(df: pd.DataFrame) -> Dict[str, Any]:
    price_percentile = df.get("price_percentile_20")
    volume_ratio = df.get("volume_ratio_ma_20")

    low_high_mask = ((price_percentile < 0.10) & (volume_ratio > 2.0)).fillna(False)
    high_high_mask = ((price_percentile > 0.90) & (volume_ratio > 2.0)).fillna(False)

    if "rsi_14" in df:
        rsi_overbought = (df["rsi_14"] > 70).fillna(False)
        rsi_oversold = (df["rsi_14"] < 30).fillna(False)
    else:
        rsi_overbought = pd.Series(False, index=df.index, dtype=bool)
        rsi_oversold = pd.Series(False, index=df.index, dtype=bool)

    adx = df.get("adx")
    plus_di = df.get("+di")
    minus_di = df.get("-di")
    if adx is None:
        adx = pd.Series(False, index=df.index)
    if plus_di is None:
        plus_di = pd.Series(False, index=df.index)
    if minus_di is None:
        minus_di = pd.Series(False, index=df.index)

    adx_threshold = 40
    adx_up = ((plus_di > minus_di) & (adx > adx_threshold)).fillna(False)
    adx_down = ((minus_di > plus_di) & (adx > adx_threshold)).fillna(False)

    buy_count = rsi_oversold.astype(int) + low_high_mask.astype(int) + adx_down.astype(int)
    sell_count = rsi_overbought.astype(int) + high_high_mask.astype(int) + adx_up.astype(int)

    ma_status: Dict[int, Dict[str, pd.Series]] = {}
    for window in [5, 10, 20, 60, 120, 180, 200, 250, 360]:
        col = f"ma_{window}"
        if col not in df:
            continue
        ma_series = df[col]
        above = (df["close"] > ma_series).fillna(False).astype(bool)
        below = (df["close"] < ma_series).fillna(False).astype(bool)
        stood_above = (above & above.shift(1) & above.shift(2)).fillna(False).astype(bool)
        stood_above &= ~above.shift(3).fillna(False).astype(bool)
        fell_below = (below & below.shift(1) & below.shift(2)).fillna(False).astype(bool)
        fell_below &= ~below.shift(3).fillna(False).astype(bool)
        ma_status[window] = {
            "above": above,
            "below": below,
            "stood_above_3": stood_above,
            "fell_below_3": fell_below,
        }

    return {
        "price_percentile": price_percentile,
        "volume_ratio": volume_ratio,
        "low_high_mask": low_high_mask,
        "high_high_mask": high_high_mask,
        "rsi_overbought": rsi_overbought,
        "rsi_oversold": rsi_oversold,
        "adx": adx,
        "+di": plus_di,
        "-di": minus_di,
        "adx_up": adx_up,
        "adx_down": adx_down,
        "buy_stars": buy_count,
        "sell_stars": sell_count,
        "ma_status": ma_status,
    }


def export_recent_signals(df: pd.DataFrame, path: str = "signals_60d.json", lookback: int = 60) -> None:
    signals = compute_signal_info(df)
    recent = df.iloc[-lookback:].copy()

    rows: list[Dict[str, Any]] = []
    for idx, row in recent.iterrows():
        ma_status_entry: Dict[str, Dict[str, bool]] = {}
        for ma_window, status in signals.get("ma_status", {}).items():
            ma_status_entry[f"ma_{ma_window}"] = {
                "above": bool(status["above"].loc[idx]),
                "below": bool(status["below"].loc[idx]),
                "stood_above_3": bool(status["stood_above_3"].loc[idx]),
                "fell_below_3": bool(status["fell_below_3"].loc[idx]),
            }

        entry: Dict[str, Any] = {
            "date": idx.strftime("%Y-%m-%d"),
            "close": round(float(row.get("close", float("nan"))), 2) if not pd.isna(row.get("close")) else None,
            "volume": round(float(row.get("volume", float("nan"))), 2) if not pd.isna(row.get("volume")) else None,
            "volume_ratio_ma20": round(float(signals["volume_ratio"].loc[idx]), 2) if signals["volume_ratio"] is not None and not pd.isna(signals["volume_ratio"].loc[idx]) else None,
            "price_percentile_20": round(float(signals["price_percentile"].loc[idx]), 4) if signals["price_percentile"] is not None and not pd.isna(signals["price_percentile"].loc[idx]) else None,
            "rsi14": round(float(row.get("rsi_14", float("nan"))), 2) if not pd.isna(row.get("rsi_14")) else None,
            "bb_lower": round(float(row.get("bb_lower", float("nan"))), 2) if not pd.isna(row.get("bb_lower")) else None,
            "bb_lower_slope": round(float(row.get("bb_lower_slope", float("nan"))), 4) if not pd.isna(row.get("bb_lower_slope")) else None,
            "atr_pct_14": round(float(row.get("atr_pct_14", float("nan"))), 3) if not pd.isna(row.get("atr_pct_14")) else None,
            "ma_5": round(float(row.get("ma_5", float("nan"))), 2) if not pd.isna(row.get("ma_5")) else None,
            "ma_10": round(float(row.get("ma_10", float("nan"))), 2) if not pd.isna(row.get("ma_10")) else None,
            "ma_20": round(float(row.get("ma_20", float("nan"))), 2) if not pd.isna(row.get("ma_20")) else None,
            "ma_60": round(float(row.get("ma_60", float("nan"))), 2) if not pd.isna(row.get("ma_60")) else None,
            "ma_120": round(float(row.get("ma_120", float("nan"))), 2) if not pd.isna(row.get("ma_120")) else None,
            "ma_180": round(float(row.get("ma_180", float("nan"))), 2) if not pd.isna(row.get("ma_180")) else None,
            "buy_stars": int(signals["buy_stars"].loc[idx]) if not pd.isna(signals["buy_stars"].loc[idx]) else 0,
            "sell_stars": int(signals["sell_stars"].loc[idx]) if not pd.isna(signals["sell_stars"].loc[idx]) else 0,
            "signals": {
                "rsi_oversold": bool(signals["rsi_oversold"].loc[idx]),
                "rsi_overbought": bool(signals["rsi_overbought"].loc[idx]),
                "low_price_high_vol": bool(signals["low_high_mask"].loc[idx]),
                "high_price_high_vol": bool(signals["high_high_mask"].loc[idx]),
                "adx_down": bool(signals["adx_down"].loc[idx]),
                "adx_up": bool(signals["adx_up"].loc[idx]),
            },
            "ma_status": ma_status_entry,
        }
        rows.append(entry)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"已导出最近 {lookback} 天信号至 {path}")


def export_atr_metrics(
    df: pd.DataFrame,
    period: int = 14,
    lookback: int = 180,
    path: str = "atr_metrics.json",
) -> None:
    """
    导出最近 lookback 天的 ATR 与 ATR% 序列及摘要统计。
    """
    atr_col = f"atr_{period}"
    atr_pct_col = f"atr_pct_{period}"
    if atr_pct_col not in df or atr_col not in df:
        raise ValueError(f"DataFrame 缺少 {atr_col} 或 {atr_pct_col} 列，无法导出 ATR。")

    subset = df.dropna(subset=[atr_pct_col, atr_col]).tail(lookback)
    series: List[Dict[str, Any]] = []
    for idx, row in subset.iterrows():
        series.append(
            {
                "date": idx.strftime("%Y-%m-%d"),
                "atr": round(float(row[atr_col]), 2),
                "atr_pct": round(float(row[atr_pct_col]), 3),
                "close": round(float(row["close"]), 2),
            }
        )

    pct_values = [item["atr_pct"] for item in series]
    summary = {}
    if pct_values:
        summary = {
            "latest": series[-1],
            "average_pct": round(float(np.mean(pct_values)), 3),
            "max_pct": round(float(np.max(pct_values)), 3),
            "min_pct": round(float(np.min(pct_values)), 3),
        }

    payload = {
        "period": period,
        "lookback_days": lookback,
        "series": series,
        "summary": summary,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"已导出 ATR 数据至 {path}（周期 {period}，最近 {lookback} 天）")

def plot_price_volume_rsi(
    df: pd.DataFrame,
    output_path: Optional[str] = None,
    show: bool = True,
    ma_windows: Optional[Iterable[int]] = None,
    plot_mas: bool = True,
    atr_period: int = 14,
) -> None:
    """
    绘制收盘价 + 布林带、成交量、RSI 指标。
    如传入 output_path，会将图像写入对应文件。
    """
    if df.empty:
        raise ValueError("No data available for plotting.")

    ma_windows_list = list(ma_windows) if ma_windows is not None else []

    fig, (ax_price, ax_volume, ax_macd, ax_dmi, ax_rsi) = plt.subplots(
        5,
        1,
        figsize=(14, 14),
        sharex=True,
        gridspec_kw={"height_ratios": [3.0, 1.0, 1.1, 1.1, 1.2]},
    )

    # 收盘价 + 布林带
    ax_price.plot(df.index, df["close"], label="Close", color="black", linewidth=1.2)
    ax_price.plot(df.index, df["bb_mid"], label="BB Mid (20)", color="#1e88e5", linewidth=1)
    ax_price.fill_between(
        df.index,
        df["bb_lower"],
        df["bb_upper"],
        color="#90caf9",
        alpha=0.35,
        label="BBand ±2σ",
    )
    if plot_mas and ma_windows_list:
        ma_colors = [
            "#ff7043",
            "#ffa726",
            "#fdd835",
            "#66bb6a",
            "#26c6da",
            "#42a5f5",
            "#ab47bc",
            "#8d6e63",
            "#78909c",
        ]
        for idx, window in enumerate(ma_windows_list):
            ma_col = f"ma_{window}"
            if ma_col in df and df[ma_col].notna().any():
                ax_price.plot(
                    df.index,
                    df[ma_col],
                    label=f"MA{window}",
                    color=ma_colors[idx % len(ma_colors)],
                    linewidth=1,
                    alpha=0.9,
                )

    signal_data = compute_signal_info(df)
    price_percentile = signal_data["price_percentile"]
    volume_ratio = signal_data["volume_ratio"]
    low_high_mask = signal_data["low_high_mask"]
    high_high_mask = signal_data["high_high_mask"]
    rsi_overbought = signal_data["rsi_overbought"]
    rsi_oversold = signal_data["rsi_oversold"]
    adx = signal_data["adx"]
    plus_di = signal_data["+di"]
    minus_di = signal_data["-di"]
    adx_up = signal_data["adx_up"]
    adx_down = signal_data["adx_down"]
    buy_count = signal_data["buy_stars"]
    sell_count = signal_data["sell_stars"]

    adx_threshold_up = 40
    adx_threshold_down = 40

    if low_high_mask.any():
        ax_price.scatter(
            df.index[low_high_mask],
            df["close"][low_high_mask],
            marker="^",
            facecolors="#d32f2f",
            edgecolors="#212121",
            linewidths=0.8,
            s=70,
            label="Low price & high vol",
            zorder=6,
        )
    if high_high_mask.any():
        ax_price.scatter(
            df.index[high_high_mask],
            df["close"][high_high_mask],
            marker="^",
            facecolors="#ffb300",
            edgecolors="#e65100",
            linewidths=0.8,
            s=70,
            label="High price & high vol",
            zorder=6,
        )
    if rsi_overbought.any():
        ax_price.scatter(
            df.index[rsi_overbought],
            df["close"][rsi_overbought],
            marker="s",
            facecolors="#ffe082",
            edgecolors="#f57f17",
            linewidths=1.0,
            s=65,
            label="RSI14 > 70",
            zorder=7,
        )
    if rsi_oversold.any():
        ax_price.scatter(
            df.index[rsi_oversold],
            df["close"][rsi_oversold],
            marker="o",
            facecolors="#e3f2fd",
            edgecolors="#0d47a1",
            linewidths=1.0,
            s=65,
            label="RSI14 < 30",
            zorder=7,
        )
    if adx_up.any():
        ax_price.scatter(
            df.index[adx_up],
            df["close"][adx_up],
            marker="^",
            facecolors="none",
            edgecolors="#2e7d32",
            linewidths=1.2,
            s=70,
            label=f"ADX>{adx_threshold_up} (+DI>-DI)",
            zorder=8,
        )
    if adx_down.any():
        ax_price.scatter(
            df.index[adx_down],
            df["close"][adx_down],
            marker="v",
            facecolors="none",
            edgecolors="#c62828",
            linewidths=1.2,
            s=70,
            label=f"ADX>{adx_threshold_down} (-DI>+DI)",
            zorder=8,
        )

    buy_star_colors = {1: "#a5d6a7", 2: "#66bb6a", 3: "#1b5e20"}
    sell_star_colors = {1: "#ef9a9a", 2: "#ef5350", 3: "#b71c1c"}

    for stars in range(1, 4):
        mask = buy_count == stars
        if mask.any():
            ax_price.scatter(
                df.index[mask],
                df["close"][mask],
                marker="$★$",
                s=120 + stars * 40,
                color=buy_star_colors.get(stars, "#66bb6a"),
                alpha=0.85,
                label=f"Buy {'★' * stars}",
                zorder=9,
            )

    for stars in range(1, 4):
        mask = sell_count == stars
        if mask.any():
            ax_price.scatter(
                df.index[mask],
                df["close"][mask],
                marker="$★$",
                s=120 + stars * 40,
                color=sell_star_colors.get(stars, "#ef5350"),
                alpha=0.85,
                label=f"Sell {'★' * stars}",
                zorder=9,
            )

    ma_spans: dict[int, list[tuple[pd.Timestamp, pd.Timestamp]]] = {}
    for window in [60, 120, 180]:
        ma_col = f"ma_{window}"
        if ma_col not in df:
            continue
        above = (df["close"] > df[ma_col]).fillna(False)
        spans: list[tuple[pd.Timestamp, pd.Timestamp]] = []
        for i in range(2, len(df)):
            if above.iloc[i] and above.iloc[i - 1] and above.iloc[i - 2]:
                prev_index = i - 3
                if prev_index >= 0 and above.iloc[prev_index]:
                    continue
                spans.append((df.index[i - 2], df.index[i]))
        if spans:
            ma_spans[window] = spans

    color_map = {60: "#0288d1", 120: "#7b1fa2", 180: "#f4511e"}
    for window, spans in ma_spans.items():
        for start, _ in spans:
            price = df.loc[start, "close"]
            ax_price.scatter(
                [start],
                [price],
                marker="*",
                s=80,
                color=color_map.get(window, "#455a64"),
                edgecolors="#263238",
                linewidths=0.6,
                zorder=9,
                label=f"Above MA{window} (3d)",
            )
            ax_price.annotate(
                start.strftime("%Y-%m-%d"),
                xy=(start, price),
                xytext=(0, 12),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                color=color_map.get(window, "#455a64"),
            )

    latest_slope = df["bb_lower_slope"].iloc[-1] if "bb_lower_slope" in df else np.nan
    latest_slope_ma5 = df["bb_lower_slope_ma_5"].iloc[-1] if "bb_lower_slope_ma_5" in df else np.nan
    if not np.isnan(latest_slope) and not np.isnan(latest_slope_ma5):
        slope_text = (
            f"BB Lower slope: {latest_slope:.2f}%\n"
            f"BB Lower slope MA5: {latest_slope_ma5:.2f}%"
        )
        ax_price.text(
            0.99,
            0.98,
            slope_text,
            transform=ax_price.transAxes,
            fontsize=9,
            verticalalignment="top",
            horizontalalignment="right",
            bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.7},
        )

    ax_price.set_ylabel("Price (USDT)")
    ax_price.set_title("OKX ETH/USDT Daily")
    ax_price.grid(True, linestyle="--", alpha=0.1)
    handles, labels = ax_price.get_legend_handles_labels()
    uniq_handles: list[object] = []
    uniq_labels: list[str] = []
    for handle, label in zip(handles, labels):
        if label not in uniq_labels:
            uniq_handles.append(handle)
            uniq_labels.append(label)
    ax_price.legend(uniq_handles, uniq_labels, loc="upper left", ncol=2, fontsize=9)

    # 成交量
    volume_ma_col = "volume_ma_20"
    volume_ratio_col = "volume_ratio_ma_20"
    colors = np.full(len(df), "#9e9e9e", dtype=object)
    ratio = df.get(volume_ratio_col)
    if ratio is not None:
        high_mask = ratio > 2.0
        low_mask = ratio < 0.7
        colors[high_mask.fillna(False).to_numpy()] = "#ef5350"
        colors[low_mask.fillna(False).to_numpy()] = "#42a5f5"
    ax_volume.bar(df.index, df["volume"], color=colors, width=0.8)
    ma_line = None
    if volume_ma_col in df and df[volume_ma_col].notna().any():
        ma_line, = ax_volume.plot(
            df.index,
            df[volume_ma_col],
            color="#ffa726",
            linewidth=1.4,
            label="Volume MA (20)",
        )
    ax_volume.set_ylabel("Volume")
    ax_volume.grid(True, linestyle="--", alpha=0.1)
    legend_handles = [
        Patch(facecolor="#ef5350", edgecolor="none", label=">2x MA (High Vol)"),
        Patch(facecolor="#42a5f5", edgecolor="none", label="<0.7x MA (Low Vol)"),
        Patch(facecolor="#9e9e9e", edgecolor="none", label="Normal"),
    ]
    handles = legend_handles.copy()
    if ma_line is not None:
        handles.append(ma_line)
    ax_volume.legend(handles=handles, loc="upper left")

    # MACD
    macd_line = df.get("macd_line")
    macd_signal = df.get("macd_signal")
    macd_hist = df.get("macd_hist")
    if macd_line is not None and macd_signal is not None and macd_hist is not None:
        hist_colors = np.where(macd_hist >= 0, "#26a69a", "#ef5350")
        ax_macd.bar(df.index, macd_hist, color=hist_colors, width=0.8, label="Histogram")
        ax_macd.plot(df.index, macd_line, color="#1976d2", linewidth=1.2, label="MACD")
        ax_macd.plot(df.index, macd_signal, color="#ffa726", linewidth=1.0, label="Signal")
    ax_macd.axhline(0, color="#616161", linewidth=0.8, linestyle="--")
    ax_macd.set_ylabel("MACD")
    ax_macd.grid(True, linestyle="--", alpha=0.1)
    ax_macd.legend(loc="upper left")

    # DMI / ADX
    adx = df.get("adx", pd.Series(index=df.index, dtype=float))
    plus_di = df.get("+di", pd.Series(index=df.index, dtype=float))
    minus_di = df.get("-di", pd.Series(index=df.index, dtype=float))
    di_axis = ax_dmi.twinx()
    dmi_handles = []
    dmi_labels = []
    if adx.notna().any():
        line_adx, = ax_dmi.plot(df.index, adx, label="ADX", color="#6d4c41", linewidth=1.2)
        dmi_handles.append(line_adx)
        dmi_labels.append("ADX")
    if plus_di.notna().any():
        line_plus, = di_axis.plot(df.index, plus_di, label="+DI", color="#2e7d32", linewidth=1.0)
        dmi_handles.append(line_plus)
        dmi_labels.append("+DI")
    if minus_di.notna().any():
        line_minus, = di_axis.plot(df.index, minus_di, label="-DI", color="#c62828", linewidth=1.0)
        dmi_handles.append(line_minus)
        dmi_labels.append("-DI")
    ax_dmi.axhline(adx_threshold_up, color="#9e9e9e", linestyle="--", linewidth=0.8)
    ax_dmi.set_ylim(0, 100)
    di_max = float(
        np.nanmax(
            [
                plus_di.max(skipna=True) if isinstance(plus_di, pd.Series) else np.nan,
                minus_di.max(skipna=True) if isinstance(minus_di, pd.Series) else np.nan,
                40.0,
            ]
        )
    )
    di_axis.set_ylim(0, di_max * 1.1)
    ax_dmi.set_ylabel("ADX")
    di_axis.set_ylabel("DI")
    ax_dmi.grid(True, linestyle="--", alpha=0.1)
    ax_dmi.legend(dmi_handles, dmi_labels, loc="upper left")

    # RSI
    rsi_columns = [col for col in df.columns if col.startswith("rsi_")]
    for col in rsi_columns:
        ax_rsi.plot(df.index, df[col], label=col.upper())
    ax_rsi.axhline(70, color="#f4511e", linestyle="--", linewidth=0.8)
    ax_rsi.axhline(30, color="#43a047", linestyle="--", linewidth=0.8)
    ax_rsi.set_ylabel("RSI")
    ax_rsi.set_xlabel("Date")
    ax_rsi.set_ylim(0, 100)

    atr_col = f"atr_pct_{atr_period}"
    atr_series = df.get(atr_col)
    legend_handles, legend_labels = ax_rsi.get_legend_handles_labels()
    if atr_series is not None and isinstance(atr_series, pd.Series) and atr_series.notna().any():
        ax_atr = ax_rsi.twinx()
        atr_line, = ax_atr.plot(
            df.index,
            atr_series,
            color="#ff8f00",
            linewidth=1.2,
            label=f"ATR% ({atr_period})",
        )
        ax_atr.set_ylabel("ATR%")
        atr_max = float(atr_series.max(skipna=True))
        ax_atr.set_ylim(0, atr_max * 1.2 if np.isfinite(atr_max) else 5)
        ax_atr.grid(False)
        legend_handles.append(atr_line)
        legend_labels.append(f"ATR% ({atr_period})")

    ax_rsi.legend(legend_handles, legend_labels, loc="upper left")
    ax_rsi.grid(True, linestyle="--", alpha=0.1)

    # 时间格式
    ax_rsi.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate()
    plt.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=150)
    if show:
        plt.show()
    else:
        plt.close(fig)


def main() -> None:
    exchange = build_exchange()

    df = fetch_daily_ohlcv(exchange)
    print(f"获取到日线条数: {len(df)}，时间范围: {df.index.min()} ~ {df.index.max()}")
    if len(df) > 0:
        df = df.iloc[:-1].copy()
    print(f"去除未收盘当日后条数: {len(df)}")
    df = add_bollinger_bands(df)
    df = add_rsi_indicators(df, periods=[6, 14, 24])
    df = add_macd_indicators(df)
    df = add_dmi_indicators(df)
    df = add_atr_indicator(df, period=14)
    ma_windows = [5, 10, 20, 60, 120, 180, 200, 250, 360]
    df = add_price_moving_averages(df, windows=ma_windows)
    df = add_volume_indicators(df, ma_window=20)
    df = add_price_percentile(df, window=20)

    export_recent_signals(df, lookback=60)
    export_atr_metrics(df, period=14, lookback=180, path="atr_metrics.json")

    low_high_mask = ((df["price_percentile_20"] < 0.10) & (df["volume_ratio_ma_20"] > 2.0)).fillna(False)
    high_high_mask = ((df["price_percentile_20"] > 0.90) & (df["volume_ratio_ma_20"] > 2.0)).fillna(False)

    plot_price_volume_rsi(
        df,
        output_path="eth_okx_daily.png",
        ma_windows=ma_windows,
        plot_mas=False,
        atr_period=14,
    )

    latest = df.dropna().iloc[-1]
    prev_ratio = latest["prev_volume_ratio_ma_20"]
    ma_volume = latest["volume_ma_20"]
    prev_volume = df["volume"].iloc[-2] if len(df) >= 2 else float("nan")
    bb_lower_slope = latest["bb_lower_slope"]
    bb_lower_slope_ma5 = latest["bb_lower_slope_ma_5"]
    print("上一个交易日成交量:", f"{prev_volume:,.2f}")
    print("当前 20 日成交量均值:", f"{ma_volume:,.2f}")
    print("前一日成交量占 20 日均量比例:", f"{prev_ratio:.2%}")
    print("布林带下轨斜率:", f"{bb_lower_slope:.2f}%")
    print("布林带下轨斜率 5 日均值:", f"{bb_lower_slope_ma5:.2f}%")
    print("低位放量信号数量:", int(low_high_mask.sum()))
    print("高位放量信号数量:", int(high_high_mask.sum()))


if __name__ == "__main__":
    main()
