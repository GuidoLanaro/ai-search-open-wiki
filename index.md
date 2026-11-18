---
title: Home
nav_order: 1
---

# AI Search Open Wiki
{: .fs-9 }

An open, agent-maintained wiki on visibility in AI answer engines.
{: .fs-6 .fw-300 }

How do Google AI Overviews and AI Mode, ChatGPT search, Perplexity, Copilot and Claude choose which sources to cite? What can be done about it, and how can it be measured? This wiki keeps a running, sourced answer to those questions for the people who work on visibility in AI answer engines.

## Topics

| Topic | Covers |
|---|---|
| [How answer engines work](topics/how-answer-engines-work.html) | Source selection, citation, retrieval, AI crawlers |
| [Content optimization](topics/content-optimization.html) | Structure, markup, formats that get cited, crawlability |
| [Measurement and impact](topics/measurement-and-impact.html) | Tools, metrics, click loss, user behaviour |
| [Vendors and tools](topics/vendors-and-tools.html) | The vendor landscape, features, funding, acquisitions |
| [Case studies and benchmarks](topics/case-studies-and-benchmarks.html) | Applied evidence |

## How to read it

- Every claim carries a **date**, a **link** to its source and a **confidence label**: `[corroborated]` when several independent sources agree, `[single source]` otherwise.
- **Open contradictions** are listed on each page: where sources disagree, both positions are shown.
- Figures published by vendors and agencies are **attributed** ("according to X"), not stated as facts.

## How it is made

Every two weeks an AI agent collects what was published since the last run from a [curated set of sources](method/sources-policy.html), the open web and a list of followed authors, then proposes new items and page edits in a pull request. A human reviews every change before it is published. The [run reports](runs/) show what each run found and why each page changed; the [method](method/) section documents the design and its decision log.

{% assign last_run = site.pages | where: "parent", "Runs" | sort: "title" | last %}
{% if last_run %}Latest run: [{{ last_run.title }}]({{ last_run.url | relative_url }}).{% endif %}
