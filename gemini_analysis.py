from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

import requests

SIGNAL_FILE = Path("signals_60d.json")
VOLATILITY_FILE = Path("atr_metrics.json")
ONCHAIN_SNAPSHOT_FILE = Path("global_onchain_news_snapshot.json")


def load_signals(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise SystemExit(
            f"未找到 {path}。请先运行 `python 获取数据.py` 生成信号数据，再执行本脚本。"
        )
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_volatility(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(
            f"未找到 {path}。请先运行 `python 获取数据.py` 生成 ATR 数据，再执行本脚本。"
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
        return {"extra_parts": [], "paragraphs": {}}
    dr = snapshot.get("daily_report", {}) if isinstance(snapshot, dict) else {}
    stable_para = dr.get("stablecoins", {}).get("paragraph")
    bridge_para = dr.get("bridges", {}).get("paragraph")
    fear_para = dr.get("fear_greed", {}).get("paragraph")
    # 新增：Gas / mempool 摘要
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
            f"BTC 手续费 — fastest: {btc_rec.get('fastestFee')}, 30min: {btc_rec.get('halfHourFee')}, 60min: {btc_rec.get('hourFee')}, economy: {btc_rec.get('economyFee')}, min: {btc_rec.get('minimumFee')} sat/vB"
        )
    gas_para = "； ".join(gas_para_parts) if gas_para_parts else None
    news_summary = _summarize_news(snapshot)

    extra_parts = []
    instructions_extra = (
        "请结合以下链上与情绪数据综合判断：稳定币规模及环比变化、主要跨链桥接的 Top N 与总量、比特币恐慌指数、ETH/BTC Gas 与 mempool 变化、当日重要新闻。"
        "输出结论（看多/中性/看空）、关键理由（引用具体数据）、风险提示、并给出短中期（1-2 周 / 1-2 月）操作建议，说明这些链上与新闻信号如何支撑或抵触观点。"
        "若数据缺失或不稳定，请偏保守，并明确不确定性来源。"
    )
    extra_parts.append(instructions_extra)
    if stable_para:
        extra_parts.append("稳定币摘要：" + str(stable_para))
    if bridge_para:
        extra_parts.append("桥接摘要：" + str(bridge_para))
    if fear_para:
        extra_parts.append("恐慌指数摘要：" + str(fear_para))
    if gas_para:
        extra_parts.append("Gas/Mempool 摘要：" + str(gas_para))
    if news_summary:
        extra_parts.append("新闻要点：" + news_summary)
    extra_parts.append("链上快照（JSON）：\n" + json.dumps(snapshot, ensure_ascii=False, indent=2))
    return {
        "extra_parts": extra_parts,
        "paragraphs": {
            "stable": stable_para,
            "bridge": bridge_para,
            "fear": fear_para,
            "gas": gas_para,
            "news": news_summary,
        },
    }


def build_payload(
    signals: List[Dict[str, Any]],
    onchain: Dict[str, Any] | None = None,
    volatility: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    instructions = """
你是一名资深的币圈投资分析师。以下数据仅包含最近60天已收盘的日线，请基于下列规则严格分析，并给出买入/卖出建议：
1. 识别买入信号时，务必检查布林带下轨斜率是否趋缓或开始向上；若布林带仍陡峭向下，即使出现触碰下轨也需谨慎。
2. 理想买入点应满足：布林带斜率趋缓或向上拐头，同时价格贴近或触碰下轨，并结合 RSI、成交量及关键均线表现进行验证。
3. 综合多个指标，尤其注意 RSI、关键点位突破情况（是否连续3天站上关键均线且放量）、成交量变化，而非单一信号判断。
4. 在形成建议时，请清晰描述你的逻辑，尤其是布林带形态、成交量与均线的配合情况。
5. 数据中已为每个交易日计算买入/卖出星级（0~3星，分别基于 RSI、放量、DMI 叠加），请结合星级及其他指标作出具体建议，并说明理由。
6. 请判断是否“有效站上/跌破关键均线”，并给出依据：默认关注 MA20/MA60/MA120/MA180；“有效”的定义为价格至少连续3天在均线之上/之下（可参考 `ma_status.*.stood_above_3` / `ma_status.*.fell_below_3`），同时量能不低于均量（以 `volume_ratio_ma20` 为准；≥1.0 为基本支持，≥1.5 为较强支持）。
请输出：
- 对当前市场趋势的综合概述（布林带、均线、量能等）。
- 买入/卖出信号的星级解释（对应日期，说明为何给出该星级，是否符合上述规则）。
- 若存在明显的支撑位/压力位，请给出对应的价格区域。
- 请给出短期（1-2 周）和中期（1-2 月）的操作建议。
- 提醒潜在风险或需要关注的指标变化。
- 结合 ATR% 的走势说明波动率水平（是否升高/走低），并讨论波动率对策略择时的影响。
- 结合链上资金流（稳定币、桥接）、Gas/Mempool、恐慌指数与新闻要点，说明市场情绪与流动性走向，并评价其对价格趋势的支撑或掣肘。
""".strip()

    payload: Dict[str, Any] = {
        "instructions": instructions,
        "recent_data": signals,
        "extra_parts": [],
    }
    if onchain:
        oc = build_onchain_parts(onchain)
        payload["extra_parts"].extend(oc.get("extra_parts", []))
        payload["onchain_paragraphs"] = oc.get("paragraphs", {})
    if volatility:
        payload["volatility"] = volatility
        payload["extra_parts"].append(
            "以下是 ATR 波动率数据（JSON）：\n" + json.dumps(volatility, ensure_ascii=False, indent=2)
        )
    return payload


def call_gemini(api_key: str, proxy: str | None, payload: Dict[str, Any]) -> str:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
    proxies = {"http": proxy, "https": proxy} if proxy else None
    parts = [
        {"text": payload["instructions"]},
        {"text": "以下是最近60天的信号数据（JSON）：\n" + json.dumps(payload["recent_data"], ensure_ascii=False, indent=2)},
    ]
    for extra in payload.get("extra_parts", []):
        parts.append({"text": str(extra)})
    request_payload = {"contents": [{"parts": parts}]}

    response = requests.post(
        url,
        params={"key": api_key},
        json=request_payload,
        proxies=proxies,
        timeout=120,
    )
    if response.status_code == 429:
        raise SystemExit("Gemini API 返回 429（请求过多）。请稍后再试或检查配额。")
    response.raise_for_status()

    result = response.json()
    text_parts: List[str] = []
    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            text = part.get("text")
            if text:
                text_parts.append(text)
    return "\n".join(text_parts).strip()


def save_report(payload: Dict[str, Any], gemini_text: str, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write("# Gemini 分析报告\n\n")
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
        if payload.get("extra_parts"):
            f.write("\n## 链上快照 (JSON)\n\n")
            onchain_json = next((p for p in payload["extra_parts"] if str(p).startswith("链上快照（JSON）：")), None)
            if onchain_json:
                content = str(onchain_json).split("链上快照（JSON）：", 1)[1]
                f.write("```json\n" + content + "\n```\n\n")
        if payload.get("volatility"):
            f.write("## ATR 波动率数据 (JSON)\n\n")
            f.write("```json\n" + json.dumps(payload["volatility"], ensure_ascii=False, indent=2) + "\n```\n\n")
        f.write("## Gemini 回复\n\n")
        f.write(gemini_text or "(无回复)")


def save_email_body(gemini_text: str, path: Path) -> None:
    body = (gemini_text or "").strip() or "(无回复)"
    with path.open("w", encoding="utf-8") as f:
        f.write(body)


def main() -> None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY 未设置")

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
    volatility = load_volatility(VOLATILITY_FILE)
    onchain = load_onchain_snapshot(ONCHAIN_SNAPSHOT_FILE)
    payload = build_payload(signals, onchain, volatility)
    gemini_text = call_gemini(api_key=api_key, proxy=proxy, payload=payload)
    save_report(payload, gemini_text, Path("gemini_analysis.md"))
    print("分析结果已写入 gemini_analysis.md")
    # 假设已有变量 gemini_text 与 payload，并已写入 gemini_analysis.md
    # 这里追加生成仅用于邮件正文的文件（不包含JSON与提示词）
    save_email_body(gemini_text, Path("gemini_email_body.md"))


if __name__ == "__main__":
    main()
