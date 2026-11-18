---
title: Measurement and impact
parent: Topics
nav_order: 3
topic_id: "3"
---

# Measurement and impact

*How visibility and traffic from answer engines are measured, and what the data says about click loss and user behaviour.*

## State of the art

**First-party measurement**
- As of June 2026, Google introduced Search Console reports on generative AI performance (impressions, pages, countries; no click data; data from 18 May 2026) and an opt-out toggle for AI Overviews, AI Mode and AI Overviews in Discover; Google's note says both had reached all sites worldwide by 31 August 2026 ([Google](https://blog.google/products-and-platforms/products/search/new-controls-website-owners)). [single source] Before that, AI feature traffic was folded into the Web search type ([Google Search Central](https://developers.google.com/search/docs/appearance/ai-features)).
- Practical consequence: impressions in AI features can now be measured first-party, but clicks from them cannot be separated.

**Click loss: experimental evidence**
- As of August 2026, a preregistered field experiment with 1,100 US participants (preprint, not peer reviewed) found that removing AI Overviews and AI Mode raised click-through to publishers, and an AI Mode-only experience lowered it and reduced trust in Google ([arXiv](https://arxiv.org/abs/2608.18352)). Secondary coverage reports about -18.8 points of external clicks under forced AI Mode and +8.8 points with AI hidden; these figures were not confirmed from the paper's abstract. [single source]

**Case-level evidence**
- As of October 2026, a single-site opt-out test by Cyrus Shepard estimated about 0.9% CTR on AI impressions (about 8% of the site's impressions) and saw regular organic clicks fall too; the author and the report both call it very small ([Search Engine Roundtable](https://www.seroundtable.com/google-ai-mode-ctr-42421.html)). [single source] Treat as an illustration of the new toggle's use, not as a benchmark; see [Case studies and benchmarks](case-studies-and-benchmarks.html).

## Open contradictions

- **How much do AI features cost publishers in clicks?** The experiment above (August 2026) finds a substantial drop in external clicks when AI Mode is forced, while the Shepard test (October 2026) finds a very low CTR on AI impressions but organic clicks that also fell when the site opted out, which points the other way for organic. The designs differ (population experiment vs one site, forced exposure vs opt-out), so they are not directly comparable. Sources: [arXiv](https://arxiv.org/abs/2608.18352), [Search Engine Roundtable](https://www.seroundtable.com/google-ai-mode-ctr-42421.html).

## Last updated

2026-11-18, run zero ([report](../runs/2026-11-18.html)).

## Sources

{% include topic-sources.html %}
