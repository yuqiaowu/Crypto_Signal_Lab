# Gemini 分析报告

## 提示内容

你是一名资深的币圈投资分析师。以下数据仅包含最近60天已收盘的日线，请基于下列规则严格分析，并给出买入/卖出建议：
1. 识别买入信号时，务必检查布林带下轨斜率是否趋缓或开始向上；若布林带仍陡峭向下，即使出现触碰下轨也需谨慎。
2. 理想买入点应满足：布林带斜率趋缓或向上拐头，同时价格贴近或触碰下轨，并结合 RSI、成交量及关键均线表现进行验证。
3. 综合多个指标，尤其注意 RSI、关键点位突破情况（是否连续3天站上关键均线且放量）、成交量变化，而非单一信号判断。
4. 在形成建议时，请清晰描述你的逻辑，尤其是布林带形态、成交量与均线的配合情况。
5. 数据中已为每个交易日计算买入/卖出星级（0~3星，分别基于 RSI、放量、DMI 叠加），请结合星级及其他指标作出具体建议，并说明理由。
6. 请判断是否“有效站上/跌破关键均线”，并给出依据：默认关注 MA20/MA60/MA120/MA180；“有效”的定义为价格至少连续3天在均线之上/之下，同时量能不低于均量（以 `volume_ratio_ma20` 为准；≥1.0 为基本支持，≥1.5 为较强支持）。
7. `recent_data` 按时间顺序排列，请务必以最后一条记录视为最新收盘日，并据此判断当前市场状态。
8. 已额外提供 `latest_ma_relation` 字段，标明最新收盘价相对各条均线的位置（above / below / both / unknown），请在分析中引用该字段验证你的判断。
请输出：
- 按以下标题输出详细内容（无须额外说明）：
  1. 《市场概述》——布林带、均线、量能综合评价。
  2. 《信号解读》——列出买入/卖出星级及理由，指明是否符合规则。
  3. 《关键价位》——若存在重要支撑/压力，请给出现价或区间。
  4. 《操作建议》——分别给出短期（1-2 周）与中期（1-2 月）策略。
  5. 《风险与关注》——提示潜在风险以及需要观测的指标变化。
  6. 《波动率观察》——解析 ATR% 的趋势与对策略的影响。
  7. 《链上与情绪》——分别引用稳定币、桥接、Gas/Mempool、恐慌指数、新闻数据以及衍生品指标（OKX 永续开仓量与多空爆仓）的具体数值，分析其含义及对价格/策略的影响；如某项缺失须说明原因。

## 最近60天信号数据 (JSON)

