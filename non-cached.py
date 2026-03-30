"""
DNS Benchmark - Non-Cached Test

Author: FlareXes
Repo: https://github.com/FlareXes/fastest-dns

Description:
Measures raw DNS resolver performance by querying randomly generated
domains. Each request forces a full DNS lookup, bypassing cache.
"""

import subprocess
import re
import time
import random
import string
import statistics
import math

SERVERS = {
    "Cloudflare": "1.1.1.1",
    "Google": "8.8.8.8",
    "Quad9": "9.9.9.9"
}

RUNS = 20


def random_domain():
    """Generate random domain like dj3k9s8f.com"""
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return f"{name}.com"


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


def test_uncached():
    print("\n=== NON-CACHED DNS TEST ===")
    print(f"Runs per server: {RUNS}")
    print("Using random domains to avoid cache\n")

    results = {}

    for name, ip in SERVERS.items():
        print(f"\n\nTesting {name} ({ip})")

        times = []

        for i in range(1, RUNS + 1):
            domain = random_domain()
            print(f"\r[{i}/{RUNS}] Querying: {domain}      ", end="", flush=True)

            t = query_dns(ip, domain)

            if t:
                times.append(t)
            else:
                print("   -> Failed")

            time.sleep(random.uniform(0.5, 1.0))

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
    data = test_uncached()

    print("\n=== RESULTS ===")
    for k, v in data.items():
        print(f"\n{k}")
        print(f"  Median: {v['median']:.2f} ms")
        print(f"  Avg:    {v['avg']:.2f} ms")
        print(f"  P95:    {v['p95']:.2f} ms")

