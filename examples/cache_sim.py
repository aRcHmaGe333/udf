#!/usr/bin/env python3
import random

def simulate(requests=1000, reuse_prob=0.8, cache_size=100):
    cache = set()
    hits = 0
    universe = 1000
    last = None
    for _ in range(requests):
        if last is None or random.random() > reuse_prob:
            req = random.randint(0, universe-1)
        else:
            req = last  # reuse
        last = req
        if req in cache:
            hits += 1
        else:
            cache.add(req)
            if len(cache) > cache_size:
                cache.pop()  # naive eviction for demo
    hit_rate = hits/requests
    print(f"Requests: {requests}")
    print(f"Approx hit rate: {hit_rate:.2f}")
    print(f"WAN savings ~ hit rate: {hit_rate:.2f}")

if __name__ == '__main__':
    simulate()

