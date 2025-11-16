const heroFieldMap = {
  atr_pct: document.querySelector('[data-field="atr_pct"]'),
  atr_date: document.querySelector('[data-field="atr_date"]'),
  atr_range: document.querySelector('[data-field="atr_range"]'),
  open_interest: document.querySelector('[data-field="open_interest"]'),
  oi_date: document.querySelector('[data-field="oi_date"]'),
};

const heroSparkMap = {
  atr: document.getElementById('sparkAtr'),
  atrRange: document.getElementById('sparkAtrRange'),
  oi: document.getElementById('sparkOi'),
};

const markdownTargets = {
  readme: document.getElementById('readmeContent'),
  analysis: document.getElementById('analysisContent'),
};

const charts = {};
const currencyCompact = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  notation: 'compact',
  maximumFractionDigits: 2,
});
const percentFormatter = new Intl.NumberFormat('en-US', {
  minimumFractionDigits: 0,
  maximumFractionDigits: 2,
});

const signalsFallbackEl = document.getElementById('signalsFallback');
const signalHighlightsEl = document.getElementById('signalHighlights');

document.addEventListener('DOMContentLoaded', () => {
  const yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  setupAnalysisToggle();
  loadMarkdown('./README.md', markdownTargets.readme);
  loadMarkdown('./model_analysis.md', markdownTargets.analysis, false);
  loadData();
  bindHeroScroll();
});

function setupAnalysisToggle() {
  const article = markdownTargets.analysis;
  const toggleBtn = document.getElementById('toggleAnalysis');
  if (!article || !toggleBtn) {
    return;
  }

  article.classList.add('is-collapsed');

  toggleBtn.addEventListener('click', () => {
    article.classList.toggle('is-collapsed');
    toggleBtn.textContent = article.classList.contains('is-collapsed') ? '展开全文' : '收起内容';
  });
}

async function loadData() {
  try {
    const [atrRes, oiRes, liqRes, signalsRes] = await Promise.allSettled([
      fetchJSON('./atr_metrics.json'),
      fetchJSON('./eth_open_interest_history.json'),
      fetchJSON('./eth_liquidations_daily.json'),
      fetchJSON('./signals_60d.json'),
    ]);

    if (atrRes.status !== 'fulfilled' || oiRes.status !== 'fulfilled' || liqRes.status !== 'fulfilled') {
      throw new Error('必要的 JSON 资源缺失，请先运行数据拉取脚本并重新部署。');
    }

    const atr = atrRes.value;
    const oi = oiRes.value;
    const liq = liqRes.value;
    const signals = signalsRes.status === 'fulfilled' ? signalsRes.value : null;

    updateHero(atr, oi);
    renderHeroSparklines(atr, oi);
    renderAtrChart(atr);
    renderOiChart(oi);
    renderLiqChart(liq);
    renderPerpSnapshotChart(atr, oi, liq);
    renderSignalsChart(signals);
    // 在合并面板中渲染火柴线小图
    renderPanelSparklines(atr, oi);
  } catch (error) {
    console.error('加载数据失败', error);
  }
}

async function fetchJSON(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`无法读取 ${path}`);
  }
  return response.json();
}

function extractGeminiReply(text) {
  try {
    // 优先从“### 1. 市场概述”开始（兼容是否带《》）
    const sectionStartRegex = /^###\s*1\.\s*(?:《)?市场概述(?:》)?/m;
    const sectionMatch = text.match(sectionStartRegex);
    if (sectionMatch) {
      const idx = text.indexOf(sectionMatch[0]);
      return text.slice(idx).trim();
    }

    // 次选：存在“## Gemini 回复”时，跳过该标题及其后的前言，直接从下一个三级标题开始
    const headerRegex = /^##\s*Gemini\s*回复\s*$/m;
    const headerMatch = text.match(headerRegex);
    if (headerMatch) {
      const headerIdx = text.indexOf(headerMatch[0]);
      const afterHeader = text.slice(headerIdx + headerMatch[0].length);
      const nextH3Regex = /^###\s+/m;
      const nextH3Match = afterHeader.match(nextH3Regex);
      if (nextH3Match) {
        const nextIdx = afterHeader.indexOf(nextH3Match[0]);
        return afterHeader.slice(nextIdx).trim();
      }
      // 如果没有后续三级标题，至少移除“Gemini 回复”行
      return text.replace(headerRegex, '').trim();
    }

    // 找不到标记则原样返回
    return text;
  } catch (_) {
    return text;
  }
}

