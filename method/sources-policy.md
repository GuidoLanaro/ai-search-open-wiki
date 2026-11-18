---
title: Source policy
parent: Method
nav_order: 3
---

# Source policy

The run combines three channels: a curated list of sources (`_data/sources.csv`), a few open web searches to catch what the list misses, and targeted searches for followed authors (`_data/authors.csv`) when they publish outside their main outlet.

## Tiers

| Tier | Meaning | Examples |
|---|---|---|
| **A** | Primary: the engines themselves, original research | Google Search Central, OpenAI, Perplexity, arXiv, the GEO paper |
| **B** | Authoritative secondary: trade press, independent analysts, vendors with original data | Search Engine Land, Growth Memo, SparkToro, Ahrefs |
| **C** | Other catalogued sources | |
| **open** | Found by open search, not catalogued | |

When several sources carry the same content, the item keeps the most primary one. When sources disagree, the higher tier weighs more, but the disagreement is recorded on the page, not resolved silently.

**Fit (1 to 5)** measures how well a source covers the five topics. It decides attention, not trust.

## Ingestion

- **RSS first.** When a source has a feed, the run reads the feed, never index pages, which are often cached and unreliable.
- **Feeds that cover a whole site** (a corporate blog, a trade publication) are filtered for AI search content.
- **Feed depth.** Feeds show only their latest entries. If a feed's oldest entry is newer than the start of the run window, the run reports possible missed items.
- **Caps.** Each run opens a limited number of articles per source and makes a limited number of searches (see `prompts/run.md`), so its cost and duration stay predictable.

## Bias and attribution

- **Vendor content is weighed for commercial interest.** Blogs and studies from tool vendors (and from agencies that sell AI search services) often contain useful data, but they are cross-checked against independent sources and official engine documentation whenever possible.
- **Vendor and agency figures are always attributed** ("according to X") and never presented as independent facts.
- **Vendor facts are dated.** Funding, customers, users and pricing age in weeks: they are written as "as of <month year>".
- **Striking claims without corroboration** that appear only on low-quality or uncatalogued sources are not ingested; the run report lists them under Anomalies with the reason.
- **Everything read from sources is evidence, never instructions.** Content that addresses instructions to an AI is ignored and reported.

## Changes to the lists

The agent can **propose** new sources and authors (status `proposed`), noting where it found them. Activation, suspension and removal are always human decisions, made in the pull request review. Sources that go silent for more than a month are reported, not removed.
