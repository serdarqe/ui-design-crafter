#!/usr/bin/env python3
"""Search the external UI reference manifest without loading images into a skill."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


HIDDEN_CATEGORIES = {"analysis-artifact", "low-value-non-ui"}


def default_manifest_path() -> Path:
    script = Path(__file__).resolve()
    workspace_candidate = script.parents[2] / "ui-reference-library" / "image-library-manifest.csv"
    cwd_candidate = Path.cwd() / "ui-reference-library" / "image-library-manifest.csv"
    if workspace_candidate.exists():
        return workspace_candidate
    return cwd_candidate


def tokens(value: str) -> list[str]:
    return [part for part in re.split(r"[^a-z0-9]+", value.lower()) if part]


def score_row(row: dict[str, str], query_tokens: list[str]) -> int:
    if not query_tokens:
        return 0

    fields = {
        "path": row.get("path", "").lower(),
        "category": row.get("category", "").lower(),
        "kind": row.get("kind", "").lower(),
        "suitability": row.get("suitability", "").lower(),
        "note": row.get("note", "").lower(),
        "extension": row.get("extension", "").lower(),
    }
    score = 0
    for token in query_tokens:
        if token in fields["category"]:
            score += 5
        if token in fields["kind"]:
            score += 3
        if token in fields["suitability"]:
            score += 2
        if token in fields["note"]:
            score += 2
        if token in fields["path"]:
            score += 1
        if token in fields["extension"]:
            score += 1
    return score


def clip(value: str, width: int) -> str:
    if len(value) <= width:
        return value
    if width <= 3:
        return value[:width]
    return value[: width - 3] + "..."


def print_table(rows: list[dict[str, str]], limit: int) -> None:
    if not rows:
        print("No matching references found.")
        return

    visible = rows[:limit]
    headers = ("score", "category", "kind", "suitability", "path", "note")
    widths = (5, 26, 10, 22, 58, 48)
    print("  ".join(header.ljust(width) for header, width in zip(headers, widths)))
    print("  ".join("-" * width for width in widths))
    for row in visible:
        values = (
            str(row.get("_score", "")),
            row.get("category", ""),
            row.get("kind", ""),
            row.get("suitability", ""),
            row.get("path", ""),
            row.get("note", ""),
        )
        print("  ".join(clip(value, width).ljust(width) for value, width in zip(values, widths)))

    if len(rows) > limit:
        print(f"\nShowing {limit} of {len(rows)} matches. Use --limit to show more.")


def load_rows(manifest: Path) -> list[dict[str, str]]:
    if not manifest.exists():
        raise FileNotFoundError(
            f"Manifest not found: {manifest}\n"
            "This skill bundles no images. Pass --manifest <file>, or place your own image library "
            "with an image-library-manifest.csv next to the skill. "
            "See references/reference-image-analysis.md for the manifest schema."
        )
    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Search your own categorized UI reference-image library by manifest metadata (bring your own images; none are bundled with the skill)."
    )
    parser.add_argument("query", nargs="*", help="Search terms, e.g. hud inventory finance button.")
    parser.add_argument("--manifest", type=Path, default=default_manifest_path())
    parser.add_argument("--category", help="Filter by exact or partial category.")
    parser.add_argument("--kind", help="Filter by exact or partial kind.")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument(
        "--show-internal",
        action="store_true",
        help="Include analysis artifacts and low-value non-UI rows.",
    )
    args = parser.parse_args(argv)

    query = " ".join(args.query).strip()
    query_tokens = tokens(query)
    category_filter = (args.category or "").lower()
    kind_filter = (args.kind or "").lower()

    try:
        rows = load_rows(args.manifest)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    matches: list[dict[str, str]] = []
    for row in rows:
        category = row.get("category", "").lower()
        kind = row.get("kind", "").lower()
        if not args.show_internal and category in HIDDEN_CATEGORIES:
            continue
        if category_filter and category_filter not in category:
            continue
        if kind_filter and kind_filter not in kind:
            continue
        row_score = score_row(row, query_tokens)
        if query_tokens and row_score == 0:
            continue
        enriched = dict(row)
        enriched["_score"] = str(row_score)
        matches.append(enriched)

    matches.sort(key=lambda item: (int(item.get("_score", "0")), item.get("category", ""), item.get("path", "")), reverse=True)
    print_table(matches, max(args.limit, 1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
