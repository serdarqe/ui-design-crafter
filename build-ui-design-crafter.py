#!/usr/bin/env python3
"""Persistent clean build step for the ui-design-crafter skill.

Run from anywhere:  python build-ui-design-crafter.py

It always: validates the skill, mirror-syncs the installed Claude/Codex copies,
and rebuilds ui-design-crafter.zip while EXCLUDING __pycache__, *.pyc/*.pyo,
images, and PDFs. Finally it verifies the zip contains no forbidden entries and
matches the source tree. This lives OUTSIDE the skill folder so it is never
packaged or shipped.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "ui-design-crafter"
ZIP_PATH = HERE / "ui-design-crafter.zip"
DESTS = [
    Path.home() / ".claude" / "skills" / "ui-design-crafter",
    Path.home() / ".codex" / "skills" / "ui-design-crafter",
]
VALIDATORS = [
    Path.home() / ".claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py",
    Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py",
]

EXCLUDE_DIRS = {"__pycache__", "node_modules", ".git"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf"}
EXCLUDE_NAMES = {".DS_Store"}
IGNORE = shutil.ignore_patterns(
    "__pycache__", "*.pyc", "*.pyo", "*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp", "*.pdf", ".DS_Store",
)


def excluded(rel: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in rel.parts):
        return True
    if rel.suffix.lower() in EXCLUDE_SUFFIXES:
        return True
    return rel.name in EXCLUDE_NAMES


def main() -> int:
    if not SRC.is_dir():
        print(f"Source skill not found: {SRC}")
        return 1

    # 0) Clean stray build artifacts at the source first.
    for junk in SRC.rglob("__pycache__"):
        shutil.rmtree(junk, ignore_errors=True)

    # 1) Validate.
    validator = next((v for v in VALIDATORS if v.exists()), None)
    if validator:
        result = subprocess.run([sys.executable, str(validator), str(SRC)], capture_output=True, text=True)
        print(f"validate: {result.stdout.strip() or result.stderr.strip()}")
        if result.returncode != 0:
            print("Validation failed; aborting build.")
            return 1
    else:
        print("validate: SKIPPED (quick_validate.py not found)")

    # 2) Mirror-sync installed copies.
    for dest in DESTS:
        if dest.parent.exists():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(SRC, dest, ignore=IGNORE)
            print(f"synced (mirror) -> {dest}")
        else:
            print(f"skip (parent missing) -> {dest}")

    # 3) Rebuild the zip with a top-level ui-design-crafter/ prefix.
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    added = []
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(SRC.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(SRC.parent)
            if excluded(rel):
                continue
            zf.write(path, rel.as_posix())
            added.append(rel.as_posix())
    print(f"zip rebuilt: {ZIP_PATH} ({len(added)} entries)")

    # 4) Verify.
    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
    forbidden = [n for n in names if n.lower().endswith(tuple(EXCLUDE_SUFFIXES)) or "__pycache__" in n]
    zip_rel = {n[len("ui-design-crafter/"):] for n in names if n.startswith("ui-design-crafter/")}
    tree_rel = {str(p.relative_to(SRC)).replace("\\", "/") for p in SRC.rglob("*")
                if p.is_file() and not excluded(p.relative_to(SRC.parent))}
    missing = sorted(tree_rel - zip_rel)
    extra = sorted(zip_rel - tree_rel)

    print(f"verify: forbidden entries = {forbidden or 'NONE'}")
    print(f"verify: in tree but missing from zip = {missing or 'NONE'}")
    print(f"verify: in zip but not in tree = {extra or 'NONE'}")
    ok = not forbidden and not missing and not extra
    print("BUILD OK" if ok else "BUILD HAS ISSUES")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