```json
[
  {
    "date": "2025-08-29",
    "close": 4360.71,
    "volume": 231691.15,
    "volume_ratio_ma20": 0.92,
    "price_percentile_20": 0.35,
    "rsi14": 52.01,
    "bb_lower": 4062.12,
    "bb_lower_slope": 0.3104,
    "atr_pct_14": 5.929,
    "ma_5": 4471.33,
    "ma_10": 4530.95,
    "ma_20": 4469.77,
    "ma_60": 3717.77,
    "ma_120": 3086.48,
    "ma_180": 2670.06,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-08-30",
    "close": 4374.56,
    "volume": 98026.89,
    "volume_ratio_ma20": 0.39,
    "price_percentile_20": 0.35,
    "rsi14": 52.34,
    "bb_lower": 4078.1,
    "bb_lower_slope": 0.3934,
    "atr_pct_14": 5.747,
    "ma_5": 4470.9,
    "ma_10": 4534.78,
    "ma_20": 4475.94,
    "ma_60": 3750.6,
    "ma_120": 3107.58,
    "ma_180": 2682.43,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-08-31",
    "close": 4391.91,
    "volume": 108257.86,
    "volume_ratio_ma20": 0.45,
    "price_percentile_20": 0.4,
    "rsi14": 52.78,
    "bb_lower": 4101.36,
    "bb_lower_slope": 0.5704,
    "atr_pct_14": 5.52,
    "ma_5": 4429.2,
    "ma_10": 4551.38,
    "ma_20": 4484.36,
    "ma_60": 3780.95,
    "ma_120": 3128.9,
    "ma_180": 2694.76,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-01",
    "close": 4314.59,
    "volume": 155657.37,
    "volume_ratio_ma20": 0.67,
    "price_percentile_20": 0.2,
    "rsi14": 50.53,
    "bb_lower": 4083.99,
    "bb_lower_slope": -0.4236,
    "atr_pct_14": 5.682,
    "ma_5": 4390.69,
    "ma_10": 4499.68,
    "ma_20": 4470.58,
    "ma_60": 3809.68,
    "ma_120": 3149.78,
    "ma_180": 2706.28,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-02",
    "close": 4326.7,
    "volume": 179977.59,
    "volume_ratio_ma20": 0.8,
    "price_percentile_20": 0.25,
    "rsi14": 50.89,
    "bb_lower": 4080.37,
    "bb_lower_slope": -0.0885,
    "atr_pct_14": 5.524,
    "ma_5": 4353.69,
    "ma_10": 4454.47,
    "ma_20": 4449.41,
    "ma_60": 3839.99,
    "ma_120": 3170.67,
    "ma_180": 2718.08,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-03",
    "close": 4450.28,
    "volume": 129027.84,
    "volume_ratio_ma20": 0.62,
    "price_percentile_20": 0.65,
    "rsi14": 54.45,
    "bb_lower": 4078.25,
    "bb_lower_slope": -0.052,
    "atr_pct_14": 5.319,
    "ma_5": 4371.61,
    "ma_10": 4421.47,
    "ma_20": 4444.59,
    "ma_60": 3872.23,
    "ma_120": 3192.61,
    "ma_180": 2730.9,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-04",
    "close": 4297.61,
    "volume": 157913.09,
    "volume_ratio_ma20": 0.77,
    "price_percentile_20": 0.15,
    "rsi14": 49.65,
    "bb_lower": 4065.59,
    "bb_lower_slope": -0.3105,
    "atr_pct_14": 5.477,
    "ma_5": 4356.22,
    "ma_10": 4413.56,
    "ma_20": 4437.5,
    "ma_60": 3901.01,
    "ma_120": 3213.34,
    "ma_180": 2742.54,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-05",
    "close": 4307.36,
    "volume": 225419.23,
    "volume_ratio_ma20": 1.07,
    "price_percentile_20": 0.2,
    "rsi14": 49.96,
    "bb_lower": 4055.55,
    "bb_lower_slope": -0.247,
    "atr_pct_14": 5.469,
    "ma_5": 4339.31,
    "ma_10": 4384.25,
    "ma_20": 4431.75,
    "ma_60": 3930.43,
    "ma_120": 3230.84,
    "ma_180": 2755.24,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-06",
    "close": 4273.68,
    "volume": 64821.15,
    "volume_ratio_ma20": 0.31,
    "price_percentile_20": 0.15,
    "rsi14": 48.86,
    "bb_lower": 4039.97,
    "bb_lower_slope": -0.3842,
    "atr_pct_14": 5.277,
    "ma_5": 4331.13,
    "ma_10": 4360.91,
    "ma_20": 4421.79,
    "ma_60": 3958.07,
    "ma_120": 3246.91,
    "ma_180": 2768.62,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-07",
    "close": 4306.14,
    "volume": 50963.28,
    "volume_ratio_ma20": 0.26,
    "price_percentile_20": 0.25,
    "rsi14": 50.0,
    "bb_lower": 4039.12,
    "bb_lower_slope": -0.0208,
    "atr_pct_14": 4.973,
    "ma_5": 4327.01,
    "ma_10": 4340.35,
    "ma_20": 4421.4,
    "ma_60": 3983.69,
    "ma_120": 3261.27,
    "ma_180": 2781.86,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-08",
    "close": 4305.99,
    "volume": 122893.61,
    "volume_ratio_ma20": 0.66,
    "price_percentile_20": 0.2,
    "rsi14": 49.99,
    "bb_lower": 4080.26,
    "bb_lower_slope": 1.0183,
    "atr_pct_14": 4.792,
    "ma_5": 4298.16,
    "ma_10": 4334.88,
    "ma_20": 4432.92,
    "ma_60": 4006.28,
    "ma_120": 3276.2,
    "ma_180": 2795.18,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-09",
    "close": 4310.31,
    "volume": 136936.79,
    "volume_ratio_ma20": 0.76,
    "price_percentile_20": 0.35,
    "rsi14": 50.17,
    "bb_lower": 4077.36,
    "bb_lower_slope": -0.071,
    "atr_pct_14": 4.619,
    "ma_5": 4300.7,
    "ma_10": 4328.46,
    "ma_20": 4431.62,
    "ma_60": 4028.81,
    "ma_120": 3291.32,
    "ma_180": 2808.77,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-10",
    "close": 4349.98,
    "volume": 159255.1,
    "volume_ratio_ma20": 0.89,
    "price_percentile_20": 0.45,
    "rsi14": 51.8,
    "bb_lower": 4093.99,
    "bb_lower_slope": 0.408,
    "atr_pct_14": 4.526,
    "ma_5": 4309.22,
    "ma_10": 4324.26,
    "ma_20": 4437.82,
    "ma_60": 4052.25,
    "ma_120": 3305.24,
    "ma_180": 2822.31,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-11",
    "close": 4458.66,
    "volume": 151311.67,
    "volume_ratio_ma20": 0.91,
    "price_percentile_20": 0.75,
    "rsi14": 56.04,
    "bb_lower": 4126.09,
    "bb_lower_slope": 0.7839,
    "atr_pct_14": 4.33,
    "ma_5": 4346.22,
    "ma_10": 4338.67,
    "ma_20": 4419.17,
    "ma_60": 4077.03,
    "ma_120": 3320.65,
    "ma_180": 2836.32,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-12",
    "close": 4712.51,
    "volume": 179102.56,
    "volume_ratio_ma20": 1.07,
    "price_percentile_20": 0.95,
    "rsi14": 64.02,
    "bb_lower": 4138.0,
    "bb_lower_slope": 0.2888,
    "atr_pct_14": 4.265,
    "ma_5": 4427.49,
    "ma_10": 4377.25,
    "ma_20": 4415.86,
    "ma_60": 4105.34,
    "ma_120": 3338.68,
    "ma_180": 2852.02,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-13",
    "close": 4667.2,
    "volume": 131477.17,
    "volume_ratio_ma20": 0.83,
    "price_percentile_20": 0.95,
    "rsi14": 61.86,
    "bb_lower": 4158.91,
    "bb_lower_slope": 0.5054,
    "atr_pct_14": 4.245,
    "ma_5": 4499.73,
    "ma_10": 4398.94,
    "ma_20": 4410.21,
    "ma_60": 4130.83,
    "ma_120": 3356.43,
    "ma_180": 2867.24,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-14",
    "close": 4604.52,
    "volume": 113474.54,
    "volume_ratio_ma20": 0.76,
    "price_percentile_20": 0.9,
    "rsi14": 58.9,
    "bb_lower": 4157.1,
    "bb_lower_slope": -0.0435,
    "atr_pct_14": 4.177,
    "ma_5": 4558.57,
    "ma_10": 4429.64,
    "ma_20": 4421.6,
    "ma_60": 4151.39,
    "ma_120": 3374.17,
    "ma_180": 2882.09,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-15",
    "close": 4523.2,
    "volume": 153338.01,
    "volume_ratio_ma20": 1.06,
    "price_percentile_20": 0.85,
    "rsi14": 55.22,
    "bb_lower": 4161.68,
    "bb_lower_slope": 0.11,
    "atr_pct_14": 4.272,
    "ma_5": 4593.22,
    "ma_10": 4451.22,
    "ma_20": 4417.74,
    "ma_60": 4168.82,
    "ma_120": 3391.05,
    "ma_180": 2895.8,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-16",
    "close": 4501.28,
    "volume": 169489.25,
    "volume_ratio_ma20": 1.18,
    "price_percentile_20": 0.75,
    "rsi14": 54.23,
    "bb_lower": 4161.78,
    "bb_lower_slope": 0.0025,
    "atr_pct_14": 4.168,
    "ma_5": 4601.74,
    "ma_10": 4473.98,
    "ma_20": 4417.44,
    "ma_60": 4184.73,
    "ma_120": 3407.49,
    "ma_180": 2909.78,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-17",
    "close": 4589.95,
    "volume": 214871.29,
    "volume_ratio_ma20": 1.46,
    "price_percentile_20": 0.85,
    "rsi14": 57.53,
    "bb_lower": 4157.77,
    "bb_lower_slope": -0.0964,
    "atr_pct_14": 4.122,
    "ma_5": 4577.23,
    "ma_10": 4502.36,
    "ma_20": 4421.36,
    "ma_60": 4201.36,
    "ma_120": 3424.71,
    "ma_180": 2924.36,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-18",
    "close": 4587.6,
    "volume": 113217.61,
    "volume_ratio_ma20": 0.8,
    "price_percentile_20": 0.8,
    "rsi14": 57.41,
    "bb_lower": 4161.12,
    "bb_lower_slope": 0.0806,
    "atr_pct_14": 3.972,
    "ma_5": 4561.31,
    "ma_10": 4530.52,
    "ma_20": 4432.7,
    "ma_60": 4215.2,
    "ma_120": 3441.68,
    "ma_180": 2938.84,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-19",
    "close": 4469.09,
    "volume": 114653.56,
    "volume_ratio_ma20": 0.81,
    "price_percentile_20": 0.65,
    "rsi14": 51.65,
    "bb_lower": 4166.77,
    "bb_lower_slope": 0.1358,
    "atr_pct_14": 4.083,
    "ma_5": 4534.22,
    "ma_10": 4546.4,
    "ma_20": 4437.43,
    "ma_60": 4226.97,
    "ma_120": 3456.71,
    "ma_180": 2952.53,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-20",
    "close": 4480.6,
    "volume": 44422.64,
    "volume_ratio_ma20": 0.32,
    "price_percentile_20": 0.65,
    "rsi14": 52.15,
    "bb_lower": 4171.43,
    "bb_lower_slope": 0.1118,
    "atr_pct_14": 3.868,
    "ma_5": 4525.7,
    "ma_10": 4559.46,
    "ma_20": 4441.86,
    "ma_60": 4239.21,
    "ma_120": 3473.0,
    "ma_180": 2965.86,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-21",
    "close": 4445.4,
    "volume": 70634.76,
    "volume_ratio_ma20": 0.53,
    "price_percentile_20": 0.45,
    "rsi14": 50.43,
    "bb_lower": 4184.35,
    "bb_lower_slope": 0.3097,
    "atr_pct_14": 3.708,
    "ma_5": 4514.53,
    "ma_10": 4558.14,
    "ma_20": 4448.4,
    "ma_60": 4252.82,
    "ma_120": 3488.96,
    "ma_180": 2979.07,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-22",
    "close": 4198.87,
    "volume": 329311.78,
    "volume_ratio_ma20": 2.33,
    "price_percentile_20": 0.05,
    "rsi14": 40.36,
    "bb_lower": 4160.85,
    "bb_lower_slope": -0.5616,
    "atr_pct_14": 4.345,
    "ma_5": 4436.31,
    "ma_10": 4506.77,
    "ma_20": 4442.01,
    "ma_60": 4261.01,
    "ma_120": 3502.69,
    "ma_180": 2991.24,
    "buy_stars": 1,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": true,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-23",
    "close": 4164.28,
    "volume": 115254.66,
    "volume_ratio_ma20": 0.82,
    "price_percentile_20": 0.05,
    "rsi14": 39.17,
    "bb_lower": 4121.69,
    "bb_lower_slope": -0.9411,
    "atr_pct_14": 4.264,
    "ma_5": 4351.65,
    "ma_10": 4456.48,
    "ma_20": 4427.71,
    "ma_60": 4268.34,
    "ma_120": 3516.02,
    "ma_180": 3003.24,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-24",
    "close": 4152.25,
    "volume": 125544.17,
    "volume_ratio_ma20": 0.9,
    "price_percentile_20": 0.05,
    "rsi14": 38.75,
    "bb_lower": 4096.05,
    "bb_lower_slope": -0.622,
    "atr_pct_14": 4.2,
    "ma_5": 4288.28,
    "ma_10": 4411.25,
    "ma_20": 4420.44,
    "ma_60": 4275.18,
    "ma_120": 3528.45,
    "ma_180": 3015.77,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-25",
    "close": 3874.19,
    "volume": 333334.39,
    "volume_ratio_ma20": 2.3,
    "price_percentile_20": 0.05,
    "rsi14": 30.51,
    "bb_lower": 3998.19,
    "bb_lower_slope": -2.3891,
    "atr_pct_14": 4.802,
    "ma_5": 4167.0,
    "ma_10": 4346.35,
    "ma_20": 4398.78,
    "ma_60": 4275.2,
    "ma_120": 3538.39,
    "ma_180": 3027.14,
    "buy_stars": 1,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": true,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-26",
    "close": 4032.28,
    "volume": 213160.44,
    "volume_ratio_ma20": 1.4,
    "price_percentile_20": 0.1,
    "rsi14": 38.51,
    "bb_lower": 3958.2,
    "bb_lower_slope": -1.0003,
    "atr_pct_14": 4.643,
    "ma_5": 4084.37,
    "ma_10": 4299.45,
    "ma_20": 4386.72,
    "ma_60": 4279.1,
    "ma_120": 3550.06,
    "ma_180": 3039.49,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-27",
    "close": 4019.0,
    "volume": 65761.17,
    "volume_ratio_ma20": 0.43,
    "price_percentile_20": 0.1,
    "rsi14": 38.12,
    "bb_lower": 3915.69,
    "bb_lower_slope": -1.074,
    "atr_pct_14": 4.444,
    "ma_5": 4048.4,
    "ma_10": 4242.36,
    "ma_20": 4372.36,
    "ma_60": 4282.85,
    "ma_120": 3562.46,
    "ma_180": 3051.7,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-28",
    "close": 4141.48,
    "volume": 84384.33,
    "volume_ratio_ma20": 0.56,
    "price_percentile_20": 0.2,
    "rsi14": 43.87,
    "bb_lower": 3897.17,
    "bb_lower_slope": -0.473,
    "atr_pct_14": 4.313,
    "ma_5": 4043.84,
    "ma_10": 4197.74,
    "ma_20": 4364.13,
    "ma_60": 4288.37,
    "ma_120": 3575.9,
    "ma_180": 3064.12,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-29",
    "close": 4214.75,
    "volume": 123246.69,
    "volume_ratio_ma20": 0.82,
    "price_percentile_20": 0.4,
    "rsi14": 47.04,
    "bb_lower": 3888.35,
    "bb_lower_slope": -0.2263,
    "atr_pct_14": 4.197,
    "ma_5": 4056.34,
    "ma_10": 4172.31,
    "ma_20": 4359.35,
    "ma_60": 4296.97,
    "ma_120": 3589.87,
    "ma_180": 3077.56,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-09-30",
    "close": 4145.3,
    "volume": 129502.12,
    "volume_ratio_ma20": 0.87,
    "price_percentile_20": 0.25,
    "rsi14": 44.47,
    "bb_lower": 3868.94,
    "bb_lower_slope": -0.4992,
    "atr_pct_14": 4.228,
    "ma_5": 4110.56,
    "ma_10": 4138.78,
    "ma_20": 4349.12,
    "ma_60": 4307.93,
    "ma_120": 3602.68,
    "ma_180": 3090.5,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-01",
    "close": 4348.31,
    "volume": 162375.29,
    "volume_ratio_ma20": 1.09,
    "price_percentile_20": 0.5,
    "rsi14": 52.61,
    "bb_lower": 3866.05,
    "bb_lower_slope": -0.0746,
    "atr_pct_14": 4.125,
    "ma_5": 4173.77,
    "ma_10": 4129.07,
    "ma_20": 4343.6,
    "ma_60": 4323.83,
    "ma_120": 3617.31,
    "ma_180": 3104.56,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-02",
    "close": 4484.64,
    "volume": 156773.91,
    "volume_ratio_ma20": 1.06,
    "price_percentile_20": 0.7,
    "rsi14": 57.15,
    "bb_lower": 3880.22,
    "bb_lower_slope": 0.3664,
    "atr_pct_14": 4.008,
    "ma_5": 4266.9,
    "ma_10": 4157.65,
    "ma_20": 4332.21,
    "ma_60": 4340.29,
    "ma_120": 3632.94,
    "ma_180": 3119.44,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-03",
    "close": 4512.79,
    "volume": 183470.5,
    "volume_ratio_ma20": 1.22,
    "price_percentile_20": 0.8,
    "rsi14": 58.04,
    "bb_lower": 3890.75,
    "bb_lower_slope": 0.2712,
    "atr_pct_14": 3.958,
    "ma_5": 4341.16,
    "ma_10": 4192.5,
    "ma_20": 4324.49,
    "ma_60": 4353.48,
    "ma_120": 3650.43,
    "ma_180": 3135.73,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-04",
    "close": 4487.62,
    "volume": 62184.12,
    "volume_ratio_ma20": 0.42,
    "price_percentile_20": 0.75,
    "rsi14": 56.9,
    "bb_lower": 3897.18,
    "bb_lower_slope": 0.1653,
    "atr_pct_14": 3.82,
    "ma_5": 4395.73,
    "ma_10": 4226.04,
    "ma_20": 4318.64,
    "ma_60": 4368.07,
    "ma_120": 3667.19,
    "ma_180": 3152.03,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-05",
    "close": 4514.63,
    "volume": 151380.97,
    "volume_ratio_ma20": 1.02,
    "price_percentile_20": 0.9,
    "rsi14": 57.86,
    "bb_lower": 3897.56,
    "bb_lower_slope": 0.0099,
    "atr_pct_14": 3.766,
    "ma_5": 4469.6,
    "ma_10": 4290.08,
    "ma_20": 4318.22,
    "ma_60": 4381.93,
    "ma_120": 3683.77,
    "ma_180": 3168.93,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-06",
    "close": 4684.25,
    "volume": 151988.37,
    "volume_ratio_ma20": 1.03,
    "price_percentile_20": 1.0,
    "rsi14": 63.37,
    "bb_lower": 3883.85,
    "bb_lower_slope": -0.3519,
    "atr_pct_14": 3.75,
    "ma_5": 4536.79,
    "ma_10": 4355.28,
    "ma_20": 4327.36,
    "ma_60": 4394.84,
    "ma_120": 3701.9,
    "ma_180": 3185.68,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-07",
    "close": 4447.3,
    "volume": 247667.22,
    "volume_ratio_ma20": 1.66,
    "price_percentile_20": 0.6,
    "rsi14": 52.95,
    "bb_lower": 3889.43,
    "bb_lower_slope": 0.1437,
    "atr_pct_14": 4.192,
    "ma_5": 4529.32,
    "ma_10": 4398.11,
    "ma_20": 4320.23,
    "ma_60": 4402.12,
    "ma_120": 3716.62,
    "ma_180": 3201.93,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-08",
    "close": 4525.98,
    "volume": 156263.86,
    "volume_ratio_ma20": 1.03,
    "price_percentile_20": 0.95,
    "rsi14": 55.56,
    "bb_lower": 3893.22,
    "bb_lower_slope": 0.0973,
    "atr_pct_14": 4.056,
    "ma_5": 4531.96,
    "ma_10": 4436.56,
    "ma_20": 4317.15,
    "ma_60": 4406.54,
    "ma_120": 3730.87,
    "ma_180": 3218.37,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-09",
    "close": 4368.2,
    "volume": 190012.02,
    "volume_ratio_ma20": 1.23,
    "price_percentile_20": 0.55,
    "rsi14": 49.61,
    "bb_lower": 3893.15,
    "bb_lower_slope": -0.0017,
    "atr_pct_14": 4.339,
    "ma_5": 4508.07,
    "ma_10": 4451.9,
    "ma_20": 4312.11,
    "ma_60": 4408.49,
    "ma_120": 3744.18,
    "ma_180": 3233.5,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-10",
    "close": 3822.49,
    "volume": 658288.47,
    "volume_ratio_ma20": 3.55,
    "price_percentile_20": 0.05,
    "rsi14": 35.47,
    "bb_lower": 3817.18,
    "bb_lower_slope": -1.9513,
    "atr_pct_14": 6.51,
    "ma_5": 4369.64,
    "ma_10": 4419.62,
    "ma_20": 4279.2,
    "ma_60": 4401.81,
    "ma_120": 3754.01,
    "ma_180": 3245.86,
    "buy_stars": 1,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": true,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-11",
    "close": 3747.38,
    "volume": 363695.02,
    "volume_ratio_ma20": 1.82,
    "price_percentile_20": 0.05,
    "rsi14": 34.03,
    "bb_lower": 3734.76,
    "bb_lower_slope": -2.1593,
    "atr_pct_14": 6.616,
    "ma_5": 4182.27,
    "ma_10": 4359.53,
    "ma_20": 4244.3,
    "ma_60": 4387.76,
    "ma_120": 3763.74,
    "ma_180": 3257.66,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_120": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-12",
    "close": 4152.11,
    "volume": 358028.25,
    "volume_ratio_ma20": 1.78,
    "price_percentile_20": 0.4,
    "rsi14": 46.6,
    "bb_lower": 3731.18,
    "bb_lower_slope": -0.0958,
    "atr_pct_14": 6.41,
    "ma_5": 4123.23,
    "ma_10": 4326.27,
    "ma_20": 4241.96,
    "ma_60": 4377.8,
    "ma_120": 3777.25,
    "ma_180": 3271.9,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-13",
    "close": 4241.8,
    "volume": 251817.62,
    "volume_ratio_ma20": 1.21,
    "price_percentile_20": 0.55,
    "rsi14": 48.92,
    "bb_lower": 3736.3,
    "bb_lower_slope": 0.1372,
    "atr_pct_14": 6.25,
    "ma_5": 4066.4,
    "ma_10": 4299.18,
    "ma_20": 4245.84,
    "ma_60": 4372.71,
    "ma_120": 3791.37,
    "ma_180": 3286.7,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-14",
    "close": 4124.95,
    "volume": 445067.93,
    "volume_ratio_ma20": 1.98,
    "price_percentile_20": 0.3,
    "rsi14": 46.11,
    "bb_lower": 3733.8,
    "bb_lower_slope": -0.0671,
    "atr_pct_14": 6.618,
    "ma_5": 4017.75,
    "ma_10": 4262.91,
    "ma_20": 4244.47,
    "ma_60": 4367.47,
    "ma_120": 3804.54,
    "ma_180": 3300.82,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-15",
    "close": 3986.15,
    "volume": 274557.02,
    "volume_ratio_ma20": 1.24,
    "price_percentile_20": 0.15,
    "rsi14": 42.95,
    "bb_lower": 3753.49,
    "bb_lower_slope": 0.5275,
    "atr_pct_14": 6.882,
    "ma_5": 4050.48,
    "ma_10": 4210.06,
    "ma_20": 4250.07,
    "ma_60": 4360.2,
    "ma_120": 3816.85,
    "ma_180": 3314.14,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-16",
    "close": 3894.62,
    "volume": 268946.62,
    "volume_ratio_ma20": 1.2,
    "price_percentile_20": 0.15,
    "rsi14": 40.95,
    "bb_lower": 3731.15,
    "bb_lower_slope": -0.5953,
    "atr_pct_14": 7.02,
    "ma_5": 4079.93,
    "ma_10": 4131.1,
    "ma_20": 4243.19,
    "ma_60": 4350.56,
    "ma_120": 3828.26,
    "ma_180": 3326.81,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-17",
    "close": 3831.88,
    "volume": 314619.36,
    "volume_ratio_ma20": 1.33,
    "price_percentile_20": 0.15,
    "rsi14": 39.6,
    "bb_lower": 3699.4,
    "bb_lower_slope": -0.8509,
    "atr_pct_14": 7.141,
    "ma_5": 4015.88,
    "ma_10": 4069.56,
    "ma_20": 4233.83,
    "ma_60": 4342.53,
    "ma_120": 3839.19,
    "ma_180": 3339.28,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-18",
    "close": 3888.96,
    "volume": 94143.0,
    "volume_ratio_ma20": 0.4,
    "price_percentile_20": 0.2,
    "rsi14": 41.5,
    "bb_lower": 3667.08,
    "bb_lower_slope": -0.8738,
    "atr_pct_14": 6.734,
    "ma_5": 3945.31,
    "ma_10": 4005.85,
    "ma_20": 4221.21,
    "ma_60": 4339.42,
    "ma_120": 3851.54,
    "ma_180": 3352.11,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-19",
    "close": 3982.74,
    "volume": 183062.66,
    "volume_ratio_ma20": 0.76,
    "price_percentile_20": 0.3,
    "rsi14": 44.58,
    "bb_lower": 3645.79,
    "bb_lower_slope": -0.5804,
    "atr_pct_14": 6.481,
    "ma_5": 3916.87,
    "ma_10": 3967.31,
    "ma_20": 4209.61,
    "ma_60": 4333.53,
    "ma_120": 3865.6,
    "ma_180": 3364.48,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-20",
    "close": 3979.43,
    "volume": 183200.97,
    "volume_ratio_ma20": 0.75,
    "price_percentile_20": 0.3,
    "rsi14": 44.49,
    "bb_lower": 3629.14,
    "bb_lower_slope": -0.4567,
    "atr_pct_14": 6.341,
    "ma_5": 3915.53,
    "ma_10": 3983.0,
    "ma_20": 4201.31,
    "ma_60": 4329.42,
    "ma_120": 3880.2,
    "ma_180": 3376.61,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-21",
    "close": 3873.09,
    "volume": 247841.11,
    "volume_ratio_ma20": 1.0,
    "price_percentile_20": 0.2,
    "rsi14": 41.61,
    "bb_lower": 3592.45,
    "bb_lower_slope": -1.0111,
    "atr_pct_14": 6.547,
    "ma_5": 3911.22,
    "ma_10": 3995.57,
    "ma_20": 4177.55,
    "ma_60": 4313.44,
    "ma_120": 3892.38,
    "ma_180": 3388.3,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-22",
    "close": 3805.43,
    "volume": 221778.19,
    "volume_ratio_ma20": 0.89,
    "price_percentile_20": 0.1,
    "rsi14": 39.85,
    "bb_lower": 3554.89,
    "bb_lower_slope": -1.0454,
    "atr_pct_14": 6.53,
    "ma_5": 3905.93,
    "ma_10": 3960.91,
    "ma_20": 4143.59,
    "ma_60": 4297.22,
    "ma_120": 3903.69,
    "ma_180": 3399.53,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-23",
    "close": 3857.38,
    "volume": 154748.54,
    "volume_ratio_ma20": 0.62,
    "price_percentile_20": 0.25,
    "rsi14": 41.89,
    "bb_lower": 3535.15,
    "bb_lower_slope": -0.5552,
    "atr_pct_14": 6.24,
    "ma_5": 3899.61,
    "ma_10": 3922.46,
    "ma_20": 4110.82,
    "ma_60": 4281.84,
    "ma_120": 3915.68,
    "ma_180": 3410.84,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_10": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": true
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-24",
    "close": 3935.2,
    "volume": 152529.37,
    "volume_ratio_ma20": 0.6,
    "price_percentile_20": 0.45,
    "rsi14": 44.9,
    "bb_lower": 3529.92,
    "bb_lower_slope": -0.1479,
    "atr_pct_14": 6.014,
    "ma_5": 3890.11,
    "ma_10": 3903.49,
    "ma_20": 4083.2,
    "ma_60": 4274.48,
    "ma_120": 3928.33,
    "ma_180": 3422.75,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-25",
    "close": 3953.94,
    "volume": 41624.94,
    "volume_ratio_ma20": 0.17,
    "price_percentile_20": 0.5,
    "rsi14": 45.63,
    "bb_lower": 3536.43,
    "bb_lower_slope": 0.1843,
    "atr_pct_14": 5.661,
    "ma_5": 3885.01,
    "ma_10": 3900.27,
    "ma_20": 4055.16,
    "ma_60": 4263.71,
    "ma_120": 3941.09,
    "ma_180": 3434.72,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-26",
    "close": 4159.27,
    "volume": 118807.67,
    "volume_ratio_ma20": 0.48,
    "price_percentile_20": 0.8,
    "rsi14": 52.99,
    "bb_lower": 3593.78,
    "bb_lower_slope": 1.6216,
    "atr_pct_14": 5.448,
    "ma_5": 3942.24,
    "ma_10": 3926.73,
    "ma_20": 4028.91,
    "ma_60": 4257.91,
    "ma_120": 3955.45,
    "ma_180": 3447.84,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": true,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  },
  {
    "date": "2025-10-27",
    "close": 4120.39,
    "volume": 178487.4,
    "volume_ratio_ma20": 0.73,
    "price_percentile_20": 0.7,
    "rsi14": 51.56,
    "bb_lower": 3618.94,
    "bb_lower_slope": 0.7003,
    "atr_pct_14": 5.384,
    "ma_5": 4005.24,
    "ma_10": 3955.58,
    "ma_20": 4012.57,
    "ma_60": 4251.39,
    "ma_120": 3968.95,
    "ma_180": 3460.77,
    "buy_stars": 0,
    "sell_stars": 0,
    "signals": {
      "rsi_oversold": false,
      "rsi_overbought": false,
      "low_price_high_vol": false,
      "high_price_high_vol": false,
      "adx_down": false,
      "adx_up": false
    },
    "ma_status": {
      "ma_5": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_10": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_20": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_60": {
        "above": false,
        "below": true,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_120": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_180": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_200": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_250": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      },
      "ma_360": {
        "above": true,
        "below": false,
        "stood_above_3": false,
        "fell_below_3": false
      }
    }
  }
]
```