// 移除各级标题中的中文书名号《》
function stripHeadingBrackets(text) {
  try {
    return text.replace(/^(\s*#{2,6}\s.*)$/gm, (line) => line.replace(/《([^》]+)》/g, '$1'));
  } catch (_) {
    return text;
  }
}

async function loadMarkdown(path, target, isLongForm = false) {
  if (!target) return;
  try {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error('获取 Markdown 失败');
    }
    let text = await response.text();
    // 仅在分析日报中展示 Gemini 回复，隐藏提示词与输入 JSON
    if (path.endsWith('model_analysis.md')) {
      text = extractGeminiReply(text);
      text = stripHeadingBrackets(text);
    }
    target.innerHTML = window.marked.parse(text, { mangle: false, headerIds: false });

    // 如果是 AI 日报，尝试从正文提取日期并更新标题
    if (path.endsWith('model_analysis.md')) {
      const dateMatch = text.match(/今天是(\d{4}-\d{2}-\d{2})/);
      const h2 = document.querySelector('#analysis .panel__header h2');
      if (h2) {
        const dateStr = dateMatch?.[1] || new Date().toISOString().slice(0, 10);
        h2.textContent = `${dateStr} 最新 AI 日报`;
      }
    }
    if (isLongForm) {
      target.classList.add('is-collapsed');
    }
  } catch (error) {
    console.error(error);
    target.innerHTML = '<p>暂时无法加载内容，请稍后再试。</p>';
  }
}

function updateHero(atrData, oiData) {
  if (atrData?.summary?.latest) {
    const latest = atrData.summary.latest;
    if (heroFieldMap.atr_pct) heroFieldMap.atr_pct.textContent = `${percentFormatter.format(latest.atr_pct)}%`;
    if (heroFieldMap.atr_date) heroFieldMap.atr_date.textContent = latest.date;
    if (typeof atrData.summary.min_pct === 'number' && typeof atrData.summary.max_pct === 'number') {
      if (heroFieldMap.atr_range)
        heroFieldMap.atr_range.textContent = `${percentFormatter.format(
          atrData.summary.min_pct,
        )}% - ${percentFormatter.format(atrData.summary.max_pct)}%`;
    }
  }

  if (Array.isArray(oiData) && oiData.length > 0) {
    const latest = oiData[oiData.length - 1];
    if (heroFieldMap.open_interest)
      heroFieldMap.open_interest.textContent = currencyCompact.format(latest.open_interest_usd);
    if (heroFieldMap.oi_date) heroFieldMap.oi_date.textContent = latest.date;
  }
}

function renderHeroSparklines(atrData, oiData) {
  try {
    // ATR sparkline using last 60 days
    if (heroSparkMap.atr && atrData?.series) {
      charts.sparkAtr?.destroy();
      const series = [...atrData.series]
        .filter((d) => d.date && typeof d.atr_pct === 'number')
        .sort((a, b) => new Date(a.date) - new Date(b.date))
        .slice(-60);
      charts.sparkAtr = new Chart(heroSparkMap.atr, {
        type: 'line',
        data: { datasets: [{ data: series.map((d) => ({ x: d.date, y: d.atr_pct })), borderColor: '#7c5dff', tension: 0.25, pointRadius: 0, fill: false }] },
        options: {
          responsive: true,
          plugins: { legend: { display: false }, tooltip: { enabled: true } },
          elements: { line: { borderWidth: 2 } },
          scales: { x: { type: 'time', display: false }, y: { display: false } },
        },
      });
    }

    // ATR range sparkline (same data for quick trend glance)
    if (heroSparkMap.atrRange && atrData?.series) {
      charts.sparkAtrRange?.destroy();
      const series = [...atrData.series]
        .filter((d) => d.date && typeof d.atr_pct === 'number')
        .sort((a, b) => new Date(a.date) - new Date(b.date))
        .slice(-180);
      charts.sparkAtrRange = new Chart(heroSparkMap.atrRange, {
        type: 'line',
        data: { datasets: [{ data: series.map((d) => ({ x: d.date, y: d.atr_pct })), borderColor: '#4ad5ff', tension: 0.25, pointRadius: 0, fill: false }] },
        options: {
          responsive: true,
          plugins: { legend: { display: false }, tooltip: { enabled: true } },
          elements: { line: { borderWidth: 2 } },
          scales: { x: { type: 'time', display: false }, y: { display: false } },
        },
      });
    }

    // Open interest sparkline using last 60 days
    if (heroSparkMap.oi && Array.isArray(oiData)) {
      charts.sparkOi?.destroy();
      const series = [...oiData]
        .filter((d) => d.date && typeof d.open_interest_usd === 'number')
        .sort((a, b) => new Date(a.date) - new Date(b.date))
        .slice(-60);
      charts.sparkOi = new Chart(heroSparkMap.oi, {
        type: 'line',
        data: { datasets: [{ data: series.map((d) => ({ x: d.date, y: d.open_interest_usd / 1e9 })), borderColor: '#ffffff', tension: 0.25, pointRadius: 0, fill: false }] },
        options: {
          responsive: true,
          plugins: { legend: { display: false }, tooltip: { enabled: true } },
          elements: { line: { borderWidth: 2 } },
          scales: { x: { type: 'time', display: false }, y: { display: false } },
        },
      });
    }
  } catch (err) {
    console.error('渲染火柴线失败', err);
  }
}

// 额外渲染图表总览中的火柴线（如果存在）
function renderPanelSparklines(atrData, oiData) {
  const sparkAtrPanel = document.getElementById('sparkAtrPanel');
  const sparkAtrRangePanel = document.getElementById('sparkAtrRangePanel');
  const sparkOiPanel = document.getElementById('sparkOiPanel');

  try {
    if (sparkAtrPanel && atrData?.series) {
      charts.sparkAtrPanel?.destroy();
      const series = [...atrData.series]
        .filter((d) => d.date && typeof d.atr_pct === 'number')
        .sort((a, b) => new Date(a.date) - new Date(b.date))
        .slice(-60);
      charts.sparkAtrPanel = new Chart(sparkAtrPanel, {
        type: 'line',
        data: { datasets: [{ data: series.map((d) => ({ x: d.date, y: d.atr_pct })), borderColor: '#7c5dff', tension: 0.25, pointRadius: 0, fill: false }] },
        options: { responsive: true, plugins: { legend: { display: false } }, scales: { x: { type: 'time', display: false }, y: { display: false } } },
      });
    }

    if (sparkAtrRangePanel && atrData?.series) {
      charts.sparkAtrRangePanel?.destroy();
      const series = [...atrData.series]
        .filter((d) => d.date && typeof d.atr_pct === 'number')
        .sort((a, b) => new Date(a.date) - new Date(b.date))
        .slice(-180);
      charts.sparkAtrRangePanel = new Chart(sparkAtrRangePanel, {
        type: 'line',
        data: { datasets: [{ data: series.map((d) => ({ x: d.date, y: d.atr_pct })), borderColor: '#4ad5ff', tension: 0.25, pointRadius: 0, fill: false }] },
        options: { responsive: true, plugins: { legend: { display: false } }, scales: { x: { type: 'time', display: false }, y: { display: false } } },
      });
    }

    if (sparkOiPanel && Array.isArray(oiData)) {
      charts.sparkOiPanel?.destroy();
      const series = [...oiData]
        .filter((d) => d.date && typeof d.open_interest_usd === 'number')
        .sort((a, b) => new Date(a.date) - new Date(b.date))
        .slice(-60);
      charts.sparkOiPanel = new Chart(sparkOiPanel, {
        type: 'line',
        data: { datasets: [{ data: series.map((d) => ({ x: d.date, y: d.open_interest_usd / 1e9 })), borderColor: '#ffffff', tension: 0.25, pointRadius: 0, fill: false }] },
        options: { responsive: true, plugins: { legend: { display: false } }, scales: { x: { type: 'time', display: false }, y: { display: false } } },
      });
    }
  } catch (err) {
    console.error('渲染图表总览火柴线失败', err);
  }
}

function bindHeroScroll() {
  const metricsSection = document.getElementById('charts-overview');
  const container = document.getElementById('latestMetrics');
  if (!metricsSection || !container) return;
  container.querySelectorAll('.hero-card').forEach((card) => {
    card.style.cursor = 'pointer';
    card.addEventListener('click', () => metricsSection.scrollIntoView({ behavior: 'smooth' }));
  });
}

function renderAtrChart(atrData) {
  if (!atrData?.series) return;
  const ctx = document.getElementById('atrChart');
  if (!ctx) return;
  charts.atr?.destroy();

  const series = [...atrData.series].sort((a, b) => new Date(a.date) - new Date(b.date));
  charts.atr = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [
        {
          label: 'ATR% (14)',
          data: series.map((d) => ({ x: d.date, y: d.atr_pct })),
          borderColor: '#7c5dff',
          backgroundColor: 'rgba(124,93,255,0.25)',
          tension: 0.25,
          fill: true,
          yAxisID: 'y',
          pointRadius: 0,
        },
        {
          label: '收盘价 (USD)',
          data: series.map((d) => ({ x: d.date, y: d.close })),
          borderColor: '#4ad5ff',
          backgroundColor: 'rgba(74,213,255,0.3)',
          tension: 0.2,
          fill: false,
          yAxisID: 'y1',
          pointRadius: 0,
        },
      ],
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      scales: {
        x: {
          type: 'time',
          time: { parser: 'yyyy-MM-dd', tooltipFormat: 'yyyy-MM-dd' },
          grid: { color: 'rgba(255,255,255,0.05)' },
        },
        y: {
          position: 'left',
          ticks: {
            callback: (value) => `${value}%`,
            color: '#ccc',
          },
          grid: { color: 'rgba(255,255,255,0.05)' },
        },
        y1: {
          position: 'right',
          ticks: {
            color: '#ccc',
            callback: (value) => `$${Number(value).toLocaleString('en-US')}`,
          },
          grid: { drawOnChartArea: false },
        },
      },
      plugins: {
        legend: { labels: { color: '#fff' } },
      },
    },
  });
}

