---
title: How answer engines work
parent: Topics
nav_order: 1
topic_id: "1"
---

# How answer engines work

*How AI answer engines select, retrieve and cite sources: retrieval and grounding, query fan-out, citation behaviour, AI crawlers. The technical foundation for the other topics.*

## State of the art

**Retrieval and fan-out**
- As of 2025 (undated documentation), Google says AI Overviews and AI Mode may run several related searches across subtopics to assemble an answer, so they can surface a wider set of links than classic search ([Google Search Central](https://developers.google.com/search/docs/appearance/ai-features)). [single source]
- As of April 2026, according to Peec AI, ChatGPT averages 2.1 fan-outs per prompt, Perplexity 1.4 and Grok 6.8; ChatGPT adds terms such as "best" and "reviews", while Perplexity mostly reruns a cleaned-up query ([Peec AI](https://docs.peec.ai/research/fanouts-per-prompt-by-engine)). [single source]

**Citation and ranking overlap**
- As of September 2025, according to Ahrefs, Perplexity's cited URLs matched Google's top 10 for about 65% of short-tail keywords, against 10% for ChatGPT; ChatGPT cited ranking domains about three times more often than ranking pages ([Ahrefs](https://ahrefs.com/blog/chatgpt-google-citations)). The cause (a ChatGPT re-ranking layer) is Ahrefs' hypothesis, not a measured fact. [single source]
- Engines therefore should not be treated as one system: ranking well on Google is a much closer proxy for Perplexity than for ChatGPT.

**Crawlers**
- As of August 2026, OpenAI documents that ChatGPT-User, which fetches pages on a user's request, may not follow robots.txt; OAI-SearchBot is the agent that governs inclusion in ChatGPT search. TollBit's H1 2026 data, as reported by Search Engine Journal, found about 15% of identified AI page-fetchers on European sites reached disallowed URLs ([Search Engine Journal](https://www.searchenginejournal.com/openai-says-robots-txt-may-not-apply-to-chatgpts-fetch-bot/585864/)). [single source] Practical detail in [Content optimization](content-optimization.html).

**Foundations**
- The original GEO paper (November 2023) framed visibility in generative engines as an optimization problem; see [Content optimization](content-optimization.html) for its findings ([arXiv](https://arxiv.org/abs/2311.09735)).

## Open contradictions

*None recorded yet.*

## Last updated

2026-11-18, run zero ([report](../runs/2026-11-18.html)).

## Sources

{% include topic-sources.html %}
