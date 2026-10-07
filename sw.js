// Service worker for After School Knowledge (issue #75).
//
// Only the app shell lives here: the page, the fonts, the manifest. Supabase
// traffic is deliberately NOT touched - that is handled in the page by the
// read-through cache and the outbox, which know the difference between a read
// worth replaying from cache and a write that must be queued in order. A
// service worker cannot make that distinction, and guessing would mean
// answering a write with a lie.
//
// Strategy is stale-while-revalidate: open instantly from cache (the point of
// the whole exercise), then refresh in the background so a new deploy is
// picked up on the next load rather than never.
const CACHE = 'ask-shell-v1';
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

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (!cacheable(url)) return;          // Supabase and everything else: untouched
  if (url.pathname.endsWith('/tests.html')) return;   // never serve tests from cache

  e.respondWith((async () => {
    const cached = await caches.match(req);
    const network = fetch(req).then((res) => {
      if (res && res.ok) caches.open(CACHE).then((c) => c.put(req, res.clone())).catch(() => {});
      return res;
    }).catch(() => null);
    // Cache first so the car ride works, network behind it so deploys land.
    return cached || (await network) || new Response('offline', { status: 503 });
  })());
});
