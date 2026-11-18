---
title: Content optimization
parent: Topics
nav_order: 2
topic_id: "2"
---

# Content optimization

*What makes content more likely to be retrieved and cited: structure, schema markup, formats, crawlability for AI crawlers.*

## State of the art

**Research basis**
- As of November 2023, the GEO paper (KDD 2024) reported that content-level optimization methods can raise visibility in generative engine responses by up to 40%, with effects that vary by domain ([arXiv](https://arxiv.org/abs/2311.09735)). [single source] It was tested on its own benchmark, not on live commercial engines.

**Official guidance**
- As of 2025, Google states that appearing in AI Overviews and AI Mode requires only being indexed and snippet-eligible, with no special markup, schema.org type or AI-specific file; it recommends allowing crawling, keeping key content in text and keeping structured data consistent with visible text ([Google Search Central](https://developers.google.com/search/docs/appearance/ai-features)). [single source]
- As of 2026, Google's controls for limiting use are nosnippet, max-snippet and noindex, plus a Search Console opt-out toggle for AI Overviews and AI Mode ([Google](https://blog.google/products-and-platforms/products/search/new-controls-website-owners)). [single source]

**Schema markup**
- As of May 2026, according to Ahrefs, 1,885 pages that added JSON-LD showed no meaningful citation lift against matched controls, and a 4.6% drop on Google AI Overviews that Ahrefs notes is hard to attribute to schema; the study cannot speak to pages not yet cited ([Ahrefs](https://ahrefs.com/blog/schema-ai-citations/)). [single source] This is consistent with Google's statement above; vendor claims of large schema lifts were not ingested (see run report).

**Crawler access**
- As of August 2026, blocking GPTBot (training) is not the same as blocking OAI-SearchBot, which governs ChatGPT search inclusion, and ChatGPT-User may ignore robots.txt; check server logs rather than relying on robots.txt alone ([Search Engine Journal](https://www.searchenginejournal.com/openai-says-robots-txt-may-not-apply-to-chatgpts-fetch-bot/585864/)). [single source] Detail in [How answer engines work](how-answer-engines-work.html).
- Fan-out behaviour differs by engine (Peec AI, April 2026); see [How answer engines work](how-answer-engines-work.html).

## Open contradictions

*None recorded yet.*

## Last updated

2026-11-18, run zero ([report](../runs/2026-11-18.html)).

## Sources

{% include topic-sources.html %}
