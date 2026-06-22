"""
Simple in-memory cache with TTL and LRU eviction for BaZi calculations.
Same input parameters always produce the same result, so caching saves significant CPU time.
"""
import time
import hashlib
import threading

class BaziCache:
    def __init__(self, max_size=500, ttl_seconds=3600):
        self._cache = {}
        self._lock = threading.Lock()
        self._max_size = max_size
        self._ttl = ttl_seconds
        self._hits = 0
        self._misses = 0

    def _make_key(self, **kwargs):
        raw = json.dumps(kwargs, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(raw.encode()).hexdigest()

    def get(self, **kwargs):
        key = self._make_key(**kwargs)
        with self._lock:
            entry = self._cache.get(key)
            if entry and time.time() - entry['time'] < self._ttl:
                self._hits += 1
                return entry['value']
            self._misses += 1
        return None

    def set(self, value, **kwargs):
        key = self._make_key(**kwargs)
        with self._lock:
            if len(self._cache) >= self._max_size:
                oldest_key = min(self._cache, key=lambda k: self._cache[k]['time'])
                del self._cache[oldest_key]
            self._cache[key] = {'value': value, 'time': time.time()}

    def stats(self):
        with self._lock:
            total = self._hits + self._misses
            rate = (self._hits / total * 100) if total > 0 else 0
            return {
                'size': len(self._cache),
                'hits': self._hits,
                'misses': self._misses,
                'hit_rate': f'{rate:.1f}%'
            }

import json
bazi_cache = BaziCache(max_size=500, ttl_seconds=3600)