function renderOiChart(data) {
  if (!Array.isArray(data)) return;
  const ctx = document.getElementById('oiChart');
  if (!ctx) return;
  charts.oi?.destroy();

  const sorted = [...data].sort((a, b) => new Date(a.date) - new Date(b.date));
  charts.oi = new Chart(ctx, {
    type: 'bar',
    data: {
      datasets: [
        {
          type: 'line',
          label: 'Open Interest (十亿美元)',
          data: sorted.map((d) => ({ x: d.date, y: d.open_interest_usd / 1e9 })),
          borderColor: '#4ad5ff',
          backgroundColor: '#4ad5ff',
          tension: 0.2,
          yAxisID: 'y',
          pointRadius: 0,
        },
        {
          type: 'bar',
          label: 'Perp Volume (十亿美元)',
          data: sorted.map((d) => ({ x: d.date, y: d.perp_volume_usd / 1e9 })),
          backgroundColor: 'rgba(124,93,255,0.4)',
          yAxisID: 'y1',
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      scales: {
        x: {
          type: 'time',
          time: { parser: 'yyyy-MM-dd', tooltipFormat: 'yyyy-MM-dd' },
          stacked: false,
          grid: { color: 'rgba(255,255,255,0.04)' },
        },
        y: {
          position: 'left',
          ticks: {
            callback: (value) => `${value.toFixed(1)}B`,
            color: '#ccc',
          },
          grid: { color: 'rgba(255,255,255,0.04)' },
        },
        y1: {
          position: 'right',
          ticks: {
            callback: (value) => `${value.toFixed(1)}B`,
            color: '#ccc',
          },
          grid: { drawOnChartArea: false },
        },
      },
      plugins: {
        legend: { labels: { color: '#fff' } },
      },
    },
  });
}

function renderLiqChart(data) {
  if (!Array.isArray(data)) return;
  const ctx = document.getElementById('liqChart');
  if (!ctx) return;
  charts.liq?.destroy();

  const recent = data
    .map((d) => ({
      ...d,
      long_liquidations_usd: d.long_liquidations_usd || 0,
      short_liquidations_usd: d.short_liquidations_usd || 0,
    }))
    .filter((d) => d.date)
    .sort((a, b) => new Date(a.date) - new Date(b.date))
    .slice(-90);

  charts.liq = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: recent.map((d) => d.date),
      datasets: [
        {
          label: 'Long Liquidations (USD)',
          data: recent.map((d) => d.long_liquidations_usd / 1e6),
          backgroundColor: 'rgba(74,213,255,0.7)',
          stack: 'stack0',
        },
        {
          label: 'Short Liquidations (USD)',
          data: recent.map((d) => d.short_liquidations_usd / 1e6),
          backgroundColor: 'rgba(255,119,146,0.8)',
          stack: 'stack0',
        },
      ],
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      scales: {
        x: {
          ticks: {
            maxRotation: 0,
            callback: (value, index, ticks) => {
              const label = recent[index]?.date;
              return index % Math.ceil(ticks.length / 6) === 0 ? label : '';
            },
            color: '#bbb',
          },
          grid: { color: 'rgba(255,255,255,0.04)' },
        },
        y: {
          ticks: {
            callback: (value) => `${value.toFixed(0)}M`,
            color: '#ccc',
          },
          grid: { color: 'rgba(255,255,255,0.04)' },
        },
      },
      plugins: {
        legend: { labels: { color: '#fff' } },
      },
    },
  });
}

