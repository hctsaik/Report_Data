// Preserve the originating ER subject while the reader visits related lessons.
(() => {
  'use strict';
  const token = new URLSearchParams(location.search).get('erReturn');
  if (!token || !/^[a-zA-Z0-9_-]{1,120}$/.test(token)) return;
  let saved, destination;
  try {
    saved = JSON.parse(sessionStorage.getItem('mes-er-return:' + token));
    destination = new URL(saved.url, location.href);
    const atlas = new URL('er-atlas.html', location.href);
    if (destination.origin !== location.origin || destination.pathname !== atlas.pathname) return;
  } catch (_) { return; }
  destination.searchParams.set('erResume', token);

  const style = document.createElement('style');
  style.textContent = '.er-return-nav{display:flex;flex-wrap:wrap;align-items:center;gap:10px 20px;margin:12px 24px;padding:12px 16px;border:1px solid #b9d4ee;border-radius:10px;background:#f1f7fe;color:#173d5d;font:600 16px/1.5 system-ui,sans-serif}.er-return-nav a{color:#125d9f;text-decoration:underline;text-underline-offset:3px;padding:8px 2px;overflow-wrap:anywhere}.er-return-nav a:focus-visible{outline:3px solid #126eca;outline-offset:3px}.er-return-nav .er-return-position{flex-basis:100%;font-size:14px;font-weight:400}@media(max-width:600px){.er-return-nav{margin:10px 12px;padding:10px 12px;gap:4px 16px}.er-return-nav a:first-child{flex-basis:100%}}';
  document.head.append(style);
  const nav = document.createElement('nav');
  nav.className = 'er-return-nav';
  nav.setAttribute('aria-label', '返回 ER 與課程首頁');
  const back = document.createElement('a');
  back.id = 'return-to-er';
  back.href = destination.href;
  back.textContent = '← 返回 ER：' + (typeof saved.label === 'string' && saved.label.trim() ? saved.label.slice(0, 160) : '剛才的主詞');
  const home = document.createElement('a');
  home.href = 'index.html#fab';
  home.textContent = '課程首頁';
  const position = document.createElement('span');
  position.className = 'er-return-position';
  const describe = () => { position.textContent = 'ER 關聯圖 → ' + document.title; };
  describe();
  nav.append(back, home, position);
  const header = document.querySelector('header');
  if (header) header.after(nav); else document.body.prepend(nav);

  const lessonPaths = new Set(['index.html', 'operations.html', 'flow.html', 'advanced.html', 'support.html', 'data-map.html', 'freshness.html'].map(file => new URL(file, location.href).pathname));
  function carryContext(root) {
    root.querySelectorAll('a[href]').forEach(link => {
      if (link.hasAttribute('download')) return;
      try {
        const url = new URL(link.getAttribute('href'), location.href);
        if (url.origin !== location.origin || !lessonPaths.has(url.pathname)) return;
        url.searchParams.set('erReturn', token);
        link.href = url.href;
      } catch (_) { /* Leave links that cannot be parsed unchanged. */ }
    });
  }
  carryContext(document);
  new MutationObserver(() => carryContext(document)).observe(document.body, {childList: true, subtree: true});
  window.addEventListener('hashchange', describe);
})();