## 链上数据摘要

- 稳定币：稳定币 — ETH 最新: 162,322,904,029.82 USD，环比: -249,485,898.18 USD / -0.15%； 前值 162,572,389,928.00 USD。
- 桥接：24h 跨链资金流 — ETH 994,451,642 USD, BTC 86,058,409 USD； ETH Top Bridges: USDT0: 186,994,219.9220644, LayerZero: 181,257,789.62229735, Circle CCTP: 95,712,351.26313002, Relay: 70,083,493.0, Chainlink CCIP: 65,145,497.01518885
- 恐慌指数：BTC 恐慌指数 — 最新值: 51.0, 分类: Neutral (近 15 天)。
- Gas/Mempool：BTC Mempool 建议费率: 最低 1 sat/vB, 经济 1 sat/vB, 正常 None sat/vB, 优先 None sat/vB

## 链上快照 (JSON)

## Gemini 回复

## 《市场概述》

当前市场整体呈现震荡上行趋势但伴随较大风险。布林带方面，虽然价格有所回升，但布林带下轨的斜率在大部分时间里仍然向下，表明潜在的下行压力依然存在。均线方面，价格站上MA5/MA10/MA20，但未能有效站稳MA60之上，中长期趋势不明朗。量能方面，近期成交量普遍低于20日均量，表明市场参与度不高，上涨动能不足。