function renderPerpSnapshotChart(atrData, oiData, liqData) {
  const ctx = document.getElementById('perpSnapshotChart');
  if (!ctx || !Array.isArray(oiData) || !atrData?.series) return;
  charts.perpSnapshot?.destroy();

  const closeMap = new Map(atrData.series.map((item) => [item.date, item.close]));
  const liqMap = new Map((Array.isArray(liqData) ? liqData : []).map((item) => [item.date, item]));

  const merged = oiData
    .map((row) => {
      const close = closeMap.get(row.date);
      const liqRow = liqMap.get(row.date);
      return {
        date: row.date,
        openInterest: typeof row.open_interest_usd === 'number' ? row.open_interest_usd / 1e9 : null,
        close: typeof close === 'number' ? close : null,
        longLiq: liqRow?.long_liquidations_usd ? liqRow.long_liquidations_usd / 1e6 : 0,
        shortLiq: liqRow?.short_liquidations_usd ? liqRow.short_liquidations_usd / 1e6 : 0,
      };
    })
    .filter((row) => row.openInterest !== null && row.close !== null);

  if (!merged.length) {
    return;
  }

  charts.perpSnapshot = new Chart(ctx, {
    data: {
      datasets: [
        {
          type: 'line',
          label: 'Close (USD)',
          data: merged.map((d) => ({ x: d.date, y: d.close })),
          borderColor: '#ffffff',
          tension: 0.25,
          yAxisID: 'price',
          pointRadius: 0,
        },
        {
          type: 'line',
          label: 'Open Interest (B USD)',
          data: merged.map((d) => ({ x: d.date, y: d.openInterest })),
          borderColor: '#4ad5ff',
          backgroundColor: 'rgba(74,213,255,0.35)',
          fill: false,
          yAxisID: 'oi',
          pointRadius: 0,
        },
        {
          type: 'bar',
          label: 'Long Liq (M USD)',
          data: merged.map((d) => ({ x: d.date, y: d.longLiq })),
          backgroundColor: 'rgba(74,213,255,0.4)',
          yAxisID: 'liq',
          stack: 'liq',
          order: 3,
        },
        {
          type: 'bar',
          label: 'Short Liq (M USD)',
          data: merged.map((d) => ({ x: d.date, y: d.shortLiq })),
          backgroundColor: 'rgba(255,119,146,0.45)',
          yAxisID: 'liq',
          stack: 'liq',
          order: 3,
        },
      ],
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      scales: {
        x: {
          type: 'time',
          time: { parser: 'yyyy-MM-dd', tooltipFormat: 'yyyy-MM-dd' },
          grid: { color: 'rgba(255,255,255,0.04)' },
        },
        price: {
          position: 'left',
          ticks: {
            callback: (value) => `$${Number(value).toLocaleString('en-US')}`,
            color: '#ccc',
          },
          grid: { color: 'rgba(255,255,255,0.04)' },
        },
        oi: {
          position: 'right',
          ticks: {
            callback: (value) => `${Number(value).toFixed(1)}B`,
            color: '#ccc',
          },
          grid: { drawOnChartArea: false },
        },
        liq: {
          position: 'right',
          ticks: {
            callback: (value) => `${Number(value).toFixed(0)}M`,
            color: '#ccc',
          },
          grid: { drawOnChartArea: false },
        },
      },
      plugins: {
        legend: { labels: { color: '#fff' } },
      },
    },
  });
}

