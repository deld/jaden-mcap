// Service worker for After School Knowledge (issue #75).
//
// Only the app shell lives here: the page, the fonts, the manifest. Supabase
// traffic is deliberately NOT touched - that is handled in the page by the
// read-through cache and the outbox, which know the difference between a read
// worth replaying from cache and a write that must be queued in order. A
// service worker cannot make that distinction, and guessing would mean
// answering a write with a lie.
//
// Two strategies, because the page and its assets want different things.
//
// The PAGE is network-first with a short timeout, falling back to cache. It
// was cache-first, which meant a deploy did not appear until the SECOND open
// - fine for a stylesheet, not fine the day the parent PIN was removed and a
// phone carried on offering it. Online you get the current app; offline you
// still get the cached one, which is the whole point of this file.
//
// ASSETS (fonts, icons) stay stale-while-revalidate. They are immutable
// enough that a load behind is harmless, and they are the slow ones.
const CACHE = 'ask-shell-v2';
const NET_TIMEOUT = 3000;
const SHELL = ['./', './index.html', './manifest.webmanifest',
               './icon-192.png', './icon-512.png', './icon-maskable-512.png'];

self.addEventListener('install', (e) => {
  // addAll fails the whole install if any one URL 404s, so each is added
  // on its own - a missing font must not cost us the offline page.
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => Promise.all(SHELL.map((u) => c.add(u).catch(() => {}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

const cacheable = (url) =>
  url.origin === self.location.origin ||
  url.hostname === 'fonts.googleapis.com' ||
  url.hostname === 'fonts.gstatic.com';

const isPage = (req, url) =>
  req.mode === 'navigate' || req.destination === 'document' ||
  url.pathname.endsWith('/') || url.pathname.endsWith('/index.html');

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (!cacheable(url)) return;          // Supabase and everything else: untouched
  if (url.pathname.endsWith('/tests.html')) return;   // never serve tests from cache

  const save = (res) => {
    if (res && res.ok) caches.open(CACHE).then((c) => c.put(req, res.clone())).catch(() => {});
    return res;
  };

  if (isPage(req, url)) {
    e.respondWith((async () => {
      // Race the network against a short timer rather than waiting it out: a
      // phone on one bar should fall back to cache quickly, not hang.
      const net = fetch(req).then(save).catch(() => null);
      const timed = await Promise.race([
        net,
        new Promise((r) => setTimeout(() => r(undefined), NET_TIMEOUT)),
      ]);
      if (timed) return timed;
      return (await caches.match(req)) || (await net) ||
             new Response('offline', { status: 503 });
    })());
    return;
  }

  e.respondWith((async () => {
    const cached = await caches.match(req);
    const net = fetch(req).then(save).catch(() => null);
    return cached || (await net) || new Response('offline', { status: 503 });
  })());
});
