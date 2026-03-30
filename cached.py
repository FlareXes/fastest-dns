"""
DNS Benchmark - Cached Test

Author: FlareXes
Repo: https://github.com/FlareXes/fastest-dns

Description:
Measures DNS performance under cached conditions by repeatedly querying
the same domain. Simulates real-world browsing where DNS responses are
served from resolver cache.
"""

import subprocess
import re
import time
import random
import statistics
import math

SERVERS = {
    "Cloudflare": "1.1.1.1",
    "Google": "8.8.8.8",
    "Quad9": "9.9.9.9"
}

DOMAIN = "google.com"
RUNS = 20


def query_dns(server, domain):
    """Run dig and extract query time in ms"""
    result = subprocess.run(
        ["dig", f"@{server}", domain],
        capture_output=True,
        text=True
    )
    match = re.search(r"Query time: (\d+)", result.stdout)
    return int(match.group(1)) if match else None


def calculate_p95(data):
    """Calculate P95 from a sorted list"""
    sorted_data = sorted(data)
    index = math.ceil(0.95 * len(sorted_data)) - 1
    return sorted_data[index]


def test_cached():
    print("\n=== CACHED DNS TEST ===")
    print(f"Domain: {DOMAIN}")
    print(f"Runs per server: {RUNS}\n")

    results = {}

    for name, ip in SERVERS.items():
        print(f"\n\nTesting {name} ({ip})")

        # Warm-up queries
        for _ in range(3):
            query_dns(ip, DOMAIN)

        times = []

        for i in range(1, RUNS + 1):
            print(f"\r[{i}/{RUNS}] Querying: {DOMAIN}      ", end="", flush=True)

            t = query_dns(ip, DOMAIN)

            if t:
                times.append(t)
            else:
                print(f"[{i}/{RUNS}] Failed")

            time.sleep(random.uniform(0.1, 0.3))

        if times:
            avg = sum(times) / len(times)
            median = statistics.median(times)
            p95 = calculate_p95(times)

            results[name] = {
                "avg": avg,
                "median": median,
                "p95": p95
            }

    return results


if __name__ == "__main__":
    data = test_cached()

    print("\n\n=== CACHED DNS RESULTS ===")
    for k, v in data.items():
        print(f"\n{k}")
        print(f"  Median: {v['median']:.2f} ms")
        print(f"  Avg:    {v['avg']:.2f} ms")
        print(f"  P95:    {v['p95']:.2f} ms")