function renderSignalsChart(data) {
  const canvas = document.getElementById('signalsChart');
  if (!canvas) return;
  charts.signals?.destroy();

  if (!Array.isArray(data) || data.length === 0) {
    canvas.classList.add('is-hidden');
    signalsFallbackEl?.classList.remove('is-hidden');
    updateSignalHighlights(null);
    return;
  }

  canvas.classList.remove('is-hidden');
  signalsFallbackEl?.classList.add('is-hidden');

  const sorted = [...data]
    .filter((d) => d.date)
    .sort((a, b) => new Date(a.date) - new Date(b.date));

  charts.signals = new Chart(canvas, {
    data: {
      datasets: [
        {
          type: 'line',
          label: 'Close (USD)',
          data: sorted.map((d) => ({ x: d.date, y: d.close })),
          borderColor: '#ffffff',
          yAxisID: 'price',
          tension: 0.25,
          pointRadius: 0,
        },
        {
          type: 'line',
          label: 'MA20',
          data: sorted.map((d) => ({ x: d.date, y: d.ma_20 })),
          borderColor: '#7c5dff',
          borderDash: [4, 4],
          yAxisID: 'price',
          tension: 0.2,
          pointRadius: 0,
        },
        {
          type: 'line',
          label: 'MA60',
          data: sorted.map((d) => ({ x: d.date, y: d.ma_60 })),
          borderColor: '#4ad5ff',
          borderDash: [6, 4],
          yAxisID: 'price',
          tension: 0.2,
          pointRadius: 0,
        },
        {
          type: 'line',
          label: 'RSI14',
          data: sorted.map((d) => ({ x: d.date, y: d.rsi14 })),
          borderColor: '#ffa726',
          backgroundColor: 'rgba(255,167,38,0.1)',
          yAxisID: 'osc',
          tension: 0.3,
          pointRadius: 0,
          fill: true,
        },
        {
          type: 'scatter',
          label: 'Buy Stars',
          data: sorted
            .filter((d) => d.buy_stars > 0 && typeof d.close === 'number')
            .map((d) => ({ x: d.date, y: d.close, r: 4 + d.buy_stars * 1.5 })),
          yAxisID: 'price',
          backgroundColor: '#66bb6a',
          pointStyle: 'triangle',
          showLine: false,
        },
        {
          type: 'scatter',
          label: 'Sell Stars',
          data: sorted
            .filter((d) => d.sell_stars > 0 && typeof d.close === 'number')
            .map((d) => ({ x: d.date, y: d.close, r: 4 + d.sell_stars * 1.5 })),
          yAxisID: 'price',
          backgroundColor: '#ef5350',
          pointStyle: 'rectRot',
          showLine: false,
        },
      ],
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      scales: {
        x: {
          type: 'time',
          time: { parser: 'yyyy-MM-dd', tooltipFormat: 'yyyy-MM-dd' },
          grid: { color: 'rgba(255,255,255,0.04)' },
        },
        price: {
          position: 'left',
          ticks: {
            callback: (value) => `$${Number(value).toLocaleString('en-US')}`,
            color: '#ccc',
          },
          grid: { color: 'rgba(255,255,255,0.04)' },
        },
        osc: {
          position: 'right',
          suggestedMin: 0,
          suggestedMax: 100,
          ticks: {
            callback: (value) => `${value}`,
            color: '#ccc',
          },
          grid: { drawOnChartArea: false },
        },
      },
      plugins: {
        legend: { labels: { color: '#fff' } },
      },
    },
  });

  updateSignalHighlights(sorted[sorted.length - 1]);
}

