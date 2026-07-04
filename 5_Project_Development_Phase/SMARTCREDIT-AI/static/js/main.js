/* SmartCredit AI - Core JS: theme, toasts, sidebar, counters */

(function () {
  const root = document.documentElement;
  const THEME_KEY = 'smartcredit-theme';

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
  }

  function initTheme() {
    const saved = window.__smartcreditTheme || 'light';
    applyTheme(saved);
  }

  window.toggleTheme = function () {
    const current = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    window.__smartcreditTheme = next;
    document.cookie = `${THEME_KEY}=${next};path=/;max-age=31536000`;
  };

  initTheme();

  window.toggleSidebar = function () {
    document.querySelector('.sidebar')?.classList.toggle('open');
  };

  // ---------------- Toasts ----------------
  function ensureToastContainer() {
    let c = document.querySelector('.toast-container');
    if (!c) {
      c = document.createElement('div');
      c.className = 'toast-container';
      document.body.appendChild(c);
    }
    return c;
  }

  const ICONS = {
    success: '&#10003;', danger: '&#33;', warning: '&#9888;', info: '&#8505;',
  };

  window.showToast = function (message, type = 'info', duration = 4200) {
    const container = ensureToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
      <span style="font-weight:700;">${ICONS[type] || ICONS.info}</span>
      <span style="flex:1; font-size:14px;">${message}</span>
      <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
    `;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), duration);
  };

  // Render flash messages passed from Flask as toasts
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-flash]').forEach((el) => {
      window.showToast(el.dataset.flash, el.dataset.flashType || 'info');
    });

    // Animated counters
    document.querySelectorAll('[data-counter]').forEach((el) => {
      const target = parseFloat(el.dataset.counter);
      const decimals = el.dataset.decimals ? parseInt(el.dataset.decimals) : 0;
      const duration = 1200;
      const start = performance.now();
      function tick(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = (target * eased).toFixed(decimals);
        if (progress < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    });

    // Fill progress bars on load
    document.querySelectorAll('[data-progress]').forEach((el) => {
      const val = el.dataset.progress;
      requestAnimationFrame(() => { el.style.width = val + '%'; });
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
      const sidebar = document.querySelector('.sidebar');
      const toggleBtn = document.querySelector('.sidebar-toggle-btn');
      if (!sidebar || !sidebar.classList.contains('open')) return;
      if (!sidebar.contains(e.target) && e.target !== toggleBtn) {
        sidebar.classList.remove('open');
      }
    });
  });
})();
