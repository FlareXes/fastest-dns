# DNS Benchmark: Cached vs Non-Cached Performance

- `cached.py` → Measures cached DNS performance
- `non-cached.py` → Measures uncached DNS performance using random domains

# Requirements
- Python 3.x
- `dig` command available (install via `dnsutils` or `bind-tools`)

# Example Usage
```
$ python cached.py

=== CACHED DNS TEST ===
Domain: google.com
Runs per server: 20


Testing Cloudflare (1.1.1.1)
[20/20] Querying: google.com

Testing Google (8.8.8.8)
[20/20] Querying: google.com

Testing Quad9 (9.9.9.9)
[20/20] Querying: google.com

=== CACHED DNS RESULTS ===

Cloudflare
  Median: 5.00 ms
  Avg:    6.10 ms
  P95:    19.00 ms

Google
  Median: 4.00 ms
  Avg:    5.65 ms
  P95:    18.00 ms

Quad9
  Median: 4.00 ms
  Avg:    5.65 ms
  P95:    20.00 ms
```

# Metrics Explanation

Each script outputs:

- **Median (P50)** → Typical response time (what users usually experience)
- **Average (Avg)** → Overall performance, but can be misleading due to spikes
- **P95** → 95% of queries are faster than this value. Reveals latency spikes and instability

👉 Key idea:
Average shows speed. Median shows reality. P95 shows pain.

# Recommended Settings

You can modify these values inside the scripts.

Default:
`RUNS = 20`

Suggested:
- Minimum: 20
- Ideal: 30–50

# Adding More DNS Providers

Edit this section in both scripts:

SERVERS = {
    "Cloudflare": "1.1.1.1",
    "Google": "8.8.8.8",
    "Quad9": "9.9.9.9"
}

Example additions:
- "OpenDNS": "208.67.222.222",
- "AdGuard": "94.140.14.14"

# License
Licensed under [MIT](LICENSE). Use freely and modify aggressively.