function updateSignalHighlights(latest) {
  if (!signalHighlightsEl) return;
  if (!latest) {
    signalHighlightsEl.innerHTML =
      '<div class="highlight-card"><span>提示</span><strong>缺少数据</strong><small>生成 signals_60d.json 后自动更新</small></div>';
    return;
  }

  const rows = [
    {
      label: 'RSI14',
      value: latest.rsi14 ?? '--',
      hint: '超买70 · 超卖30',
    },
    {
      label: 'ATR%14',
      value: latest.atr_pct_14 ? `${percentFormatter.format(latest.atr_pct_14)}%` : '--',
      hint: '波动率',
    },
    {
      label: 'Buy Stars',
      value: latest.buy_stars ?? 0,
      hint: '0~3 星',
    },
    {
      label: 'Sell Stars',
      value: latest.sell_stars ?? 0,
      hint: '0~3 星',
    },
    {
      label: 'Volume/Ma20',
      value: latest.volume_ratio_ma20 ?? '--',
      hint: '>=1 表示量能支撑',
    },
  ];

  signalHighlightsEl.innerHTML = rows
    .map(
      (row) => `
      <div class="highlight-card">
        <span>${row.label}</span>
        <strong>${row.value}</strong>
        <small>${row.hint}</small>
      </div>
    `,
    )
    .join('');
}
