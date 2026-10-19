# ZEC Flow Digest

An open dataset and live dashboard that tracks how much ZEC moves into and out of Zcash's shielded pools each day, using only public aggregate data.

Built for **ZECATHON** (Core & Tooling track).

- **Live dashboard:** https://kellyonchain.github.io/zec-flow-digest/
- **Open data:** [`data/daily_totals.csv`](data/daily_totals.csv) and [`data/pool_snapshots.csv`](data/pool_snapshots.csv)

## What it does

A GitHub Action runs every six hours (00:05, 06:05, 12:05 and 18:05 UTC). It calls CipherScan's public API and saves two things to this repo:

1. The combined shielded pool balance for each day (the API provides the latest 30 days, and this repo keeps adding to them).
2. A snapshot of each pool's balance (Sprout, Sapling, Orchard, Ironwood).

The dashboard reads those CSV files and shows daily net flow, total shielded supply, the pool split, and pool balances over time.

## Why track the combined total

Shielded supply is split across four pools, and coins move between them (for example from Orchard to Ironwood). Looking at one pool alone can make a transfer look like an inflow or outflow. This project measures the **combined** balance of all shielded pools, so a move between pools cancels out and only ZEC entering or leaving the shielded pools counts as flow.

Net flow for a day = that day's combined shielded balance minus the previous day's.

## Privacy

This project reads only public pool totals. It never touches addresses, notes, viewing keys or individual transactions, so it reveals nothing about any user and cannot link a shielded transaction to a person.

## Open data

**`data/daily_totals.csv`** (one row per day)

| Column | Meaning |
|---|---|
| `date` | UTC date |
| `poolSize` | Combined balance of all shielded pools, in ZEC |
| `shielded`, `transparent`, `shieldedPercentage` | Daily activity figures as reported by CipherScan's API (see their docs for exact definitions) |
| `privacyScore` | CipherScan's composite privacy score |

**`data/pool_snapshots.csv`** (one row per collector run)

| Column | Meaning |
|---|---|
| `timestamp_utc` | When the snapshot was taken |
| `sprout`, `sapling`, `orchard`, `ironwood` | Balance of each pool, in ZEC |
| `total` | Combined shielded balance, in ZEC |

Anyone is free to reuse the CSV files. They are served publicly from the live site's `data/` folder.

## How it works

- `collect.py` fetches the API response and updates the two CSV files (Python, `requests` only).
- `.github/workflows/collect.yml` runs it every six hours and commits the new data.
- `index.html` is a single static page (Chart.js) served by GitHub Pages.

To run the collector yourself:

```
pip install requests
python collect.py
```

## What is real and what is not

Real: the daily collection, the stored history, the net flow calculation and the live dashboard, all running on public data.

Not included: no wallet, no node, no direct chain parsing. The data comes from CipherScan's API, so this project depends on it.

## Limitations

- The API only provides the latest 30 days of combined history. Per-pool history starts at the first snapshot (2026-10-17) and grows each day.
- The current UTC day is partial, so the dashboard draws it faded and leaves it out of the headline and totals until it completes.
- The data shows how much moved, not why. For example, 2026-09-30 shows a single-day increase of about 49,395 ZEC that this data does not explain.
- Shielded transactions are private by design, so this cannot show who moved the coins.

## Data source

Pool and supply data comes from [CipherScan](https://cipherscan.app)'s public API. No CipherScan code is used here.

## Next steps

- Find and document the cause of the Sep 30 jump.
- Add longer per-pool history if a source for it is available.
- Mark key network events on the charts.
