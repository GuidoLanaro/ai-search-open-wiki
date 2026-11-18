---
title: Data schema
parent: Method
nav_order: 4
---

# Data schema

The wiki keeps its structured data in four CSV files in `_data/`. The site reads them directly; the agent writes them only through `scripts/data.py`, which enforces this schema. The same checks run in CI on every pull request (`python scripts/data.py validate`).

**Format:** UTF-8, comma-separated, header row, fields quoted only when needed. Dates are `YYYY-MM-DD`. Empty means "not set".

**Status values** (sources, authors, vendors):
- `active`: used by the run;
- `proposed`: suggested by the agent, waiting for a human decision (sources and authors only);
- `suspended`: kept for history, ignored by the run.

Activation, suspension and removal are always human decisions.

## items.csv — the item log

One row per item. Append-only: existing rows are never modified or deleted.

| Column | Required | Values |
|---|---|---|
| `url` | yes | Canonical URL, without tracking parameters or fragment. Unique (deduplication key, see below). |
| `title` | yes | Title of the original piece. |
| `published` | yes | Publication date of the original. `YYYY-MM` or `YYYY` accepted when the day is not exposed. |
| `ingested` | yes | Date of the run that added the item. |
| `source_id` | no | `id` of a row in `sources.csv`. Empty when found by open search or through an author outside the catalogued sources. |
| `tier` | yes | `A`, `B`, `C` or `open`. |
| `topics` | yes | 1 to 3 topic numbers from 1 to 5, separated by `;` (e.g. `1;3`). The first is the dominant topic. |
| `type` | yes | `product-news`, `study-data`, `case-study`, `analysis-opinion`. |
| `summary` | yes | 2 to 3 factual sentences, in our own words, with key figures. |

There is no status column: an item in an open pull request is under review, a merged item is published, an item removed before merge is discarded.

## sources.csv — curated sources

| Column | Required | Values |
|---|---|---|
| `id` | yes | Short slug, unique (e.g. `search-engine-land`). |
| `name` | yes | |
| `url` | yes | Main URL. Unique. |
| `feed` | no | RSS/Atom feed URL: the preferred ingestion channel. |
| `tier` | yes | `A` (primary: engines, original research), `B` (authoritative secondary), `C` (other). |
| `fit` | yes | 1 to 5: how well the source covers the five topics. |
| `cadence` | yes | `daily`, `weekly`, `monthly`, `irregular`. |
| `status` | yes | `active`, `proposed`, `suspended`. |
| `notes` | no | Coverage, biases, caveats (e.g. vendor conflict of interest). |

## authors.csv — followed authors

Authors whose work also appears outside their main publication. The run searches for them by name.

| Column | Required | Values |
|---|---|---|
| `id` | yes | Short slug, unique. |
| `name` | yes | |
| `main_publication` | no | URL of the publication already covered by `sources.csv`. |
| `profile` | no | Personal site or newsletter. |
| `tier` | yes | `A`, `B` or `C`: used for items found through this author on publications not in `sources.csv`. |
| `status` | yes | `active`, `proposed`, `suspended`. |
| `notes` | no | Context; for proposals, where the author was found. |

## vendors.csv — vendor watchlist

Vendors whose changelog or blog is checked at every run. Outside the topic taxonomy: movements go to the run report.

| Column | Required | Values |
|---|---|---|
| `id` | yes | Short slug, unique. |
| `name` | yes | |
| `url` | yes | Main URL. |
| `changelog` | no | Changelog, release notes or blog checked at each run. |
| `last_move` | no | Latest movement, one line. Updated by the run. |
| `last_move_date` | no | Date of the latest movement. Updated by the run. |
| `status` | yes | `active` or `suspended`. Vendors are added by humans only. |
| `notes` | no | Context, biases. |

The run may change only `last_move` and `last_move_date`, and only for active vendors.

## Deduplication key

Two URLs are the same item when they match after normalization:
- scheme and host lower-cased, `www.` and default ports dropped, `http` and `https` treated as equal;
- fragment removed;
- tracking parameters removed (`utm_*`, `gclid`, `fbclid`, `mc_cid`, `mc_eid`, `_hsenc`, `_hsmi`, `mkt_tok`, `ref`, `ref_src`, `igshid` and similar);
- trailing slash removed from the path.

`python scripts/data.py normalize <url>` shows the stored form; `python scripts/data.py seen <url>` checks the log.