## 《信号解读》

最新交易日（2025-10-27）无买入或卖出星级信号。但在2025-10-10和2025-09-22两个交易日出现了买入一星信号，均是由于“低价高量”造成，但随后价格均未能维持涨势，表明这种信号并不稳定，需要配合其他指标验证。当前价格运行在布林带中轨附近，且布林带下轨斜率开始趋缓，但并未向上拐头，不符合理想买入点的条件。根据规则，不建议仅凭星级信号进行交易。

## 《关键价位》

- **支撑位：** 关键支撑位于布林带下轨，当前在3618.94附近； 另一个支撑位在MA120，当前在3968.95附近。如果价格有效跌破MA120，可能进一步下探。
- **阻力位：** 首个阻力位在MA60，当前位于4251.39附近； 更强的阻力位可能位于前期高点4684.25附近。

## 《操作建议》

- **短期（1-2 周）：**
  - **谨慎观望：** 考虑到成交量偏低和布林带下轨未明显拐头向上，短期内不建议激进操作。等待价格有效突破MA60并连续站稳3日以上（放量配合），或价格回落至布林带下轨附近且下轨斜率趋缓时，再考虑小仓位介入。
  - **控制风险：** 如果已经持有仓位，密切关注价格能否持续站稳MA20，若跌破则考虑减仓。
