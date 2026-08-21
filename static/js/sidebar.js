// sidebar.js
document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const desktopToggle = document.getElementById('sidebar-toggle');
  const mobileToggle = document.getElementById('mobile-toggle');
  const mainContent = document.querySelector('.main-content');
  const navbar = document.querySelector('.navbar');

  if (desktopToggle && sidebar) {
    desktopToggle.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
      if (mainContent) mainContent.classList.toggle('sidebar-collapsed');
      if (navbar) navbar.classList.toggle('sidebar-collapsed');
    });
  }

  if (mobileToggle && sidebar) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('mobile-open');
    });

    // Close mobile sidebar when clicking outside
    document.addEventListener('click', (e) => {
      if (sidebar.classList.contains('mobile-open') && 
          !sidebar.contains(e.target) && 
          e.target !== mobileToggle) {
        sidebar.classList.remove('mobile-open');
      }
    });
  }
});
