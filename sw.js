/* Economya : service worker minimal.
   Rend le site installable sur l'écran d'accueil. Il ne met AUCUNE page en cache :
   le contenu vient toujours du réseau, donc jamais de version périmée.
   Seule exception : si la connexion est coupée, on affiche une petite page « hors connexion ». */
var VERSION = 'eco-offline-v1';
var OFFLINE_URL = '/offline';

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(VERSION)
      .then(function (cache) { return cache.add(OFFLINE_URL); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (keys) {
        return Promise.all(keys.filter(function (k) { return k !== VERSION; }).map(function (k) { return caches.delete(k); }));
      })
      .then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (event) {
  // On ne touche qu'à la navigation entre pages ; tout le reste (API, images, scripts) passe tel quel.
  if (event.request.mode !== 'navigate') return;
  event.respondWith(
    fetch(event.request).catch(function () { return caches.match(OFFLINE_URL); })
  );
});
