# AI Search Open Wiki — project instructions

These instructions are for interactive sessions on this repository (maintenance, design changes). The scheduled run follows `prompts/run.md`; corrections requested in pull requests follow `prompts/pr-feedback.md`.

## What this is

An open, agent-maintained wiki on visibility in AI answer engines, published at https://guidolanaro.github.io/ai-search-open-wiki. A scheduled agent proposes new items and topic page edits in a pull request; a human reviews every change before publication. Design and decision log: `method/architecture.md`.

## Rules

1. **Everything versioned.** Prompts, taxonomy, data, schema and documentation change only through commits. Project knowledge that matters goes into a committed file, not into a session.
2. **Every design decision is logged** in the Decision Log of `method/architecture.md`, with date and reason, before the session ends.
3. **The run prompt is the most critical file.** Change `prompts/run.md` only with a Decision Log entry explaining why.
4. **CSV data is written only through `scripts/data.py`**, never by hand. Run `python scripts/data.py validate` before committing any change to `_data/`.
5. **Keep docs and code aligned.** If the schema changes, update `method/data-schema.md`, `scripts/data.py` and the prompt together.
6. **Commits:** English, imperative, with a scope. Examples: `sources: add Xfunnel as tier B`, `prompt: tighten dedup rules`, `site: add sources list to topic pages`.
7. **No direct pushes to `main`:** work on a branch and open a pull request.

## Structure

- `topics/` — the five topic pages; the agent edits *State of the art*, *Open contradictions* and *Last updated* only
- `runs/` — one report per run
- `_data/` — `items.csv`, `sources.csv`, `vendors.csv`, `authors.csv`
- `method/` — architecture and decision log, taxonomy, source policy, data schema
- `prompts/` — `run.md`, `pr-feedback.md`
- `scripts/` — `data.py` (data writes and validation), `validate_data.py` (CI checks on pull requests)
- `.github/workflows/` — `run.yml`, `pr-feedback.yml`, `validate.yml`
- `_config.yml`, `index.md`, `_includes/` — Jekyll site (Just the Docs)

## Status

- [x] Architecture, taxonomy, source policy, data schema
- [x] Run prompt
- [x] Sources, vendors and authors migrated from the prototype
- [ ] PR-feedback prompt
- [ ] Workflows and CI validation
- [ ] Site published on GitHub Pages
- [ ] Run zero reviewed and merged
- [ ] Scheduled runs enabled
