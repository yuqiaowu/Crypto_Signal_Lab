from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

import requests

SIGNAL_FILE = Path("signals_60d.json")


def load_signals(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise SystemExit(
            f"未找到 {path}。请先运行 `python 获取数据.py` 生成信号数据，再执行本脚本。"
        )
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_payload(signals: List[Dict[str, Any]]) -> Dict[str, Any]:
    instructions = """
你是一名资深的币圈投资分析师。请基于以下规则严格分析最近60天的 ETH/USDT 日线数据，并给出买入/卖出建议：
1. 识别买入信号时，务必检查布林带下轨斜率是否趋缓或开始向上；若布林带仍陡峭向下，即使出现触碰下轨也需谨慎。
2. 理想买入点应满足：布林带斜率趋缓或向上拐头，同时价格贴近或触碰下轨，并结合 RSI、成交量及关键均线表现进行验证。
3. 综合多个指标，尤其注意 RSI、关键点位突破情况（是否连续3天站上关键均线且放量）、成交量变化，而非单一信号判断。
4. 在形成建议时，请清晰描述你的逻辑，尤其是布林带形态、成交量与均线的配合情况。
5. 卖出信号关注 RSI>70、高位放量、ADX>40 且 +DI>-DI；低位放量作为支撑，高位放量作为压力。
6. 数据中已为每个交易日计算买入/卖出星级（0~3星，分别基于 RSI、放量、DMI 叠加），请结合星级及其他指标作出具体建议，并说明理由。
请输出：
- 对当前市场趋势的综合概述（布林带、均线、量能等）。
- 买入/卖出信号的星级解释（对应日期，说明为何给出该星级，是否符合上述规则）。
- 若存在明显的支撑位/压力位，请给出对应的价格区域。
- 请给出短期（1-2 周）和中期（1-2 月）的操作建议。
- 提醒潜在风险或需要关注的指标变化。
""".strip()

    return {
        "instructions": instructions,
        "recent_data": signals,
    }


def call_gemini(api_key: str, proxy: str | None, payload: Dict[str, Any]) -> str:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
    proxies = {"http": proxy, "https": proxy} if proxy else None
    request_payload = {
        "contents": [
            {
                "parts": [
                    {"text": payload["instructions"]},
                    {"text": "以下是最近60天的信号数据（JSON）：\n" + json.dumps(payload["recent_data"], ensure_ascii=False, indent=2)},
                ]
            }
        ]
    }

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
        f.write("## Gemini 回复\n\n")
        f.write(gemini_text or "(无回复)")


def main() -> None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY 未设置")

    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    signals = load_signals(SIGNAL_FILE)
    payload = build_payload(signals)
    gemini_text = call_gemini(api_key=api_key, proxy=proxy, payload=payload)
    save_report(payload, gemini_text, Path("gemini_analysis.md"))
    print("分析结果已写入 gemini_analysis.md")


if __name__ == "__main__":
    main()
