(() => {
  const root = document.documentElement;
  const storageKey = 'rui-yu-theme';
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = null;
  try {
    const saved = localStorage.getItem(storageKey);
    if (saved === 'light' || saved === 'dark') preference = saved;
  } catch (_) {}

  const applyTheme = theme => {
    root.dataset.theme = theme;
    const toggle = document.querySelector('[data-theme-toggle]');
    if (toggle) {
      toggle.setAttribute('aria-checked', String(theme === 'dark'));
      toggle.title = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
    }
    const color = document.querySelector('meta[name="theme-color"]');
    if (color) color.content = theme === 'dark' ? '#111111' : '#ffffff';
  };

  applyTheme(preference || (systemTheme.matches ? 'dark' : 'light'));
  systemTheme.addEventListener('change', () => {
    if (!preference) applyTheme(systemTheme.matches ? 'dark' : 'light');
  });

  const bindControls = () => {
    const toggle = document.querySelector('[data-theme-toggle]');
    if (toggle) {
      applyTheme(root.dataset.theme);
      toggle.hidden = false;
      toggle.addEventListener('click', () => {
        preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem(storageKey, preference); } catch (_) {}
        applyTheme(preference);
      });
    }
    document.querySelector('[data-print]')?.addEventListener('click', () => window.print());
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindControls, {once: true});
  } else {
    bindControls();
  }
})();
