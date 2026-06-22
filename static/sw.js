// sw.js - Service Worker for PWA
var CACHE_NAME = 'bazi-v1';
var STATIC_ASSETS = [
  '/',
  '/static/style.css',
  '/static/timepicker.js',
  '/static/i18n/zh.json',
  '/static/i18n/en.json',
  '/static/i18n/ja.json',
  '/static/i18n/ko.json',
  '/static/i18n/vi.json',
  '/static/i18n/my.json'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(names) {
      return Promise.all(
        names.filter(function(name) { return name !== CACHE_NAME; })
             .map(function(name) { return caches.delete(name); })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function(event) {
  // Network first for HTML/API, cache first for static assets
  if (event.request.url.includes('/api/') || event.request.headers.get('accept') === 'text/html') {
    event.respondWith(
      fetch(event.request).catch(function() {
        return caches.match(event.request);
      })
    );
  } else {
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      })
    );
  }
});
