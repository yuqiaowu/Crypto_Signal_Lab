# neweth
对以太坊的分析

## 快速脚本

- `fetch_onchain_and_news.py`：调用 DeFiLlama（含 datasets 备用源）、Blockchair、mempool.space 及 Etherscan 等开放 API，汇总以太坊/比特币的资金流动、mempool 排队、Gas 费用以及最新新闻。执行 `python fetch_onchain_and_news.py` 后会在项目根目录生成 `global_onchain_news_snapshot.json`。如需获取以太坊 Gas 数据，请在环境变量中设置 `ETHERSCAN_API_KEY`。
- `获取数据.py`：拉取 OKX 日线行情并计算布林带、RSI、DMI、ATR% 等指标。执行 `python 获取数据.py` 会生成信号文件 `signals_60d.json`、波动率数据 `atr_metrics.json` 以及图像 `eth_okx_daily.png`，供模型分析脚本与其它流程引用。
- `model_analysis.py`：优先调用 Gemini（默认 `gemini-2.0-flash`，可通过 `GEMINI_MODEL`/`GEMINI_API_VERSION` 覆盖），若失败则回退到 DeepSeek（`DEEPSEEK_API_KEY`），基于上述数据生成日报 (`model_analysis.md` / `model_email_body.md`)。
