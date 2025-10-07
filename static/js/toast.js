// API: showToast({ title, message, type='info', timeout=2500 })
// Types: 'success' | 'error' | 'warning' | 'info'

(function () {
  const el = document.getElementById('toast-component');
  const iconEl = document.getElementById('toast-icon');
  const titleEl = document.getElementById('toast-title');
  const msgEl = document.getElementById('toast-message');
  const progEl = document.getElementById('toast-progress');

  if (!el || !iconEl || !titleEl || !msgEl || !progEl) return;

  let hideTimer = null, rafId = null, startTs = null, duration = 0;

  const TYPES = {
    success: { icon: '✓', classes: 'bg-emerald-600' },
    error:   { icon: '✕', classes: 'bg-rose-700' },
    warning: { icon: '!', classes: 'bg-amber-600' },
    info:    { icon: 'i', classes: 'bg-slate-900' },
  };

  function resetTypeClasses() {
    el.classList.remove('bg-emerald-600','bg-rose-700','bg-amber-600','bg-slate-900');
  }

  function clearTimers() {
    if (hideTimer) clearTimeout(hideTimer);
    if (rafId) cancelAnimationFrame(rafId);
    hideTimer = null; rafId = null; startTs = null;
  }

  function animateProgress(ts) {
    if (!startTs) startTs = ts;
    const pct = Math.min(1, (ts - startTs) / duration);
    progEl.style.width = (pct * 100).toFixed(2) + '%';
    if (pct < 1) rafId = requestAnimationFrame(animateProgress);
  }

  function show({ title='Notice', message='', type='info', timeout=2500 } = {}) {
    const t = TYPES[type] || TYPES.info;

    // style & content
    resetTypeClasses();
    el.classList.add(t.classes);
    iconEl.textContent = t.icon;
    titleEl.textContent = String(title);
    msgEl.textContent = String(message);
    progEl.style.width = '0%';

    // reveal (uses your classes)
    el.classList.remove('opacity-0','translate-y-64','pointer-events-none');
    el.classList.add('opacity-100','translate-y-0','pointer-events-auto');

    // timers
    duration = Math.max(800, Number(timeout) || 2500);
    clearTimers();
    rafId = requestAnimationFrame(animateProgress);
    hideTimer = setTimeout(hide, duration);
  }

  function hide() {
    clearTimers();
    el.classList.add('opacity-0','translate-y-64','pointer-events-none');
    el.classList.remove('opacity-100','translate-y-0','pointer-events-auto');
    setTimeout(() => { progEl.style.width = '0%'; }, 220);
  }

  // Pause on hover
  el.addEventListener('mouseenter', () => clearTimers());
  el.addEventListener('mouseleave', () => {
    if (getComputedStyle(el).opacity !== '0') {
      startTs = null;
      rafId = requestAnimationFrame(animateProgress);
      hideTimer = setTimeout(hide, duration);
    }
  });

  // Public API
  window.showToast = show;
  window.hideToast = hide;

  // Optional event-based trigger
  window.addEventListener('toast:show', e => show(e.detail || {}));
})();
