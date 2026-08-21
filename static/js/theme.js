// theme.js
document.addEventListener('DOMContentLoaded', () => {
  const themeSwitch = document.getElementById('theme-switch');
  
  // Check for saved theme preference or use system preference
  const savedTheme = localStorage.getItem('theme');
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
    document.documentElement.setAttribute('data-theme', 'dark');
    if(themeSwitch) themeSwitch.checked = true;
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
    if(themeSwitch) themeSwitch.checked = false;
  }
  
  // Listen for toggle
  if(themeSwitch) {
    themeSwitch.addEventListener('change', (e) => {
      if(e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
      }
    });
  }
});
