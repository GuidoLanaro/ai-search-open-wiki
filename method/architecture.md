---
title: Architecture
parent: Method
nav_order: 1
---

# Architecture

*Last updated: 2026-11-18*

## Components

1. **Trigger.** A GitHub Actions workflow (`.github/workflows/run.yml`) runs at night on the 1st and 15th of each month, and can be started manually. If the pull request of the previous run is still open, the run fails with an explicit message (so GitHub notifies the maintainer) instead of covering the same window twice.
2. **Agent.** The workflow installs the Claude Code CLI and runs it headless (`claude -p`) with `prompts/run.md`, read from the repository at every run: a change to the prompt is a commit, and the next run uses it. The agent's tools are limited to reading and writing files, web search and fetch, and `scripts/data.py`.
3. **Acquisition.** Curated sources (by tier, RSS first), 3 to 5 open web searches, targeted searches for followed authors, and a check of each vendor on the watchlist. The window runs from the last run to today, so a late run leaves no gap.
4. **Deduplication.** `_data/items.csv` is the index of what has already been seen. The key is the canonical URL, normalized by `scripts/data.py`.
5. **Analysis.** Each item is tested for relevance, tagged with one to three topics (dominant first), a tier and a type, and summarized in two or three factual sentences.
6. **Two layers of content.**
   - The **item log** (`_data/items.csv`): append-only, the basis for deduplication and for the source lists on each page.
   - The **topic pages** (`topics/`): living documents, updated by revision rather than accumulation, with dated, sourced and labelled claims.
7. **Run report** (`runs/YYYY-MM-DD.md`): highlights, new items by topic, impact plan, list of page changes with the items behind them, vendor movements, anomalies. It is created at the start of the run and filled as the run proceeds.
8. **Publication.** GitHub Pages builds the site with Jekyll and the Just the Docs theme, reading Markdown pages and CSV data directly.

## Review: nothing is published without approval

The agent writes files only. Fixed workflow steps then create a branch, commit, and open a pull request whose description is the run report.

- **Merge** publishes everything in the pull request.
- **Edits** can be made directly on the branch, or requested with a comment mentioning `@claude`: a second workflow (`pr-feedback.yml`, using `anthropics/claude-code-action` with `prompts/pr-feedback.md`) applies only what was asked, only to files the pull request already touches, and asks back when the request is ambiguous. Only comments by the repository owner trigger it.
- **Closing** without merge discards the run.

An item in an open pull request is under review; a merged item is published; an item removed before merge is discarded. The history of each decision stays in the pull request.

## Guarantees in code, not only in the prompt

- **Branch protection** on `main`: no change reaches the site without a pull request.
- **Closed list of writes.** The agent may append items, propose sources and authors, update two vendor columns, edit three sections of the topic pages and create the run report. `scripts/validate_data.py` rejects any other change, and any modification of existing items. It runs inside the run workflow before the pull request is opened (a failure opens the pull request as a draft, with the errors listed), after every `@claude` correction (a failure is posted as a comment), and on pull requests opened by people (`validate.yml`). Validation is built into the agent workflows because changes pushed with the workflow token do not trigger other workflows.
- **CSV writes only through `scripts/data.py`**, which enforces the [data schema](data-schema.html), quoting and deduplication. The same checks run in CI.
- **No git access for the agent.** Branch, commit and pull request are handled by the workflow.
- **Limits.** The prompt sets caps the agent can count (searches, articles per source, one attempt per source). The workflow sets a maximum number of turns and a time limit. If a run is interrupted, the pull request opens as a draft marked as interrupted, and the report written so far shows what was done.

## Known risks

- **Synthesis** is the delicate step: nuance can be lost, or a weak source can overwrite a stronger one. Mitigation: conservative writing rules, contradictions recorded instead of resolved, review of the diff.
- **Vendor bias** in the sources: cross-checking against independent sources and official documentation (see [source policy](sources-policy.html)).
- **Feed depth**: a source that publishes a lot can push items out of its feed before the next run. The run reports when this may have happened.

## Future directions

