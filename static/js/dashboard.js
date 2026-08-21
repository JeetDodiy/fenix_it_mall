/* Fenix IT Mall – Dashboard Charts & Animations
   Requires: Chart.js, GSAP (loaded via CDN in template)
*/

document.addEventListener('DOMContentLoaded', function () {

  // ── Simple Counter Display (No Animation) ──
  // Just display the values directly without GSAP animation
  document.querySelectorAll('[data-count]').forEach(function (el) {
    const target = parseFloat(el.getAttribute('data-count')) || 0;
    const prefix = el.getAttribute('data-prefix') || '';
    const suffix = el.getAttribute('data-suffix') || '';
    const isFloat = el.getAttribute('data-float') === '1';
    
    // Display value immediately
    el.textContent = prefix + (isFloat
      ? target.toFixed(2)
      : Math.round(target).toLocaleString('en-IN')) + suffix;
  });

  // Simple fade-in for cards (CSS-based, no GSAP)
  setTimeout(function() {
    document.querySelectorAll('.stat-card, .card').forEach(function(card) {
      card.style.opacity = '1';
    });
  }, 50);

  // ── Chart.js defaults ──
  if (typeof Chart !== 'undefined') {
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.borderColor = 'rgba(255,255,255,0.06)';
    Chart.defaults.font.family = "'Inter', 'Segoe UI', sans-serif";

    // ── Revenue & Sales Line Chart ──
    const revCtx = document.getElementById('revenueChart');
    if (revCtx) {
      new Chart(revCtx, {
        type: 'line',
        data: {
          labels: JSON.parse(revCtx.dataset.labels || '[]'),
          datasets: [
            {
              label: 'Revenue (₹)',
              data: JSON.parse(revCtx.dataset.revenue || '[]'),
              borderColor: '#06b6d4',
              backgroundColor: 'rgba(6,182,212,0.08)',
              borderWidth: 2.5,
              pointBackgroundColor: '#06b6d4',
              pointRadius: 4,
              tension: 0.4,
              fill: true,
              yAxisID: 'y',
            },
            {
              label: 'Profit (₹)',
              data: JSON.parse(revCtx.dataset.profit || '[]'),
              borderColor: '#10b981',
              backgroundColor: 'rgba(16,185,129,0.05)',
              borderWidth: 2,
              pointBackgroundColor: '#10b981',
              pointRadius: 3,
              tension: 0.4,
              fill: false,
              yAxisID: 'y',
            },
            {
              label: 'Sales Count',
              data: JSON.parse(revCtx.dataset.sales || '[]'),
              borderColor: '#a855f7',
              backgroundColor: 'transparent',
              borderWidth: 2,
              borderDash: [6, 3],
              pointBackgroundColor: '#a855f7',
              pointRadius: 3,
              tension: 0.4,
              fill: false,
              yAxisID: 'y1',
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: { position: 'top', labels: { usePointStyle: true, padding: 20, font: { size: 12 } } },
            tooltip: {
              backgroundColor: 'rgba(13,21,38,0.95)',
              borderColor: 'rgba(6,182,212,0.3)',
              borderWidth: 1,
              padding: 12,
              titleFont: { size: 13, weight: '600' },
              callbacks: {
                label: function (ctx) {
                  if (ctx.datasetIndex < 2) return ' ₹' + ctx.parsed.y.toLocaleString('en-IN');
                  return ' ' + ctx.parsed.y + ' sales';
                }
              }
            }
          },
          scales: {
            x: { grid: { color: 'rgba(255,255,255,0.04)' } },
            y: { position: 'left', grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { callback: v => '₹' + v.toLocaleString('en-IN') } },
            y1: { position: 'right', grid: { drawOnChartArea: false }, ticks: { stepSize: 1 } }
          }
        }
      });
    }

    // ── Category Donut Chart ──
    const catCtx = document.getElementById('categoryChart');
    if (catCtx) {
      const colors = ['#06b6d4','#a855f7','#10b981','#f59e0b','#ef4444','#3b82f6','#ec4899','#14b8a6'];
      new Chart(catCtx, {
        type: 'doughnut',
        data: {
          labels: JSON.parse(catCtx.dataset.labels || '[]'),
          datasets: [{
            data: JSON.parse(catCtx.dataset.values || '[]'),
            backgroundColor: colors.map(c => c + '99'),
            borderColor: colors,
            borderWidth: 2,
            hoverOffset: 8,
          }]
        },
        options: {
          responsive: true, maintainAspectRatio: false, cutout: '68%',
          plugins: {
            legend: { position: 'right', labels: { usePointStyle: true, padding: 16, font: { size: 12 } } },
            tooltip: {
              backgroundColor: 'rgba(13,21,38,0.95)',
              borderColor: 'rgba(6,182,212,0.3)',
              borderWidth: 1,
              padding: 10,
            }
          }
        }
      });
    }

    // ── Inventory Status Bar Chart ──
    const invCtx = document.getElementById('inventoryChart');
    if (invCtx) {
      new Chart(invCtx, {
        type: 'bar',
        data: {
          labels: ['In Stock', 'Low Stock', 'Out of Stock'],
          datasets: [{
            data: JSON.parse(invCtx.dataset.values || '[]'),
            backgroundColor: ['rgba(16,185,129,0.7)', 'rgba(245,158,11,0.7)', 'rgba(239,68,68,0.7)'],
            borderColor: ['#10b981', '#f59e0b', '#ef4444'],
            borderWidth: 2,
            borderRadius: 8,
            borderSkipped: false,
          }]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false } },
            y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { stepSize: 1 } }
          }
        }
      });
    }

    // ── Best Sellers Horizontal Bar ──
    const bsCtx = document.getElementById('bestSellersChart');
    if (bsCtx) {
      new Chart(bsCtx, {
        type: 'bar',
        data: {
          labels: JSON.parse(bsCtx.dataset.labels || '[]'),
          datasets: [{
            label: 'Units Sold',
            data: JSON.parse(bsCtx.dataset.values || '[]'),
            backgroundColor: 'rgba(168,85,247,0.7)',
            borderColor: '#a855f7',
            borderWidth: 2,
            borderRadius: 6,
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { stepSize: 1 } },
            y: { grid: { display: false } }
          }
        }
      });
    }
  }
});
