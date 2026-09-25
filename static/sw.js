/**
 * SautiCare Service Worker (Offline Resilience & PWA Support - v2)
 * Ensures African elders can access emergency SOS and phone guides even with 0MB data.
 * Uses Network-First with Cache-Fallback to guarantee real-time updates.
 */

const CACHE_NAME = "sauticare-v2";
const STATIC_ASSETS = [
  "/",
  "/static/style.css?v=2.2",
  "/static/app.js?v=2.2",
  "/manifest.json",
  "/static/icon.svg",
  "/static/icon-192.png",
  "/static/icon-512.png"
];

// Install Event: Pre-cache core app shell
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("[SautiCare SW v2] Caching app shell assets...");
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Activate Event: Clean up stale caches immediately
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log("[SautiCare SW v2] Removing old cache:", key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event: Network-first for shell and static, with offline fallback
self.addEventListener("fetch", (event) => {
  const request = event.request;
  const url = new URL(request.url);

  // 1. Navigation requests (HTML page): Network first, fallback to cached index.html
  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request).catch(() => {
        return caches.match("/");
      })
    );
    return;
  }

  // 2. Static Assets (CSS, JS, Icons, Images): Network first, fallback to Cache
  if (url.pathname.startsWith("/static/") || url.pathname === "/manifest.json") {
    event.respondWith(
      fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone));
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(request);
        })
    );
    return;
  }

  // 3. API Requests: Network first, fallback to offline JSON if disconnected
  if (url.pathname.startsWith("/api/")) {
    event.respondWith(
      fetch(request).catch(() => {
        if (url.pathname === "/api/health") {
          return new Response(JSON.stringify({
            status: "offline_mode",
            service: "SautiCare Offline Lifeline",
            offline_support: true,
            assemblyai_configured: false
          }), { headers: { "Content-Type": "application/json" } });
        }
        // Fallback response for process-text when offline
        return new Response(JSON.stringify({
          action: "offline_guide",
          is_emergency: false,
          swahili_response: "Uko nje ya mtandao kwa sasa. Simu za dharura na huduma ya simu bado zinafanya kazi bila bando.",
          english_translation: "You are offline. Emergency calls and USSD dialer still work without internet data.",
          visual_card: {
            type: "device_action",
            title: "Hali ya Nje ya Mtandao (Offline) 📶",
            details: "Simu za dharura na kodi za simu (*334#, *144#) zinafanya kazi kawaida."
          }
        }), { headers: { "Content-Type": "application/json" } });
      })
    );
    return;
  }

  // Default: Network fetch
  event.respondWith(fetch(request));
});