Two patterns from the [openwiki](https://github.com/langchain-ai/openwiki) assessment, postponed until the first real runs show where deduplication fails:

1. **Per-source deduplication cursor**, persisted outside the model's control (a committed state file), so each run processes only the delta.
2. **Deterministic fetch separated from LLM synthesis**: a workflow step downloads feeds and pages into raw files, and the agent reads only those.

## Decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-07 | Two layers: item log and topic pages | The log gives deduplication and traceability; the topic pages are what readers consult. Pages alone would not allow deduplication. |
| 2026-07 | Measurement and impact share one topic | Two sides of the same question; split only if the page grows too large. |
| 2026-07 | Sources organized in tiers | Synthesis weighs evidence by source reliability; uncatalogued sources are mostly reached by open search. |
| 2026-07 | Relevance judged by contribution to the field, not by usefulness to a specific consulting practice | The first supervised run showed that a practice-oriented filter discarded substantive material. |
| 2026-07 | Run zero distinct from periodic runs; foundational material goes through the item log with its real publication date | Pages cannot start empty, and routing the foundation through the log preserves deduplication and traceability. |
| 2026-07 | Ingested content is untrusted evidence, never instructions; instructions aimed at an AI are ignored and reported | The run reads third-party web content with no other defence against prompt injection (gap found in the openwiki assessment). |
| 2026-07 | Canonical home for multi-topic items: full detail on the dominant topic's page, one-line pointer elsewhere | Avoids duplicated paragraphs across pages updated independently (pattern from openwiki). |
| 2026-07 | Impact plan required in every run report | Makes the decision of what to touch explicit and checkable (pattern from openwiki). |
| 2026-07 | Two confidence labels on new claims: `[corroborated]` and `[single source]` | Tier measures source reliability, not how well a single fact is corroborated; two levels keep pages readable. |
| 2026-07 | Review before publication: topic pages change only after explicit human approval | Reviewing the diff before it is written, not after. Implemented through pull requests since 2026-11. |
| 2026-07 | Vendor watchlist outside the taxonomy; the vendor list is data, never hardcoded in the prompt | Vendor monitoring is an operational need across topics, and keeping it as data allows changes without touching the prompt. |
| 2026-07 | Followed authors as a separate list | Sources track publications, so an author writing elsewhere was missed (found in the second supervised run). |
| 2026-07-25 | Dynamic window (last run to today); no item without a resolved canonical URL; striking uncorroborated claims go to Anomalies | Late runs leave no gap; the URL is the deduplication key; untrusted evidence is reported, not propagated. |
| 2026-11-18 | The prototype becomes a public personal project, in a new repository with a clean history | The prototype's history contains material tied to its original setting, not relevant to an open project. |
| 2026-11-18 | System of record moves from Notion to files in the repository: Markdown for pages and reports, CSV for structured data | Everything versioned and diffable, reviewable in pull requests, publishable as a static site. |
| 2026-11-18 | Review through pull requests, with branch protection on `main`; corrections through `@claude` comments | The approval rule is enforced by GitHub instead of the prompt; replaces the staged report and the separate apply step. |
| 2026-11-18 | Runs on GitHub Actions with headless Claude Code; git and pull request handled by workflow steps, not by the agent | Fewer permissions for the agent and deterministic publication steps. |
| 2026-11-18 | CSV written only through `scripts/data.py`, validated again in CI | Format, allowed values and deduplication guaranteed by code, not by the prompt. |
| 2026-11-18 | English; relevance test reformulated for practitioners in general | An open wiki is read internationally. |
| 2026-11-18 | Five topics: the topic on the consulting services market is dropped | It was competitive intelligence on service providers: a different purpose, different sources, and content that ages quickly. |
| 2026-11-18 | Runs every two weeks, at night, on the 1st and 15th | Weekly runs are too frequent to review reliably; monthly windows exceed the depth of high-volume feeds and produce pull requests too large to review. |
| 2026-11-18 | Countable caps in the prompt, turn and time limits in the workflow, report written during the run, draft pull request on interruption | The agent cannot see how many turns it has left, so the guarantee that an interruption stays visible must come from the sequence and from code. |
| 2026-11-18 | Site on GitHub Pages with Jekyll and Just the Docs | Reads Markdown and CSV natively, with no build pipeline to maintain; built-in navigation and search. |
| 2026-11-18 | Licences: MIT for code, CC BY 4.0 for content | Standard choices for an open project; content can be reused with attribution. |
| 2026-11-18 | Vendor watchlist limited to products dedicated to AI visibility | Platforms where AI search features are a small part of a broader product add noise to every run; their relevant moves are caught by open search. |
| 2026-11-18 | The run calls the Claude Code CLI directly in the workflow; corrections in pull requests use `anthropics/claude-code-action` | The run needs full control over limits, exit status and publication steps; the action already handles comment triggers and commits to the pull request branch. |
| 2026-11-18 | Validation (`scripts/validate_data.py`) runs inside the agent workflows, not only as a separate check | Pull requests and commits made with the workflow token do not trigger other workflows, so a separate check would never run on them. |
| 2026-11-18 | Only the repository owner can trigger `@claude` corrections | The repository is public: anyone can comment, and a comment must not be able to start the agent. |
| 2026-11-18 | A run that finds the previous run's pull request still open fails instead of skipping silently | A failed workflow notifies the maintainer; a silent skip would go unnoticed. |
| 2026-11-18 | Corrections can remove only rows added in the same pull request (`remove-item`, `remove-proposal`) | Discarding part of a run must not require editing CSV by hand, and the item log on `main` stays append-only. |
| 2026-11-18 | Schedule disabled until manual runs are reliable | Follows the validation path: manual runs first, then the cron. |
| 2026-11-18 | New run zero in English over six months; curated sources, vendors and authors migrated from the prototype, earlier items and pages not migrated | The prototype's content was in Italian and dated July 2026; a new run zero also tests the new pipeline end to end. |
