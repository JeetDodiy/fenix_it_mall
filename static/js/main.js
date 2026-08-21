/* Fenix IT Mall – Global JS */

// ── Confirm delete helper ──
function confirmDelete(msg) {
  return window.confirm(msg || 'Are you sure you want to delete this?');
}

// ── Format currency ──
function formatINR(amount) {
  return '₹' + parseFloat(amount).toLocaleString('en-IN', { minimumFractionDigits: 2 });
}

// ── Auto-hide alerts after 4s ──
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.alert-auto').forEach(function (el) {
    setTimeout(function () {
      el.style.opacity = '0';
      el.style.transform = 'translateY(-10px)';
      el.style.transition = 'all 0.4s ease';
      setTimeout(function () { el.remove(); }, 400);
    }, 4000);
  });

  // ── Active nav item highlight by URL ──
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(function (item) {
    const href = item.getAttribute('href');
    if (href && path.startsWith(href) && href !== '/') {
      item.classList.add('active');
    }
  });

  // ── Close dropdowns on outside click ──
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.dropdown')) {
      document.querySelectorAll('.dropdown-menu.open').forEach(function (m) {
        m.classList.remove('open');
      });
    }
  });
});

// ── Simple modal helpers ──
function openModal(id) {
  const m = document.getElementById(id);
  if (m) m.style.display = 'flex';
}
function closeModal(id) {
  const m = document.getElementById(id);
  if (m) m.style.display = 'none';
}
// Close modal on backdrop click
document.addEventListener('click', function (e) {
  if (e.target.classList.contains('modal-backdrop')) {
    e.target.style.display = 'none';
  }
});