- **中期（1-2 月）：**
  - **逢低布局：** 中期来看，可以关注价格在MA120（3968.95附近）附近的表现，如果价格在该位置获得有效支撑且放量上攻，可考虑逐步建仓。
  - **长期持有：** 坚守价值投资逻辑，根据财务情况，逢回调逐步买入。

## 《风险与关注》

- **下跌风险：** 需警惕价格跌破MA5、MA10/MA20后，可能引发进一步下跌。若布林带下轨再次陡峭向下，应及时止损。
- **量能不足：** 关注成交量能否持续放大，若量能持续萎缩，可能导致上涨乏力。
- **宏观事件：** 密切关注美联储政策、地缘政治等宏观事件，这些因素可能对市场产生重大影响。
- **监管风险：** 关注各国监管政策变化，尤其是对稳定币的监管动向。

## 《波动率观察》

最近14日的ATR%为5.38%，相较于前期的波动有所降低，但仍然处于相对较高的水平，表明市场波动依然较大。这要求交易者在制定策略时充分考虑止损，并控制仓位规模。ATR%较高时，短线交易风险较高，不宜重仓操作。

## 《链上与情绪》

- **稳定币：** 稳定币总市值略有下降（-0.15%），但依然保持在高位，说明市场整体流动性尚可。需要注意的是，俄罗斯卢布稳定币受到欧盟制裁，可能对市场产生一定影响。Zelle支持stablecoin做国际支付，长期是利好。日本发行yen stablecoin对币圈是长期利好。
- **跨链桥接：** ETH跨链资金流入较高，表明市场对ETH的需求依然旺盛，但需要关注资金流向，判断其对价格的实际影响。
- **Gas/Mempool：** BTC Mempool 费用较低，表明链上活动并不活跃，可能反映了市场交易情绪偏谨慎。
- **恐慌指数：** BTC恐慌指数为51，属于中性水平，表明市场情绪相对稳定，既不过分乐观也不过分悲观。
- **新闻数据：** 新闻方面，关于Mt. Gox再次推迟赔付的消息可能对市场情绪产生负面影响；Bitcoin ETP流入量增多，显示机构信心有所恢复。Solana创始人质疑L2安全性，coinbase推进AI智能体交易等信息，短期内影响不大，需要持续观察。
- **衍生品：** OKX 永续开仓量增加 (+9.51% d/d) 显示交易活跃度上升，但多空爆仓数据显示空头爆仓量较大，可能预示着短期内存在进一步上涨的可能。

综上，当前市场多空因素交织，建议保持谨慎，密切关注关键价位和市场情绪变化，灵活调整交易策略。