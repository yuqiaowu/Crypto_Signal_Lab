from __future__ import annotations

import json
import os
import time
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List

import requests

SIGNAL_FILE = Path("signals_60d.json")
ONCHAIN_SNAPSHOT_FILE = Path("global_onchain_news_snapshot.json")


def load_signals(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise SystemExit(
            f"未找到 {path}。请先运行 `python 获取数据.py` 生成信号数据，再执行本脚本。"
        )
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_onchain_snapshot(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _summarize_news(snapshot: Dict[str, Any]) -> str | None:
    news = snapshot.get("news")
    if not isinstance(news, dict):
        return None
    highlights: List[str] = []
    for topic in ("bitcoin", "ethereum", "general", "cryptocompare"):
        section = news.get(topic)
        if not isinstance(section, dict):
            continue
        section_items = section.get("items")
        if isinstance(section_items, list):
            for entry in section_items[:3]:
                if not isinstance(entry, dict):
                    continue
                title = entry.get("title")
                source = entry.get("source")
                if not title:
                    continue
                highlights.append(f"{title} ({source})" if source else str(title))
        if len(highlights) >= 6:
            break
    if not highlights:
        return None
    return "； ".join(highlights[:6])


def build_onchain_parts(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    if not snapshot:
        return {"extra_blocks": [], "paragraphs": {}}
    dr = snapshot.get("daily_report", {}) if isinstance(snapshot, dict) else {}
    stable_para = dr.get("stablecoins", {}).get("paragraph")
    bridge_para = dr.get("bridges", {}).get("paragraph")
    fear_para = dr.get("fear_greed", {}).get("paragraph")

    eth_gas = snapshot.get("eth_gas", {})
    btc_mempool = snapshot.get("btc_mempool", {})
    eth_oracle = eth_gas.get("gas_oracle_summary") if isinstance(eth_gas, dict) else None
    eth_base_fee = None
    blockchair_eth = snapshot.get("blockchair", {}).get("ethereum") if isinstance(snapshot.get("blockchair"), dict) else None
    if isinstance(blockchair_eth, dict):
        gs = blockchair_eth.get("gas_snapshot")
        if isinstance(gs, dict):
            eth_base_fee = gs.get("base_fee_gwei")
    btc_rec = btc_mempool.get("recommended_fees") if isinstance(btc_mempool, dict) else None

    gas_para_parts = []
    if isinstance(eth_oracle, dict):
        gas_para_parts.append(
            f"ETH Gas — 提议: {eth_oracle.get('propose_gwei')} gwei, 安全: {eth_oracle.get('safe_gwei')} gwei, 快速: {eth_oracle.get('fast_gwei')} gwei, 建议基础费: {eth_oracle.get('suggest_base_fee')} gwei"
        )
    if eth_base_fee is not None:
        gas_para_parts.append(f"Blockchair 基础费参考: {eth_base_fee} gwei")
    if isinstance(btc_rec, dict):
        gas_para_parts.append(
            f"BTC Mempool 建议费率: 最低 {btc_rec.get('minimumFee')} sat/vB, 经济 {btc_rec.get('economyFee')} sat/vB, 正常 {btc_rec.get('normalFee')} sat/vB, 优先 {btc_rec.get('priorityFee')} sat/vB"
        )

    gas_para = "；".join([p for p in gas_para_parts if p]) if gas_para_parts else None

    news_summary = None
    dr_news = dr.get("news") if isinstance(dr, dict) else None

    def _format_usd(value: Any) -> str:
        try:
            num = float(value)
        except (TypeError, ValueError):
            return "N/A"
        abs_num = abs(num)
        if abs_num >= 1e9:
            return f"{num / 1e9:.2f}B"
        if abs_num >= 1e6:
            return f"{num / 1e6:.1f}M"
        if abs_num >= 1e3:
            return f"{num / 1e3:.1f}K"
        return f"{num:.0f}"

    derivatives = snapshot.get("derivatives") if isinstance(snapshot, dict) else None
    derivatives_okx = derivatives.get("okx") if isinstance(derivatives, dict) else None
    oi_data = derivatives_okx.get("eth_open_interest_volume") if isinstance(derivatives_okx, dict) else None
    liq_data = derivatives_okx.get("eth_liquidations") if isinstance(derivatives_okx, dict) else None
    derivatives_para_parts: List[str] = []

    if isinstance(oi_data, dict):
        latest = oi_data.get("latest")
        prev = oi_data.get("previous")
        change_pct = oi_data.get("change_pct")
        if isinstance(latest, dict):
            date_str = latest.get("date_cn") or latest.get("timestamp")
            oi_val = latest.get("open_interest_usd")
            vol_val = latest.get("perp_volume_usd")
            piece = f"OKX 永续开仓量（{date_str}）≈ {_format_usd(oi_val)} USD"
            if change_pct is not None:
                piece += f" ({change_pct:+.2f}% d/d)"
            elif isinstance(prev, dict) and prev.get("open_interest_usd"):
                try:
                    diff = float(oi_val) - float(prev.get("open_interest_usd"))
                    piece += f" (较前日变动 {_format_usd(diff)})"
                except (TypeError, ValueError):
                    pass
            if vol_val is not None:
                piece += f"，当日永续成交额 {_format_usd(vol_val)} USD"
            derivatives_para_parts.append(piece)
        elif oi_data.get("error"):
            derivatives_para_parts.append(f"OKX 开仓量获取失败: {oi_data.get('error')}")

    if isinstance(liq_data, dict):
        series = liq_data.get("series")
        totals = liq_data.get("totals")
        if isinstance(series, list) and series:
            latest_liq = series[-1]
            latest_piece = (
                f"最近爆仓（{latest_liq.get('date')}）多头 {_format_usd(latest_liq.get('long_liquidations_usd'))} USD，"
                f"空头 {_format_usd(latest_liq.get('short_liquidations_usd'))} USD"
            )
            derivatives_para_parts.append(latest_piece)
        if isinstance(totals, dict) and derivatives_para_parts:
            totals_piece = (
                f"样本区间合计：多头 {_format_usd(totals.get('long_usd'))} USD，空头 {_format_usd(totals.get('short_usd'))} USD"
            )
            derivatives_para_parts.append(totals_piece)
        if liq_data.get("error"):
            derivatives_para_parts.append(f"爆仓数据获取失败: {liq_data.get('error')}")

    derivatives_para = "； ".join(derivatives_para_parts) if derivatives_para_parts else None

    extra_blocks: List[str] = []
    if stable_para:
        extra_blocks.append("稳定币摘要：" + str(stable_para))
    if bridge_para:
        extra_blocks.append("跨链桥接摘要：" + str(bridge_para))
    if fear_para:
        extra_blocks.append("恐慌指数摘要：" + str(fear_para))
    if gas_para:
        extra_blocks.append("Gas/Mempool 摘要：" + str(gas_para))
    if isinstance(dr_news, dict):
        extra_blocks.append(
            "新闻原始数据（JSON）：\n" + json.dumps(dr_news, ensure_ascii=False, indent=2)
        )
    if derivatives_para:
        extra_blocks.append("衍生品摘要：" + derivatives_para)
    if isinstance(derivatives_okx, dict):
        extra_blocks.append("衍生品原始数据（OKX）：\n" + json.dumps(derivatives_okx, ensure_ascii=False, indent=2))
    return {
        "extra_blocks": extra_blocks,
        "paragraphs": {
            "stable": stable_para,
            "bridge": bridge_para,
            "fear": fear_para,
            "gas": gas_para,
            "news": news_summary,
            "derivatives": derivatives_para,
        },
    }


def summarize_latest_day(signals: List[Dict[str, Any]]) -> str | None:
    if not signals:
        return None
    latest = signals[-1]
    if not isinstance(latest, dict):
        return None
    date = latest.get("date", "未知日期")
    close = latest.get("close")
    volume = latest.get("volume")
    vol_ratio = latest.get("volume_ratio_ma20")
    rsi = latest.get("rsi14")
    bb_lower = latest.get("bb_lower")
    bb_slope = latest.get("bb_lower_slope")
    atr_pct = latest.get("atr_pct_14")
    ma_values = {
        "MA5": latest.get("ma_5"),
        "MA10": latest.get("ma_10"),
        "MA20": latest.get("ma_20"),
        "MA60": latest.get("ma_60"),
    }

    def _fmt(value: Any) -> str:
        try:
            return f"{float(value):,.2f}"
        except (TypeError, ValueError):
            return "N/A"

    def _fmt_pct(value: Any) -> str:
        try:
            return f"{float(value):.2f}%"
        except (TypeError, ValueError):
            return "N/A"

    parts: List[str] = [
        f"最新交易日（{date}）收盘 { _fmt(close) } USD",
    ]

    ma_parts: List[str] = []
    for label, base in ma_values.items():
        try:
            diff_pct = (float(close) / float(base) - 1.0) * 100 if close and base else None
        except (TypeError, ValueError, ZeroDivisionError):
            diff_pct = None
        if base is not None:
            if diff_pct is not None:
                ma_parts.append(f"{label} { _fmt(base) } ({diff_pct:+.2f}%)")
            else:
                ma_parts.append(f"{label} { _fmt(base) }")
    if ma_parts:
        parts.append(" | ".join(ma_parts))

    vol_piece = f"成交量 { _fmt(volume) }"
    if vol_ratio is not None:
        try:
            vol_piece += f"（为20日均量的 {float(vol_ratio):.2f}x）"
        except (TypeError, ValueError):
            pass
    parts.append(vol_piece)

    if rsi is not None:
        parts.append(f"RSI14 { _fmt(rsi) }")
    if bb_lower is not None:
        bb_piece = f"布林带下轨 { _fmt(bb_lower) }"
        if bb_slope is not None:
            try:
                bb_piece += f"，斜率 {float(bb_slope):+.4f}"
            except (TypeError, ValueError):
                pass
        parts.append(bb_piece)
    if atr_pct is not None:
        parts.append(f"ATR%14 {_fmt_pct(atr_pct)}")
    return "； ".join(parts)


def compute_latest_ma_relation(signals: List[Dict[str, Any]]) -> Dict[str, str] | None:
    if not signals:
        return None
    latest = signals[-1]
    if not isinstance(latest, dict):
        return None
    ma_status = latest.get("ma_status")
    if not isinstance(ma_status, dict):
        return None
    relation: Dict[str, str] = {}
    for ma_key, status in ma_status.items():
        if not isinstance(status, dict):
            continue
        above = bool(status.get("above"))
        below = bool(status.get("below"))
        if above and not below:
            relation[ma_key] = "above"
        elif below and not above:
            relation[ma_key] = "below"
        elif above and below:
            relation[ma_key] = "both"
        else:
            relation[ma_key] = "unknown"
    return relation or None


def build_payload(
    signals: List[Dict[str, Any]],
    onchain: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    today_str = time.strftime("%Y-%m-%d", time.localtime())
    instructions = f"""
你是一名资深的币圈投资分析师。以下数据仅包含最近60天已收盘的日线，请基于下列规则严格分析，并给出买入/卖出建议：
1. 识别买入信号时，务必检查布林带下轨斜率是否趋缓或开始向上；若布林带仍陡峭向下，即使出现触碰下轨也需谨慎。
2. 理想买入点应满足：布林带斜率趋缓或向上拐头，同时价格贴近或触碰下轨，并结合 RSI、成交量及关键均线表现进行验证。
3. 综合多个指标，尤其注意 RSI、关键点位突破情况（是否连续3天站上关键均线且放量）、成交量变化，而非单一信号判断。
4. 在形成建议时，请清晰描述你的逻辑，尤其是布林带形态、成交量与均线的配合情况。
5. 数据中已为每个交易日计算买入/卖出星级（0~3星，分别基于 RSI、放量、DMI 叠加），请结合星级及其他指标作出具体建议，并说明理由。
6. 请判断是否“有效站上/跌破关键均线”，并给出依据：默认关注 MA20/MA60/MA120/MA180；“有效”的定义为价格至少连续3天在均线之上/之下，同时量能不低于均量（以 `volume_ratio_ma20` 为准；≥1.0 为基本支持，≥1.5 为较强支持）。
7. `recent_data` 按时间顺序排列，请务必以最后一条记录视为最新收盘日，并据此判断当前市场状态。
8. 已额外提供 `latest_ma_relation` 字段，标明最新收盘价相对各条均线的位置（above / below / both / unknown），请在分析中引用该字段验证你的判断。
9. 请在《市场概述》的开头明确写出今天是 {today_str}（当地时间），确保读者了解分析日期。
10. 输出必须使用 Markdown 格式：各章节标题使用二级标题（##），要点使用项目符号（-）；不要使用《》包裹标题。
请输出：
- 按以下标题输出详细内容（无须额外说明）：
  1. 《市场概述》——布林带、均线、量能综合评价。
  2. 《信号解读》——列出买入/卖出星级及理由，指明是否符合规则。
  3. 《关键价位》——若存在重要支撑/压力，请给出现价或区间。
  4. 《操作建议》——分别给出短期（1-2 周）与中期（1-2 月）策略。
  5. 《风险与关注》——提示潜在风险以及需要观测的指标变化。
  6. 《波动率观察》——解析 ATR% 的趋势与对策略的影响。
  7. 《链上与情绪》——分别引用稳定币、桥接、Gas/Mempool、恐慌指数、新闻数据以及衍生品指标（OKX 永续开仓量与多空爆仓）的具体数值，分析其含义及对价格/策略的影响；如某项缺失须说明原因。
""".strip()

    payload: Dict[str, Any] = {
        "instructions": instructions,
        "recent_data": signals,
        "extra_blocks": [],
    }
    payload["extra_blocks"].append(f"今日日期：{today_str}")
    latest_summary = summarize_latest_day(signals)
    if latest_summary:
        payload["extra_blocks"].append("最新交易日摘要：" + latest_summary)
    latest_relation = compute_latest_ma_relation(signals)
    if latest_relation:
        payload["latest_ma_relation"] = latest_relation
        payload["extra_blocks"].append(
            "最新均线相对位置：" + json.dumps(latest_relation, ensure_ascii=False)
        )
    if onchain:
        oc = build_onchain_parts(onchain)
        payload["extra_blocks"].extend(oc.get("extra_blocks", []))
        payload["onchain_paragraphs"] = oc.get("paragraphs", {})
    return payload


def call_deepseek(
    api_key: str,
    proxy: str | None,
    payload: Dict[str, Any],
    model: str | None = None,
    max_retries: int | None = None,
    backoff_seconds: int | None = None,
) -> str:
    url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
    model_name = model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    proxies = {"http": proxy, "https": proxy} if proxy else None

    system_prompt = payload["instructions"]
    user_blocks = [
        "以下是最近60天的信号数据（JSON）：\n" + json.dumps(payload["recent_data"], ensure_ascii=False, indent=2)
    ]
    for block in payload.get("extra_blocks", []):
        user_blocks.append(str(block))
    user_message = "\n\n".join(user_blocks)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    retries = max_retries if max_retries is not None else int(os.getenv("DEEPSEEK_MAX_RETRIES", "6"))
    retries = max(1, retries)
    backoff = backoff_seconds if backoff_seconds is not None else int(os.getenv("DEEPSEEK_RETRY_BACKOFF", "60"))
    backoff = max(1, backoff)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    request_payload = {
        "model": model_name,
        "messages": messages,
        "temperature": float(os.getenv("DEEPSEEK_TEMPERATURE", "0.6")),
        "max_tokens": int(os.getenv("DEEPSEEK_MAX_TOKENS", "2048")),
        "stream": False,
    }

    for attempt in range(retries):
        response = requests.post(
            url,
            headers=headers,
            json=request_payload,
            proxies=proxies,
            timeout=120,
        )
        if response.status_code == 429:
            if attempt < retries - 1:
                wait_seconds = backoff * (attempt + 1)
                print(f"DeepSeek API 返回 429，{wait_seconds}s 后重试（第 {attempt + 1}/{retries} 次）")
                time.sleep(wait_seconds)
                continue
            raise RuntimeError("DeepSeek API 返回 429（请求过多）。请稍后再试或检查配额。")
        if response.status_code >= 500 and attempt < retries - 1:
            wait_seconds = backoff * (attempt + 1)
            print(f"DeepSeek API 返回 {response.status_code}，{wait_seconds}s 后重试（第 {attempt + 1}/{retries} 次）")
            time.sleep(wait_seconds)
            continue
        if response.status_code == 400:
            try:
                err_obj = response.json()
                detail = err_obj.get("error", {}).get("message") or err_obj
            except ValueError:
                detail = response.text
            print(f"DeepSeek API 返回 400：{detail}")
            raise RuntimeError(f"DeepSeek API 返回 400（请求无效）：{detail}")
        if response.status_code >= 400:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            response.raise_for_status()
        try:
            result = response.json()
        except ValueError as exc:
            raise RuntimeError(f"DeepSeek API 返回无法解析的内容：{response.text[:500]}") from exc
        break
    else:
        raise RuntimeError("DeepSeek API 调用失败，已达到最大重试次数。")

    text_parts: List[str] = []
    choices = result.get("choices", [])
    for choice in choices:
        msg = choice.get("message", {})
        content = msg.get("content")
        if content:
            text_parts.append(content)
    return "\n".join(text_parts).strip()


def call_gemini(
    api_key: str,
    proxy: str | None,
    payload: Dict[str, Any],
    model: str | None = None,
    max_retries: int | None = None,
    backoff_seconds: int | None = None,
) -> str:
    model_name = model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    api_version = os.getenv("GEMINI_API_VERSION", "v1")
    base_url = os.getenv(
        "GEMINI_API_URL",
        f"https://generativelanguage.googleapis.com/{api_version}/models/{model_name}:generateContent",
    )
    proxies = {"http": proxy, "https": proxy} if proxy else None

    parts = [
        {"text": payload["instructions"]},
        {
            "text": "以下是最近60天的信号数据（JSON）：\n"
            + json.dumps(payload["recent_data"], ensure_ascii=False, indent=2)
        },
    ]
    for block in payload.get("extra_blocks", []):
        parts.append({"text": str(block)})

    request_payload = {"contents": [{"parts": parts}]}

    retries = max_retries if max_retries is not None else int(os.getenv("GEMINI_MAX_RETRIES", "6"))
    retries = max(1, retries)
    backoff = backoff_seconds if backoff_seconds is not None else int(os.getenv("GEMINI_RETRY_BACKOFF", "60"))
    backoff = max(1, backoff)

    for attempt in range(retries):
        response = requests.post(
            base_url,
            params={"key": api_key},
            json=request_payload,
            proxies=proxies,
            timeout=120,
        )
        if response.status_code == 429:
            if attempt < retries - 1:
                wait_seconds = backoff * (attempt + 1)
                print(f"Gemini API 返回 429，{wait_seconds}s 后重试（第 {attempt + 1}/{retries} 次）")
                time.sleep(wait_seconds)
                continue
            raise RuntimeError("Gemini API 返回 429（请求过多）。请稍后再试或检查配额。")
        if response.status_code >= 500 and attempt < retries - 1:
            wait_seconds = backoff * (attempt + 1)
            print(f"Gemini API 返回 {response.status_code}，{wait_seconds}s 后重试（第 {attempt + 1}/{retries} 次）")
            time.sleep(wait_seconds)
            continue
        if response.status_code >= 400:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            raise RuntimeError(f"Gemini API 调用失败：{detail}")
        try:
            result = response.json()
        except ValueError as exc:
            raise RuntimeError(f"Gemini API 返回无法解析的内容：{response.text[:500]}") from exc
        break
    else:
        raise RuntimeError("Gemini API 调用失败，已达到最大重试次数。")

    text_parts: List[str] = []
    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            text = part.get("text")
            if text:
                text_parts.append(text)
    return "\n".join(text_parts).strip()


def save_report(payload: Dict[str, Any], analysis_text: str, path: Path, model_label: str) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write(f"# {model_label} 分析报告\n\n")
        f.write("## 提示内容\n\n")
        f.write(payload["instructions"] + "\n\n")
        f.write("## 最近60天信号数据 (JSON)\n\n")
        f.write("```json\n" + json.dumps(payload["recent_data"], ensure_ascii=False, indent=2) + "\n```\n\n")
        if payload.get("onchain_paragraphs"):
            f.write("## 链上数据摘要\n\n")
            ocp = payload["onchain_paragraphs"]
            if ocp.get("stable"):
                f.write("- 稳定币：" + str(ocp["stable"]) + "\n")
            if ocp.get("bridge"):
                f.write("- 桥接：" + str(ocp["bridge"]) + "\n")
            if ocp.get("fear"):
                f.write("- 恐慌指数：" + str(ocp["fear"]) + "\n")
            if ocp.get("gas"):
                f.write("- Gas/Mempool：" + str(ocp["gas"]) + "\n")
            if ocp.get("news"):
                f.write("- 新闻要点：" + str(ocp["news"]) + "\n")
        if payload.get("extra_blocks"):
            f.write("\n## 链上快照 (JSON)\n\n")
            onchain_json = next((b for b in payload["extra_blocks"] if str(b).startswith("链上快照（JSON）：")), None)
            if onchain_json:
                content = str(onchain_json).split("链上快照（JSON）：", 1)[1]
                f.write("```json\n" + content + "\n```\n\n")
        f.write(f"## {model_label} 回复\n\n")
        f.write(analysis_text or "(无回复)")
        ts = datetime.now(timezone.utc).isoformat()
        f.write("\n\n---\nGenerated at: " + ts + " (UTC)\n")


def _format_email_markdown(text: str) -> str:
    t = (text or "").strip()
    if not t:
        return "(无回复)"
    date_match = re.search(r"今天是(\d{4}-\d{2}-\d{2})", t)
    date_str = date_match.group(1) if date_match else time.strftime("%Y-%m-%d", time.localtime())
    # 标题规范化：将《标题》或前置编号的《标题》转为二级标题
    t = re.sub(r"^\s*\d+\.\s*《([^》]+)》", r"## \1", t, flags=re.MULTILINE)
    t = re.sub(r"《([^》]+)》", r"## \1", t)
    # 在标题前插入空行，便于渲染
    t = re.sub(r"(?<!\n)\n## ", "\n\n## ", t)
    header = f"# AI 每日报告（{date_str}）\n"
    return header + "\n" + t

def save_email_body(analysis_text: str, path: Path) -> None:
    body = _format_email_markdown(analysis_text)
    with path.open("w", encoding="utf-8") as f:
        f.write(body)
        ts = datetime.now(timezone.utc).isoformat()
        f.write("\n\n---\nGenerated at: " + ts + " (UTC)\n")


def main() -> None:
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not deepseek_key and not gemini_key:
        raise SystemExit("未设置 DEEPSEEK_API_KEY 或 GEMINI_API_KEY，无法生成分析。")

    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    if proxy is not None:
        proxy = proxy.strip()

    use_local_proxy = os.environ.get("USE_LOCAL_PROXY", "1").lower()
    if proxy:
        pass
    elif use_local_proxy in {"1", "true", "yes"}:
        proxy = "http://127.0.0.1:7890"
    else:
        proxy = None
        for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
            os.environ.pop(key, None)

    signals = load_signals(SIGNAL_FILE)
    onchain = load_onchain_snapshot(ONCHAIN_SNAPSHOT_FILE)
    payload = build_payload(signals, onchain)
    if payload["recent_data"]:
        print("最新交易日数据快照：")
        print(json.dumps(payload["recent_data"][-1], ensure_ascii=False, indent=2))
    analysis_text = None
    model_label = ""

    if gemini_key:
        try:
            analysis_text = call_gemini(
                api_key=gemini_key,
                proxy=proxy,
                payload=payload,
            )
            model_label = "Gemini"
            if analysis_text:
                print("使用 Gemini 生成分析。")
            else:
                print("Gemini 返回空响应，尝试回退 DeepSeek。")
                analysis_text = None
        except Exception as exc:
            print(f"Gemini 调用失败：{exc}")

    if analysis_text is None:
        if not deepseek_key:
            raise SystemExit("Gemini 调用失败且未配置 DeepSeek API Key。")
        try:
            analysis_text = call_deepseek(api_key=deepseek_key, proxy=proxy, payload=payload)
            model_label = "DeepSeek"
            print("使用 DeepSeek 生成分析。")
        except Exception as exc:
            raise SystemExit(f"DeepSeek 调用失败：{exc}") from exc

    save_report(payload, analysis_text, Path("model_analysis.md"), model_label or "模型")
    print("分析结果已写入 model_analysis.md")
    save_email_body(analysis_text, Path("model_email_body.md"))


if __name__ == "__main__":
    main()
