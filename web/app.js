const heroFieldMap = {
  atr_pct: document.querySelector('[data-field="atr_pct"]'),
  atr_date: document.querySelector('[data-field="atr_date"]'),
  atr_range: document.querySelector('[data-field="atr_range"]'),
  open_interest: document.querySelector('[data-field="open_interest"]'),
  oi_date: document.querySelector('[data-field="oi_date"]'),
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

document.addEventListener('DOMContentLoaded', () => {
  const yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  setupAnalysisToggle();
  setupImageFallbacks();
  loadMarkdown('./README.md', markdownTargets.readme);
  loadMarkdown('./model_analysis.md', markdownTargets.analysis, true);
  loadData();
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

function setupImageFallbacks() {
  document.querySelectorAll('img[data-hide-on-error="true"]').forEach((img) => {
    img.addEventListener('error', () => {
      const parent = img.closest('.gallery__item');
      if (parent) parent.classList.add('is-hidden');
    });
  });
}

async function loadData() {
  try {
    const [atr, oi, liq] = await Promise.all([
      fetchJSON('./atr_metrics.json'),
      fetchJSON('./eth_open_interest_history.json'),
      fetchJSON('./eth_liquidations_daily.json'),
    ]);
    updateHero(atr, oi);
    renderAtrChart(atr);
    renderOiChart(oi);
    renderLiqChart(liq);
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

async function loadMarkdown(path, target, isLongForm = false) {
  if (!target) return;
  try {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error('获取 Markdown 失败');
    }
    const text = await response.text();
    target.innerHTML = window.marked.parse(text, { mangle: false, headerIds: false });
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
    heroFieldMap.atr_pct.textContent = `${percentFormatter.format(latest.atr_pct)}%`;
    heroFieldMap.atr_date.textContent = latest.date;
    if (typeof atrData.summary.min_pct === 'number' && typeof atrData.summary.max_pct === 'number') {
      heroFieldMap.atr_range.textContent = `${percentFormatter.format(
        atrData.summary.min_pct,
      )}% - ${percentFormatter.format(atrData.summary.max_pct)}%`;
    }
  }

  if (Array.isArray(oiData) && oiData.length > 0) {
    const latest = oiData[oiData.length - 1];
    heroFieldMap.open_interest.textContent = currencyCompact.format(latest.open_interest_usd);
    heroFieldMap.oi_date.textContent = latest.date;
  }
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
