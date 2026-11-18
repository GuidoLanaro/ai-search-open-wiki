---
title: How answer engines work
parent: Topics
nav_order: 1
topic_id: "1"
---

# How answer engines work

*How AI answer engines select, retrieve and cite sources: retrieval and grounding, query fan-out, citation behaviour, AI crawlers. The technical foundation for the other topics.*

## State of the art

**Retrieval and query fan-out**
- As of November 2026, Google documents that AI Overviews and AI Mode may issue several related searches across subtopics (query fan-out), which lets them show a wider set of links than classic Search; the two features may use different models, so their links can differ. [Google Search Central](https://developers.google.com/search/docs/appearance/ai-features) [single source: official documentation]
- As of November 2026, Ahrefs describes ChatGPT as writing its own search queries, with about 1.6 queries per response in its tests, and reports 83% of answers to brand questions cited the brand's own site. [Ahrefs](https://ahrefs.com/blog/where-does-chatgpt-get-its-information) [single source: vendor]
- As of November 2026, a meta-analysis cites an AirOps study in which 85% of retrieved pages were never cited and 32.9% of cited pages ranking in the top 20 appeared only for a fan-out query. [Growth Memo](https://www.growth-memo.com/p/ai-search-meta-analysis-q4-2026) [single source: secondary report of a vendor study]

**Citation selection**
- As of July 2026, a survey of 45 GEO studies finds topical relevance and position within the retrieved context are the most reproducible levers, generic heuristics transfer poorly across engines, and the original GEO gains hold only for sources already in the context. [Critical GEO survey](https://arxiv.org/abs/2607.14035) [single source: preprint, not peer reviewed]. The original paper reported gains of up to 40% in visibility. [Aggarwal et al.](https://arxiv.org/abs/2311.09735)
- As of November 2026, Ahrefs finds off-site mentions correlate with AI mentions, strongest for Reddit ranking threads (0.75) and weakest for ChatGPT; brand size explains part of the link and causation is not shown. [Ahrefs](https://ahrefs.com/blog/mention-types-ai-visibility) [single source: vendor]. Content-format detail is on [Content optimization](content-optimization.html).
- As of 2026, a study of 100 B2B "best" queries found that a brand's own listicle was cited in AI Overviews but the brand was omitted from the recommendation in about 69% of cases. [Search Engine Land](https://searchengineland.com/google-ai-overviews-cite-self-serving-listicles-recommend-competitors-480573) [single source; accessed through secondary coverage]
- As of May 2026, a benchmark of ranking-manipulation methods found simple black-box rewriting matched or beat gradient-based attacks on a small open model and could evade some detectors, a reminder that citation signals can be gamed. [GEO-Bench](https://arxiv.org/abs/2605.29107) [single source: preprint]
- Citation persistence is short: as of September 2026, Profound reports a median citation half-life of 11 days across 883,000 pages and seven engines. Full detail on [Measurement and impact](measurement-and-impact.html). [Profound](https://www.tryprofound.com/blog/the-half-life-of-an-ai-citation-is-11-days) [single source: vendor]

**Crawlers, controls and data sources**
- As of October 2026, Google supports a shared robots.txt token for AI training preferences (draft IETF AIPREF work), treated as a Google-Extended disallow; sites that allow Google-Extended can be eligible for Gemini Apps grounding responses. Google plans support in 2027. [Google Search Central Blog](https://developers.google.com/search/blog/2026/10/ai-training-control) [single source: official announcement]
- As of November 2026, Google states that AI features need only normal indexing and snippet eligibility, with preview limits set through nosnippet, data-nosnippet, max-snippet or noindex. [Google Search Central](https://developers.google.com/search/docs/appearance/ai-features) [single source: official documentation]
- As of November 2026, ChatGPT answers draw on training data, live search, licensed publisher content and user context, according to Ahrefs, which also reports only about 8% of ChatGPT citations rank in the Google or Bing top 10 for the same prompt. [Ahrefs](https://ahrefs.com/blog/where-does-chatgpt-get-its-information) [single source: vendor]

**Pointers**
- Usage data on how people use ChatGPT (6.9% of prompts involve researching a brand to buy from): see [Measurement and impact](measurement-and-impact.html).

## Open contradictions

- **How closely citations follow classic rankings.** Ahrefs reports about 8% of ChatGPT citations in the Google or Bing top 10 ([Ahrefs](https://ahrefs.com/blog/where-does-chatgpt-get-its-information)); Google says generative features are rooted in core ranking and quality systems ([Google guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)). The measures, engines and dates differ, and none of these is a controlled comparison.
- **Do generic GEO tactics work?** The original GEO paper reports gains of up to 40% ([paper](https://arxiv.org/abs/2311.09735)); the 2026 survey argues these gains hold only for already-retrieved content and do not show organic discoverability ([survey](https://arxiv.org/abs/2607.14035)).

## Last updated

2026-11-18, run 2026-11-18 (run zero).

## Sources

{% include topic-sources.html %}
