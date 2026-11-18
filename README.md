# AI Search Open Wiki

**An open, agent-maintained wiki on visibility in AI answer engines.**

Site: [guidolanaro.github.io/ai-search-open-wiki](https://guidolanaro.github.io/ai-search-open-wiki)

Every two weeks an AI agent reads a curated set of sources, searches the open web, and proposes updates to five topic pages on how answer engines (Google AI Overviews and AI Mode, ChatGPT search, Perplexity, Copilot, Claude) select and cite content, and what that means for the people who work on visibility. Nothing is published until a human reviews the pull request.

## Method

- **Dated, sourced claims.** Every statement carries a date, a link to its source, and a confidence label (`[corroborated]` or `[single source]`).
- **Contradictions stay visible.** When sources disagree, the page shows both positions instead of picking one.
- **Vendor figures are attributed.** Numbers published by tool vendors and agencies are reported as their claims, not as facts.
- **Conservative updates.** The agent edits the pages surgically and must justify every change with a new item.

## How it works

```
1st and 15th of the month, at night
  GitHub Actions  →  Claude Code (prompts/run.md)
                      reads _data/ and topics/
                      collects, deduplicates, classifies
                      writes items, page edits, run report
                  →  pull request
  Human review    →  merge = publish  ·  "@claude" comment = correction  ·  close = discard
  GitHub Pages    →  site rebuilt from the repository
```

| Path | Content |
|---|---|
| `topics/` | The five topic pages |
| `runs/` | One report per run |
| `_data/` | Items, sources, vendor watchlist, followed authors (CSV) |
| `method/` | Architecture and decision log, taxonomy, source policy, data schema |
| `prompts/` | The run prompt and the PR-feedback prompt |
| `scripts/` | `data.py`: the only way the agent writes CSV data, and the validation used in CI |
| `.github/workflows/` | Scheduled run, PR feedback, validation |

Start from [`method/architecture.md`](method/architecture.md) for the full design.

## Credits

The incremental page-update rules (surgical edits, impact plan, canonical home for each concept) are adapted from [langchain-ai/openwiki](https://github.com/langchain-ai/openwiki).

## Licence

Code: [MIT](LICENSE). Content in `topics/`, `runs/` and `_data/`: [CC BY 4.0](LICENSE-CONTENT).

Maintained by [Guido Lanaro](https://github.com/GuidoLanaro).
