---
title: Taxonomy
parent: Method
nav_order: 2
---

# Taxonomy

Every item in the log gets one to three topic tags. Each topic has a page that the agent keeps up to date; the *Sources* list at the bottom of each page is generated from the items tagged with that topic.

## Relevance test

An item enters the wiki if it changes what a practitioner should **do**, **measure** or **believe** about visibility in AI answer engines.

Readers are the people who work on that visibility: marketing, SEO and content leads, and the consultants who advise them. New data, new methods, documented changes in engine behaviour and well-evidenced cases pass the test. Thin, promotional, repetitive or speculative content does not. Findings specific to B2B are labelled as such in the summary; B2B is a label, not a filter.

## The five topics

### 1. How answer engines work
Source selection, citation, retrieval (RAG, grounding, query fan-out), AI crawler behaviour. The technical foundation for everything else.

### 2. Content optimization
Structure, schema markup, formats that get cited, crawlability. What to do in practice.

### 3. Measurement and impact
Tools, metrics and methods for measuring visibility and traffic from answer engines; data on click loss and user behaviour. Measurement and impact are two sides of the same question and share one page; they will be split only if the page grows too large.

### 4. Vendors and tools
The landscape of AI visibility tracking and optimization tools: features, methods, pricing, funding, acquisitions.

### 5. Case studies and benchmarks
Applied evidence, with its methods and limits.

## Classification rules

- **One to three topics per item.** More than three is a sign that the summary is too generic: keep the two or three that dominate.
- **Dominant topic first.** The first topic is the item's canonical home: its full detail goes on that page, and other pages get a one-line pointer. No paragraph is duplicated across pages.
- **No forcing.** An item that does not fit any topic with conviction is dropped.

## Outside the taxonomy

The **vendor watchlist** (`_data/vendors.csv`) is checked at every run, but it is not a topic: vendor movements are reported in the run report and only reach topic 4 when they change the landscape. The list is data, never hardcoded in the prompt.
