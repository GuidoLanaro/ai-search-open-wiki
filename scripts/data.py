#!/usr/bin/env python3
"""Read and write the wiki's CSV data, enforcing method/data-schema.md.

The agent never edits the CSV files by hand: every write goes through this
script, so quoting, allowed values and deduplication are guaranteed by code.

Commands:
  normalize <url>          print the stored form of a URL
  seen <url>               print "seen <stored url>" or "new"
  add-item ...             append an item to items.csv
  propose-source ...       append a source with status "proposed"
  propose-author ...       append an author with status "proposed"
  update-vendor ...        update last_move / last_move_date of an active vendor
  remove-item --url        remove an item added in the current pull request
  remove-proposal ...      remove a source or author with status "proposed"
  set-field ...            maintainers only: change one field of a source, author or vendor
  validate                 check all CSV files (used in CI); exit 1 on errors

Standard library only. Data directory: _data/ next to this script's parent,
or $WIKI_DATA_DIR if set.
"""

import argparse
import csv
import datetime as dt
import os
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

DATA_DIR = Path(os.environ.get("WIKI_DATA_DIR", Path(__file__).resolve().parent.parent / "_data"))

COLUMNS = {
    "items": ["url", "title", "published", "ingested", "source_id", "tier", "topics", "type", "summary"],
    "sources": ["id", "name", "url", "feed", "tier", "fit", "cadence", "status", "notes"],
    "authors": ["id", "name", "main_publication", "profile", "tier", "status", "notes"],
    "vendors": ["id", "name", "url", "changelog", "last_move", "last_move_date", "status", "notes"],
}
REQUIRED = {
    "items": ["url", "title", "published", "ingested", "tier", "topics", "type", "summary"],
    "sources": ["id", "name", "url", "tier", "fit", "cadence", "status"],
    "authors": ["id", "name", "tier", "status"],
    "vendors": ["id", "name", "url", "status"],
}
ITEM_TIERS = {"A", "B", "C", "open"}
SOURCE_TIERS = {"A", "B", "C"}
ITEM_TYPES = {"product-news", "study-data", "case-study", "analysis-opinion"}
CADENCES = {"daily", "weekly", "monthly", "irregular"}
STATUSES = {"active", "proposed", "suspended"}
VENDOR_STATUSES = {"active", "suspended"}
TOPICS = {"1", "2", "3", "4", "5"}

TRACKING_PARAMS = {
    "gclid", "dclid", "fbclid", "msclkid", "mc_cid", "mc_eid", "_hsenc", "_hsmi",
    "mkt_tok", "ref", "ref_src", "igshid", "yclid", "twclid", "li_fat_id", "si", "s_kwcid",
}
TRACKING_PREFIXES = ("utm_", "hsa_", "pk_", "mtm_")

DATE_FULL = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_PARTIAL = re.compile(r"^\d{4}(-\d{2}){0,2}$")
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class DataError(Exception):
    pass


# ---------------------------------------------------------------- URLs

