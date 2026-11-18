#!/usr/bin/env python3
"""Check the working tree against a base ref (default: origin/main).

Used by the workflows before a run's pull request is opened, after every
@claude correction, and on pull requests opened by people.

  python3 scripts/validate_data.py --mode run   # changes made by the agent
  python3 scripts/validate_data.py --mode any   # changes made by people

Both modes: schema validation of every CSV (scripts/data.py).
Run mode adds the write rules of prompts/run.md:
  - only allowed paths are changed: _data/*.csv, existing topic pages, a new runs/YYYY-MM-DD.md
  - items.csv is append-only
  - sources.csv and authors.csv: existing rows unchanged, new rows only with status "proposed"
  - vendors.csv: same rows; only last_move / last_move_date of active vendors change
  - topic pages: front matter, section headings and the Sources section unchanged
  - run reports: required front matter
In "any" mode the run rules are reported as warnings, not errors.

Exit code 1 if there are errors. Output is Markdown, ready for a PR comment.
"""

import argparse
import csv
import io
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import data  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TOPIC_HEADINGS = ["## State of the art", "## Open contradictions", "## Last updated", "## Sources"]
RUN_FILE = re.compile(r"^runs/\d{4}-\d{2}-\d{2}\.md$")
DATA_FILES = {f"_data/{n}.csv" for n in data.COLUMNS}


def git(*args, check=True) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def base_text(base: str, path: str):
    r = subprocess.run(["git", "show", f"{base}:{path}"], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def rows_of(text: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(text)))


def changed_paths(base: str) -> dict[str, str]:
    """path -> status (A, M, D, ...) for the working tree against base, untracked files included."""
    changes = {}
    for line in git("diff", "--name-status", "--no-renames", base).splitlines():
        status, path = line.split("\t", 1)
        changes[path] = status[0]
    for path in git("ls-files", "--others", "--exclude-standard").splitlines():
        changes[path] = "A"
    return changes


def split_front_matter(text: str):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[4:end], text[end + 5:]
    return None, text


def check_paths(changes, base, issues):
    for path, status in sorted(changes.items()):
        if path in DATA_FILES and status == "M":
            continue
        if path.startswith("topics/") and path.endswith(".md") and path != "topics/index.md" and status == "M":
            continue
        if RUN_FILE.match(path) and status == "A":
            continue
        issues.append(f"`{path}`: change not allowed for a run ({'added' if status == 'A' else 'deleted' if status == 'D' else 'modified'})")


def check_items(base, issues):
    old = base_text(base, "_data/items.csv")
    if old is None:
        return
    old_rows, new_rows = rows_of(old), data.read_rows("items")
    if new_rows[:len(old_rows)] != old_rows:
        issues.append("`_data/items.csv`: existing items were modified, removed or reordered (the log is append-only)")


def check_proposals(base, name, issues):
    old = base_text(base, f"_data/{name}.csv")
    if old is None:
        return
    old_rows, new_rows = rows_of(old), data.read_rows(name)
    if new_rows[:len(old_rows)] != old_rows:
        issues.append(f"`_data/{name}.csv`: existing rows were modified, removed or reordered")
        return
    for row in new_rows[len(old_rows):]:
        if row["status"] != "proposed":
            issues.append(f"`_data/{name}.csv`: new row `{row['id']}` has status `{row['status']}`; the agent may only add `proposed` rows")


def check_vendors(base, issues):
    old = base_text(base, "_data/vendors.csv")
    if old is None:
        return
    old_rows, new_rows = rows_of(old), data.read_rows("vendors")
    if [r["id"] for r in old_rows] != [r["id"] for r in new_rows]:
        issues.append("`_data/vendors.csv`: vendors were added, removed or reordered (only people change the watchlist)")
        return
    for o, n in zip(old_rows, new_rows):
        changed = {k for k in o if o[k] != n[k]}
        if changed - {"last_move", "last_move_date"}:
            issues.append(f"`_data/vendors.csv`: `{o['id']}` changed {sorted(changed)}; only last_move and last_move_date may change")
        elif changed and o["status"] != "active":
            issues.append(f"`_data/vendors.csv`: `{o['id']}` is not active and must not be updated")


def check_topic(base, path, issues):
    old = base_text(base, path)
    new = (ROOT / path).read_text(encoding="utf-8")
    if old is None:
        return
    old_fm, old_body = split_front_matter(old)
    new_fm, new_body = split_front_matter(new)
    if old_fm != new_fm:
        issues.append(f"`{path}`: front matter changed")
    positions = [new_body.find("\n" + h + "\n") for h in TOPIC_HEADINGS]
    if -1 in positions or positions != sorted(positions):
        issues.append(f"`{path}`: section headings missing or out of order (expected {', '.join(TOPIC_HEADINGS)})")
        return
    old_sources = old_body[old_body.find("\n## Sources\n"):]
    new_sources = new_body[new_body.find("\n## Sources\n"):]
    if old_sources != new_sources:
        issues.append(f"`{path}`: the Sources section is generated by the site and must not change")


def check_run_report(path, issues):
    fm, body = split_front_matter((ROOT / path).read_text(encoding="utf-8"))
    date = Path(path).stem
    expected = {"title": f"Run {date}", "parent": "Runs", "nav_exclude": "true"}
    found = dict(line.split(":", 1) for line in (fm or "").splitlines() if ":" in line)
    found = {k.strip(): v.strip().strip('"') for k, v in found.items()}
    for k, v in expected.items():
        if found.get(k) != v:
            issues.append(f"`{path}`: front matter needs `{k}: {v}`")
    if not body.strip():
        issues.append(f"`{path}`: the run report is empty")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--base", default="origin/main")
    p.add_argument("--mode", choices=["run", "any"], default="any")
    a = p.parse_args()

    errors, rule_issues = [], []

    # Schema validation of every CSV
    tables = {}
    for name in data.COLUMNS:
        try:
            tables[name] = data.read_rows(name)
        except data.DataError as e:
            errors.append(str(e))
    for name, rows in tables.items():
        errors += data.validate_table(name, rows)
    errors += data.cross_check(tables)

    # Write rules of a run
    if not errors:
        changes = changed_paths(a.base)
        if a.mode == "run":  # people may change any file
            check_paths(changes, a.base, rule_issues)
        check_items(a.base, rule_issues)
        check_proposals(a.base, "sources", rule_issues)
        check_proposals(a.base, "authors", rule_issues)
        check_vendors(a.base, rule_issues)
        for path, status in changes.items():
            if path.startswith("topics/") and path != "topics/index.md" and path.endswith(".md") and status == "M":
                check_topic(a.base, path, rule_issues)
            if RUN_FILE.match(path) and status != "D":
                check_run_report(path, rule_issues)

    warnings = []
    if a.mode == "run":
        errors += rule_issues
    else:
        warnings = rule_issues

    lines = []
    if errors:
        lines.append("**Validation failed**")
        lines += [f"- {e}" for e in errors]
    if warnings:
        lines.append("**Changes outside the rules for automated runs** (fine if made on purpose by a person)")
        lines += [f"- {w}" for w in warnings]
    if not lines:
        lines.append("**Validation passed**")
    print("\n".join(lines))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
