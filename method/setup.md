---
title: Setup
parent: Method
nav_order: 5
---

# Setup

What the repository needs before the agent can run, and how to run your own copy.

## 1. Claude credentials

The workflows authenticate with a Claude subscription token (Pro, Max, Team or Enterprise plans).

1. On your computer, with Claude Code installed, run `claude setup-token` and copy the token.
2. In the repository: **Settings → Secrets and variables → Actions → New repository secret**, name `CLAUDE_CODE_OAUTH_TOKEN`.

The token lasts about a year, then has to be generated again. Runs use the same usage allowance as your own sessions, which is one reason they are scheduled at night.

An Anthropic API key works too (secret `ANTHROPIC_API_KEY`, billed per token), with small changes to the two workflows.

## 2. Actions permissions

**Settings → Actions → General → Workflow permissions:**
- select **Read and write permissions**;
- tick **Allow GitHub Actions to create and approve pull requests**.

Without the second option the run cannot open its pull request.

## 3. Branch protection

**Settings → Branches → Add rule** (or **Rules → Rulesets**) for `main`: **Require a pull request before merging**, with zero required approvals (GitHub does not let you approve your own pull request).

Do not add the *Validate* workflow as a required status check: run pull requests are validated inside the run workflow. GitHub holds workflows triggered by the workflow token for manual approval ("Action required" in the Actions tab), so a required check would block every run pull request. Those pending *Validate* runs can be ignored.

On private repositories, branch protection needs a paid GitHub plan; on public ones it is free.

## 4. First runs

1. **Actions → Run → Run workflow.** The first run is run zero: a six-month window, higher limits (500 turns, 180 minutes).
2. Review the pull request. Corrections: edit files on the branch, or comment `@claude` with the request.
3. Merge, or close to discard.
4. Repeat manually until runs are reliable, then enable the schedule: uncomment the `schedule` block in `.github/workflows/run.yml`.

The limits can be changed for a single manual run (fields *max turns* and *time limit*) and, permanently, in the *Set up the run* step.

## 5. Site

**Settings → Pages → Build and deployment:** source **Deploy from a branch**, branch `main`, folder `/ (root)`. GitHub Pages builds the site with Jekyll at every push to `main`. On private repositories Pages needs a paid plan.

If you fork the project, update `baseurl`, `url` and the repository links in `_config.yml`.
