import csv
import os
from datetime import datetime, timezone

import requests

URL = "https://api.mainnet.cipherscan.app/api/privacy-stats"
os.makedirs("data", exist_ok=True)

response = requests.get(URL, timeout=30)
response.raise_for_status()
data = response.json()

# 1. Save today's balance for each pool (one new row per run)
pools = data["shieldedPool"]
row = {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "sprout": pools["sprout"],
    "sapling": pools["sapling"],
    "orchard": pools["orchard"],
    "ironwood": pools["ironwood"],
    "total": pools["currentSize"],
}
path = "data/pool_snapshots.csv"
new_file = not os.path.exists(path)
with open(path, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(row.keys()))
    if new_file:
        writer.writeheader()
    writer.writerow(row)

# 2. Keep the 30-day combined history and let it grow past 30 days
daily_path = "data/daily_totals.csv"
fields = ["date", "shielded", "transparent", "shieldedPercentage", "poolSize", "privacyScore"]
history = {}
if os.path.exists(daily_path):
    with open(daily_path, newline="") as f:
        for d in csv.DictReader(f):
            history[d["date"]] = d
for d in data["trends"]["daily"]:
    history[d["date"]] = d
with open(daily_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for date in sorted(history):
        writer.writerow(history[date])

print("Saved snapshot and", len(history), "days of history")
