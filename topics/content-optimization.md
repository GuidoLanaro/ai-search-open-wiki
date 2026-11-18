---
title: Content optimization
parent: Topics
nav_order: 2
topic_id: "2"
---

# Content optimization

*What makes content more likely to be retrieved and cited: structure, schema markup, formats, crawlability for AI crawlers.*

## State of the art

**What the engine owner says**
- As of May 2026, Google's guide says generative AI features rest on core Search ranking and quality systems, that it does not treat AEO or GEO as separate disciplines, and that mass-producing pages for query variations is scaled content abuse. It recommends original content with first-hand experience and a distinct point of view, solid technical basics, and Merchant Center and Business Profile feeds for commerce and local. [Google guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [announcement](https://developers.google.com/search/blog/2026/05/a-new-resource-for-optimizing) [single source: official documentation]
- As of May 2026, the same guide says Google Search does not use llms.txt or Markdown files, that content chunking, special phrasing for AI and special schema are not needed, and that manufactured mentions do not help. [Google guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) [single source: official documentation]
- As of November 2026, Google requires only indexing and snippet eligibility for AI Overviews and AI Mode; no additional markup or files. [Google Search Central](https://developers.google.com/search/docs/appearance/ai-features) [single source: official documentation]

**What studies suggest**
- As of November 2026, off-site presence correlates with AI visibility: in 260M prompts for 10,000 US brands, Reddit ranking-thread mentions correlated at 0.75, webpage mentions 0.70, news 0.67 and YouTube 0.64 with AI mentions; a 10x rise in webpage mentions went with about 3.7x more AI mentions. Correlation, partly explained by brand size. [Ahrefs](https://ahrefs.com/blog/mention-types-ai-visibility) [single source: vendor]
- As of 2026, listicles are heavily cited but self-promotional ones often do not earn the recommendation: the brand was cited yet omitted in about 69% of 100 B2B queries. [Search Engine Land](https://searchengineland.com/google-ai-overviews-cite-self-serving-listicles-recommend-competitors-480573) [corroborated: a preprint also found ranked listicles to be the top cited format, about 21% of citations, see [Case studies and benchmarks](case-studies-and-benchmarks.html)]
- As of November 2026, Ahrefs found no statistically meaningful change in ChatGPT citations after adding structured data in one of its studies, which is consistent with Google's statement that no special schema exists for AI features. [Ahrefs](https://ahrefs.com/blog/where-does-chatgpt-get-its-information) [single source: vendor]
- As of July 2026, a survey of the GEO literature finds that citation-oriented rewrites can impair retrieval and that gains from generic tactics are not shown to increase organic discoverability. [Critical GEO survey](https://arxiv.org/abs/2607.14035) [single source: preprint]. See [How answer engines work](how-answer-engines-work.html) for the retrieval detail.

## Open contradictions

- **Is there special optimization for AI search?** Google says it is still SEO with no special markup or files ([guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)); the original GEO paper reports content tactics can lift visibility by up to 40% ([paper](https://arxiv.org/abs/2311.09735)), and the 2026 survey says that holds only for already-retrieved content ([survey](https://arxiv.org/abs/2607.14035)). Google also advises against the chunking and rewriting that many practitioners recommend; no independent test of that was ingested this run.
- **Off-site mentions.** Google says manufactured mentions are not helpful ([guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)); Ahrefs finds mentions strongly correlated with AI visibility, without showing causation ([Ahrefs](https://ahrefs.com/blog/mention-types-ai-visibility)). These claims address different things (inauthentic versus organic mentions) and are kept side by side.

## Last updated

2026-11-18, run 2026-11-18 (run zero).

## Sources

{% include topic-sources.html %}