def normalize_url(url: str) -> str:
    """Stored form: tracking params, fragment, default port and trailing slash removed."""
    url = url.strip()
    parts = urlsplit(url)
    if parts.scheme.lower() not in ("http", "https") or not parts.netloc:
        raise DataError(f"not an absolute http(s) URL: {url!r}")
    scheme = parts.scheme.lower()
    host = (parts.hostname or "").lower()
    port = parts.port
    netloc = host if port is None or (scheme, port) in (("http", 80), ("https", 443)) else f"{host}:{port}"
    query = [
        (k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if k.lower() not in TRACKING_PARAMS and not k.lower().startswith(TRACKING_PREFIXES)
    ]
    path = parts.path
    if len(path) > 1:
        path = path.rstrip("/")
    return urlunsplit((scheme, netloc, path, urlencode(query), ""))


def dedup_key(url: str) -> str:
    """Comparison key: stored form, without scheme and www."""
    parts = urlsplit(normalize_url(url))
    host = parts.netloc[4:] if parts.netloc.startswith("www.") else parts.netloc
    path = "" if parts.path == "/" else parts.path
    return host + path + (("?" + parts.query) if parts.query else "")


# ---------------------------------------------------------------- files

def path_of(name: str) -> Path:
    return DATA_DIR / f"{name}.csv"


def read_rows(name: str) -> list[dict]:
    path = path_of(name)
    if not path.exists():
        raise DataError(f"missing file: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS[name]:
            raise DataError(f"{path.name}: header is {reader.fieldnames}, expected {COLUMNS[name]}")
        return [dict(r) for r in reader]


def write_rows(name: str, rows: list[dict]) -> None:
    path = path_of(name)
    tmp = path.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS[name], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(path)


def append_row(name: str, row: dict) -> None:
    rows = read_rows(name)
    rows.append({c: row.get(c, "") for c in COLUMNS[name]})
    errors = validate_table(name, rows) + cross_check({name: rows})
    if errors:
        raise DataError("; ".join(errors))
    write_rows(name, rows)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def today() -> str:
    return dt.date.today().isoformat()


# ---------------------------------------------------------------- validation

def check_date(value: str, partial: bool = False) -> bool:
    pattern = DATE_PARTIAL if partial else DATE_FULL
    if not pattern.match(value):
        return False
    fmt = {4: "%Y", 7: "%Y-%m", 10: "%Y-%m-%d"}[len(value)]
    try:
        dt.datetime.strptime(value, fmt)
    except ValueError:
        return False
    return True


def validate_table(name: str, rows: list[dict]) -> list[str]:
    errors = []
    seen_ids, seen_urls = {}, {}
    for n, row in enumerate(rows, start=2):  # line 1 is the header
        where = f"{name}.csv line {n}"
        if None in row or any(v is None for v in row.values()):
            errors.append(f"{where}: wrong number of fields")
            continue
        row = {k: v.strip() for k, v in row.items()}
        for col in REQUIRED[name]:
            if not row[col]:
                errors.append(f"{where}: {col} is empty")

        if "id" in row and row["id"]:
            if not SLUG.match(row["id"]):
                errors.append(f"{where}: id {row['id']!r} is not a lowercase slug")
            if row["id"] in seen_ids:
                errors.append(f"{where}: id {row['id']!r} already on line {seen_ids[row['id']]}")
            seen_ids[row["id"]] = n

        for col in ("url", "feed", "main_publication", "profile", "changelog"):
            if row.get(col):
                try:
                    normalize_url(row[col])
                except DataError as e:
                    errors.append(f"{where}: {col}: {e}")

        if name in ("items", "sources") and row["url"]:
            try:
                key = dedup_key(row["url"])
                if key in seen_urls:
                    errors.append(f"{where}: url duplicates line {seen_urls[key]}")
                seen_urls[key] = n
                if name == "items" and row["url"] != normalize_url(row["url"]):
                    errors.append(f"{where}: url not in stored form, expected {normalize_url(row['url'])}")
            except DataError:
                pass

        if name == "items":
            if row["published"] and not check_date(row["published"], partial=True):
                errors.append(f"{where}: published {row['published']!r} is not YYYY-MM-DD, YYYY-MM or YYYY")
            if row["ingested"] and not check_date(row["ingested"]):
                errors.append(f"{where}: ingested {row['ingested']!r} is not YYYY-MM-DD")
            if row["tier"] and row["tier"] not in ITEM_TIERS:
                errors.append(f"{where}: tier {row['tier']!r} not in {sorted(ITEM_TIERS)}")
            if row["type"] and row["type"] not in ITEM_TYPES:
                errors.append(f"{where}: type {row['type']!r} not in {sorted(ITEM_TYPES)}")
            if row["topics"]:
                topics = row["topics"].split(";")
                if not 1 <= len(topics) <= 3 or set(topics) - TOPICS or len(set(topics)) != len(topics):
                    errors.append(f"{where}: topics {row['topics']!r} must be 1-3 distinct numbers 1-5 separated by ';'")
        else:
            if name != "vendors" and row["tier"] and row["tier"] not in SOURCE_TIERS:
                errors.append(f"{where}: tier {row['tier']!r} not in {sorted(SOURCE_TIERS)}")
            allowed = VENDOR_STATUSES if name == "vendors" else STATUSES
            if row["status"] and row["status"] not in allowed:
                errors.append(f"{where}: status {row['status']!r} not in {sorted(allowed)}")

        if name == "sources":
            if row["fit"] and row["fit"] not in {"1", "2", "3", "4", "5"}:
                errors.append(f"{where}: fit {row['fit']!r} must be 1-5")
            if row["cadence"] and row["cadence"] not in CADENCES:
                errors.append(f"{where}: cadence {row['cadence']!r} not in {sorted(CADENCES)}")

        if name == "vendors" and row["last_move_date"] and not check_date(row["last_move_date"]):
            errors.append(f"{where}: last_move_date {row['last_move_date']!r} is not YYYY-MM-DD")
    return errors


def cross_check(tables: dict) -> list[str]:
    """items.source_id must exist in sources.csv."""
    errors = []
    if "items" not in tables:
        return errors
    sources = tables.get("sources")
    if sources is None:
        try:
            sources = read_rows("sources")
        except DataError:
            return errors
    ids = {s["id"] for s in sources}
    for n, row in enumerate(tables["items"], start=2):
        sid = (row.get("source_id") or "").strip()
        if sid and sid not in ids:
            errors.append(f"items.csv line {n}: source_id {sid!r} not in sources.csv")
    return errors


# ---------------------------------------------------------------- commands

def find_seen(url: str):
    key = dedup_key(url)
    for row in read_rows("items"):
        if dedup_key(row["url"]) == key:
            return row["url"]
    return None


def cmd_normalize(a):
    print(normalize_url(a.url))


def cmd_seen(a):
    match = find_seen(a.url)
    print(f"seen {match}" if match else "new")


def cmd_add_item(a):
    url = normalize_url(a.url)
    match = find_seen(url)
    if match:
        raise DataError(f"already in items.csv: {match}")
    append_row("items", {
        "url": url, "title": a.title, "published": a.published, "ingested": a.ingested or today(),
        "source_id": a.source_id or "", "tier": a.tier, "topics": a.topics, "type": a.type,
        "summary": " ".join(a.summary.split()),
    })
    print(f"added {url}")


def cmd_propose_source(a):
    sid = a.id or slugify(a.name)
    key = dedup_key(a.url)
    if any(dedup_key(s["url"]) == key for s in read_rows("sources")):
        raise DataError(f"source already listed: {a.url}")
    append_row("sources", {
        "id": sid, "name": a.name, "url": normalize_url(a.url), "feed": a.feed or "", "tier": a.tier,
        "fit": a.fit, "cadence": a.cadence, "status": "proposed", "notes": a.notes or "",
    })
    print(f"proposed source {sid}")


def cmd_propose_author(a):
    aid = a.id or slugify(a.name)
    if any(r["id"] == aid or r["name"].lower() == a.name.lower() for r in read_rows("authors")):
        raise DataError(f"author already listed: {a.name}")
    append_row("authors", {
        "id": aid, "name": a.name, "main_publication": a.main_publication or "", "profile": a.profile or "",
        "tier": a.tier, "status": "proposed", "notes": a.notes or "",
    })
    print(f"proposed author {aid}")


def cmd_update_vendor(a):
    if not check_date(a.date):
        raise DataError(f"date {a.date!r} is not YYYY-MM-DD")
    rows = read_rows("vendors")
    for row in rows:
        if row["id"] == a.id:
            if row["status"] != "active":
                raise DataError(f"vendor {a.id!r} is not active")
            row["last_move"] = " ".join(a.last_move.split())
            row["last_move_date"] = a.date
            break
    else:
        raise DataError(f"no vendor with id {a.id!r}")
    errors = validate_table("vendors", rows)
    if errors:
        raise DataError("; ".join(errors))
    write_rows("vendors", rows)
    print(f"updated vendor {a.id}")


def cmd_remove_item(a):
    key = dedup_key(a.url)
    rows = read_rows("items")
    kept = [r for r in rows if dedup_key(r["url"]) != key]
    if len(kept) == len(rows):
        raise DataError(f"no item with url {a.url!r}")
    write_rows("items", kept)
    print(f"removed item {a.url} (CI rejects removals of items already on main)")


def cmd_remove_proposal(a):
    rows = read_rows(a.table)
    match = [r for r in rows if r["id"] == a.id]
    if not match:
        raise DataError(f"no {a.table} row with id {a.id!r}")
    if match[0]["status"] != "proposed":
        raise DataError(f"{a.table} row {a.id!r} is {match[0]['status']!r}, not 'proposed'")
    write_rows(a.table, [r for r in rows if r["id"] != a.id])
    print(f"removed proposed {a.table} row {a.id}")


def cmd_set_field(a):
    if a.table == "items":
        raise DataError("items are append-only: use remove-item on an unmerged item instead")
    if a.field == "id" or a.field not in data_columns(a.table):
        raise DataError(f"{a.table}.csv has no editable field {a.field!r}")
    rows = read_rows(a.table)
    for row in rows:
        if row["id"] == a.id:
            row[a.field] = " ".join(a.value.split())
            break
    else:
        raise DataError(f"no {a.table} row with id {a.id!r}")
    errors = validate_table(a.table, rows) + cross_check({a.table: rows})
    if errors:
        raise DataError("; ".join(errors))
    write_rows(a.table, rows)
    print(f"{a.table}.{a.id}.{a.field} updated")


def data_columns(table):
    return COLUMNS[table]


def cmd_validate(a):
    tables, errors = {}, []
    for name in COLUMNS:
        try:
            tables[name] = read_rows(name)
        except DataError as e:
            errors.append(str(e))
    for name, rows in tables.items():
        errors += validate_table(name, rows)
    errors += cross_check(tables)
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("ok: " + ", ".join(f"{n} {len(r)} rows" for n, r in tables.items()))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("normalize"); s.add_argument("url"); s.set_defaults(fn=cmd_normalize)
    s = sub.add_parser("seen"); s.add_argument("url"); s.set_defaults(fn=cmd_seen)

    s = sub.add_parser("add-item")
    s.add_argument("--url", required=True)
    s.add_argument("--title", required=True)
    s.add_argument("--published", required=True)
    s.add_argument("--ingested", help="defaults to today")
    s.add_argument("--source-id")
    s.add_argument("--tier", required=True, choices=sorted(ITEM_TIERS))
    s.add_argument("--topics", required=True, help="e.g. 1;3 (dominant topic first)")
    s.add_argument("--type", required=True, choices=sorted(ITEM_TYPES))
    s.add_argument("--summary", required=True)
    s.set_defaults(fn=cmd_add_item)

    s = sub.add_parser("propose-source")
    s.add_argument("--id")
    s.add_argument("--name", required=True)
    s.add_argument("--url", required=True)
    s.add_argument("--feed")
    s.add_argument("--tier", required=True, choices=sorted(SOURCE_TIERS))
    s.add_argument("--fit", required=True, choices=["1", "2", "3", "4", "5"])
    s.add_argument("--cadence", required=True, choices=sorted(CADENCES))
    s.add_argument("--notes")
    s.set_defaults(fn=cmd_propose_source)

    s = sub.add_parser("propose-author")
    s.add_argument("--id")
    s.add_argument("--name", required=True)
    s.add_argument("--main-publication")
    s.add_argument("--profile")
    s.add_argument("--tier", required=True, choices=sorted(SOURCE_TIERS))
    s.add_argument("--notes")
    s.set_defaults(fn=cmd_propose_author)

    s = sub.add_parser("update-vendor")
    s.add_argument("--id", required=True)
    s.add_argument("--last-move", required=True)
    s.add_argument("--date", required=True)
    s.set_defaults(fn=cmd_update_vendor)

    s = sub.add_parser("remove-item", help="only for items added in the current pull request")
    s.add_argument("--url", required=True)
    s.set_defaults(fn=cmd_remove_item)

    s = sub.add_parser("remove-proposal", help="remove a source or author with status 'proposed'")
    s.add_argument("--table", required=True, choices=["sources", "authors"])
    s.add_argument("--id", required=True)
    s.set_defaults(fn=cmd_remove_proposal)

    s = sub.add_parser("set-field", help="maintainers only: change one field of a source, author or vendor")
    s.add_argument("--table", required=True, choices=["sources", "authors", "vendors"])
    s.add_argument("--id", required=True)
    s.add_argument("--field", required=True)
    s.add_argument("--value", required=True)
    s.set_defaults(fn=cmd_set_field)

    s = sub.add_parser("validate"); s.set_defaults(fn=cmd_validate)

    a = p.parse_args(argv)
    try:
        a.fn(a)
    except DataError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
