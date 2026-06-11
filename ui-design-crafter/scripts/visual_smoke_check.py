#!/usr/bin/env python3
"""Visual smoke checks for UI screenshots and browser-captured metrics.

This script is intentionally heuristic. It does not replace a designer's visual
review, but it catches common "do not call this done yet" problems:

- missing mobile/desktop screenshot evidence
- horizontal overflow from browser metrics
- text overflow/clipping from browser metrics
- hidden primary CTA from browser metrics
- likely frame/card stacking from browser metrics
- blank, extremely dark, or extremely light screenshots
- viewport screenshots whose dimensions do not match expected targets

Usage:
    python visual_smoke_check.py --screenshots out/mobile.png out/desktop.png
    python visual_smoke_check.py --metrics out/visual-metrics.json
    python visual_smoke_check.py --screenshots out/*.png --metrics out/*.json --strict

For pixel-level screenshot checks, install Pillow in the project environment. If
Pillow is not available, the script still reads PNG/JPEG dimensions and runs the
metrics checks.
"""

from __future__ import annotations

import argparse
import glob
import json
import math
import struct
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:  # keep Unicode output from crashing on Windows cp125x consoles
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


EXPECTED_VIEWPORTS = {
    "mobile-small": (360, 740),
    "mobile-common": (390, 844),
    "mobile-large": (430, 932),
    "mobile-small-landscape": (740, 360),
    "mobile-common-landscape": (844, 390),
    "mobile-large-landscape": (932, 430),
    "tablet": (768, 1024),
    "desktop": (1366, 768),
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


@dataclass
class Finding:
    severity: str
    rule: str
    target: str
    message: str


def try_import_pillow():
    try:
        from PIL import Image  # type: ignore

        return Image
    except Exception:
        return None


def png_dimensions(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", header[16:24])


def jpeg_dimensions(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        data = handle.read()
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        return None
    index = 2
    while index + 9 < len(data):
        if data[index] != 0xFF:
            index += 1
            continue
        marker = data[index + 1]
        index += 2
        if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
            continue
        if index + 2 > len(data):
            return None
        length = int.from_bytes(data[index : index + 2], "big")
        if length < 2 or index + length > len(data):
            return None
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            if length >= 7:
                height = int.from_bytes(data[index + 3 : index + 5], "big")
                width = int.from_bytes(data[index + 5 : index + 7], "big")
                return (width, height)
            return None
        index += length
    return None


def webp_dimensions(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        data = handle.read(40)
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    fourcc = data[12:16]
    try:
        if fourcc == b"VP8 ":  # lossy: 14-bit width/height at offset 26/28 (LE)
            width = int.from_bytes(data[26:28], "little") & 0x3FFF
            height = int.from_bytes(data[28:30], "little") & 0x3FFF
            return (width, height)
        if fourcc == b"VP8L":  # lossless: 14+14 bits packed after the 0x2f signature
            bits = int.from_bytes(data[21:25], "little")
            return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
        if fourcc == b"VP8X":  # extended: 24-bit canvas width-1/height-1 at offset 24/27 (LE)
            width = int.from_bytes(data[24:27], "little") + 1
            height = int.from_bytes(data[27:30], "little") + 1
            return (width, height)
    except (IndexError, ValueError):
        return None
    return None


def image_dimensions(path: Path) -> tuple[int, int] | None:
    suffix = path.suffix.lower()
    try:
        if suffix == ".png":
            return png_dimensions(path)
        if suffix in {".jpg", ".jpeg"}:
            return jpeg_dimensions(path)
        if suffix == ".webp":
            return webp_dimensions(path)
    except OSError:
        return None
    return None


def nearest_expected_viewport(width: int, height: int) -> tuple[str, int]:
    best_name = ""
    best_delta = 10**9
    for name, (expected_w, expected_h) in EXPECTED_VIEWPORTS.items():
        delta = abs(width - expected_w) + abs(height - expected_h)
        swapped = abs(width - expected_h) + abs(height - expected_w)
        if delta < best_delta:
            best_name, best_delta = name, delta
        if swapped < best_delta:
            best_name, best_delta = f"{name}-rotated", swapped
    return best_name, best_delta


def classify_viewport(width: int, height: int) -> str:
    if min(width, height) <= 480 and max(width, height) >= 600:
        return "mobile"
    if width <= 900 and height >= 700:
        return "tablet"
    if width >= 1000 and height >= 600:
        return "desktop"
    return "unknown"


def iter_paths(paths: list[Path]) -> list[Path]:
    result: list[Path] = []
    for path in paths:
        if any(ch in str(path) for ch in ["*", "?"]):
            result.extend(Path(item) for item in sorted(glob.glob(str(path), recursive=True)))
        elif path.is_dir():
            result.extend(sorted(p for p in path.rglob("*") if p.suffix.lower() in IMAGE_EXTENSIONS or p.suffix.lower() == ".json"))
        else:
            result.append(path)
    return result


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def analyze_pixels(path: Path, width: int, height: int, Image) -> list[Finding]:
    findings: list[Finding] = []
    try:
        with Image.open(path) as image:
            image = image.convert("RGB")
            sample_w = min(width, 96)
            sample_h = min(height, 96)
            image.thumbnail((sample_w, sample_h))
            # Reconstruct RGB tuples from raw bytes; avoids the deprecated
            # Image.getdata() (removed in Pillow 14) and works on all versions.
            raw = image.tobytes()
            pixels = [(raw[i], raw[i + 1], raw[i + 2]) for i in range(0, len(raw) - 2, 3)]
    except Exception as exc:
        return [Finding("warn", "image-read", str(path), f"Could not read pixels: {exc}")]

    if not pixels:
        return [Finding("fail", "blank-image", str(path), "Screenshot has no readable pixels.")]

    lumas = [luminance(pixel) for pixel in pixels]
    avg = sum(lumas) / len(lumas)
    variance = sum((value - avg) ** 2 for value in lumas) / len(lumas)
    stdev = math.sqrt(variance)
    dark_fraction = sum(1 for value in lumas if value < 28) / len(lumas)
    light_fraction = sum(1 for value in lumas if value > 242) / len(lumas)
    mid_fraction = sum(1 for value in lumas if 45 <= value <= 210) / len(lumas)

    if dark_fraction > 0.92:
        findings.append(Finding(
            "fail",
            "background-too-dark",
            str(path),
            f"{dark_fraction:.0%} of sampled pixels are near-black. Theme evidence or UI may be hidden.",
        ))
    elif dark_fraction > 0.78:
        findings.append(Finding(
            "warn",
            "background-very-dark",
            str(path),
            f"{dark_fraction:.0%} of sampled pixels are near-black. Verify the background is not just fog/darkness.",
        ))

    if light_fraction > 0.92:
        findings.append(Finding(
            "warn",
            "background-too-light",
            str(path),
            f"{light_fraction:.0%} of sampled pixels are near-white. Verify text and controls have enough structure.",
        ))

    if stdev < 7:
        findings.append(Finding(
            "fail",
            "blank-or-flat-screenshot",
            str(path),
            f"Very low luminance variation (stdev {stdev:.1f}). Screenshot may be blank, covered, or only a flat gradient.",
        ))
    elif stdev < 14:
        findings.append(Finding(
            "warn",
            "low-visual-evidence",
            str(path),
            f"Low luminance variation (stdev {stdev:.1f}). Verify background/content is not generic or hidden.",
        ))

    if mid_fraction < 0.18:
        findings.append(Finding(
            "warn",
            "limited-midtones",
            str(path),
            f"Only {mid_fraction:.0%} of sampled pixels are midtone. Check contrast and surface readability.",
        ))

    return findings


def analyze_screenshot(path: Path, Image) -> tuple[list[Finding], dict[str, Any] | None]:
    findings: list[Finding] = []
    if not path.exists():
        return [Finding("fail", "missing-screenshot", str(path), "Screenshot file does not exist.")], None
    if path.suffix.lower() not in IMAGE_EXTENSIONS:
        return [Finding("warn", "not-image", str(path), "Path is not a supported screenshot image.")], None
    if path.stat().st_size < 2048:
        findings.append(Finding("fail", "tiny-screenshot-file", str(path), "Screenshot file is very small and may be empty."))

    dims = image_dimensions(path)
    if Image is not None:
        try:
            with Image.open(path) as image:
                dims = image.size
        except Exception:
            pass

    if dims is None:
        findings.append(Finding("warn", "unknown-image-size", str(path), "Could not determine screenshot dimensions."))
        return findings, None

    width, height = dims
    nearest, delta = nearest_expected_viewport(width, height)
    category = classify_viewport(width, height)

    metadata = {
        "path": str(path),
        "width": width,
        "height": height,
        "category": category,
        "nearestExpectedViewport": nearest,
        "expectedDelta": delta,
    }

    if width < 320 or height < 560:
        findings.append(Finding("fail", "viewport-too-small", str(path), f"Screenshot is {width}x{height}; too small for UI QA."))
    if delta > 180 and category != "unknown":
        findings.append(Finding(
            "warn",
            "nonstandard-viewport",
            str(path),
            f"Screenshot is {width}x{height}; nearest standard viewport is {nearest} with delta {delta}.",
        ))

    if Image is None:
        findings.append(Finding(
            "info",
            "pixel-check-skipped",
            str(path),
            "Pillow is not installed, so brightness/blankness pixel checks were skipped.",
        ))
    else:
        findings.extend(analyze_pixels(path, width, height, Image))

    return findings, metadata


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def as_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        if isinstance(payload.get("results"), list):
            return [item for item in payload["results"] if isinstance(item, dict)]
        if isinstance(payload.get("viewports"), list):
            return [item for item in payload["viewports"] if isinstance(item, dict)]
        return [payload]
    return []


def get_number(data: dict[str, Any], *paths: str) -> float | None:
    for path in paths:
        current: Any = data
        ok = True
        for part in path.split("."):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                ok = False
                break
        if ok and isinstance(current, (int, float)):
            return float(current)
    return None


def get_bool(data: dict[str, Any], *paths: str) -> bool | None:
    for path in paths:
        current: Any = data
        ok = True
        for part in path.split("."):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                ok = False
                break
        if ok and isinstance(current, bool):
            return current
    return None


def count_list(data: dict[str, Any], *paths: str) -> int | None:
    for path in paths:
        current: Any = data
        ok = True
        for part in path.split("."):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                ok = False
                break
        if ok:
            if isinstance(current, list):
                return len(current)
            if isinstance(current, (int, float)):
                return int(current)
    return None


def count_or_bool(data: dict[str, Any], *paths: str) -> int | None:
    for path in paths:
        count = count_list(data, path)
        if count is not None:
            return count
        flag = get_bool(data, path)
        if flag is not None:
            return 1 if flag else 0
    return None


def record_name(record: dict[str, Any], source: Path, index: int) -> str:
    label = record.get("name") or record.get("viewportName") or record.get("id")
    width = get_number(record, "viewport.width", "width")
    height = get_number(record, "viewport.height", "height")
    if label:
        return str(label)
    if width and height:
        return f"{source.name}:{int(width)}x{int(height)}"
    return f"{source.name}:record-{index + 1}"


def analyze_metrics(path: Path) -> tuple[list[Finding], list[dict[str, Any]]]:
    findings: list[Finding] = []
    metadata: list[dict[str, Any]] = []
    if not path.exists():
        return [Finding("fail", "missing-metrics", str(path), "Metrics JSON file does not exist.")], metadata
    try:
        payload = load_json(path)
    except Exception as exc:
        return [Finding("fail", "metrics-json", str(path), f"Could not parse metrics JSON: {exc}")], metadata

    records = as_records(payload)
    if not records:
        return [Finding("warn", "empty-metrics", str(path), "Metrics JSON has no viewport records.")], metadata

    for index, record in enumerate(records):
        target = record_name(record, path, index)
        width = get_number(record, "viewport.width", "width", "document.clientWidth")
        height = get_number(record, "viewport.height", "height", "document.clientHeight")
        scroll_width = get_number(record, "document.scrollWidth", "scrollWidth")
        client_width = get_number(record, "document.clientWidth", "clientWidth", "viewport.width")
        cta_visible = get_bool(record, "ctaVisible", "primaryCtaVisible", "issues.primaryCtaVisible")
        horizontal_overflow = get_bool(record, "horizontalOverflow", "issues.horizontalOverflow")
        text_overflow_count = count_list(record, "textOverflow", "issues.textOverflow", "clippedText", "issues.clippedText")
        frame_stack_count = count_list(record, "frameStackCandidates", "issues.frameStackCandidates")
        nested_card_count = count_list(record, "nestedCardCandidates", "issues.nestedCardCandidates")
        safe_area_risk = get_bool(record, "safeAreaRisk", "issues.safeAreaRisk")
        ad_overlap_count = count_or_bool(
            record,
            "adOverlapCount",
            "adOverlaps",
            "adOverlap",
            "adsCoverCriticalUi",
            "issues.adOverlapCount",
            "issues.adsCoverCriticalUi",
        )
        board_obstruction_count = count_or_bool(
            record,
            "boardHudOverlapCount",
            "playfieldObstructionCount",
            "playfieldObstructions",
            "playfieldObstructed",
            "issues.boardHudOverlapCount",
            "issues.playfieldObstructed",
        )

        metadata.append({
            "target": target,
            "width": width,
            "height": height,
            "category": classify_viewport(int(width), int(height)) if width and height else "unknown",
        })

        if width and height:
            nearest, delta = nearest_expected_viewport(int(width), int(height))
            if delta > 180 and classify_viewport(int(width), int(height)) != "unknown":
                findings.append(Finding(
                    "warn",
                    "nonstandard-metrics-viewport",
                    target,
                    f"Metrics viewport is {int(width)}x{int(height)}; nearest standard viewport is {nearest}.",
                ))

        if horizontal_overflow is True:
            findings.append(Finding("fail", "horizontal-overflow", target, "Browser metrics report horizontal overflow."))
        elif scroll_width and client_width and scroll_width > client_width + 1:
            findings.append(Finding(
                "fail",
                "horizontal-overflow",
                target,
                f"scrollWidth {int(scroll_width)} exceeds clientWidth {int(client_width)}.",
            ))

        if text_overflow_count is not None and text_overflow_count > 0:
            severity = "fail" if text_overflow_count >= 3 else "warn"
            findings.append(Finding(
                severity,
                "text-overflow",
                target,
                f"{text_overflow_count} text element(s) appear clipped, overflowing, or truncated.",
            ))

        if cta_visible is False:
            findings.append(Finding("fail", "primary-cta-hidden", target, "Primary CTA is not visible in this viewport."))

        if nested_card_count is not None and nested_card_count > 0:
            findings.append(Finding(
                "warn",
                "nested-card-candidates",
                target,
                f"{nested_card_count} nested card/panel candidate(s) found.",
            ))

        if frame_stack_count is not None and frame_stack_count > 0:
            severity = "fail" if frame_stack_count >= 5 else "warn"
            findings.append(Finding(
                severity,
                "frame-stack-candidates",
                target,
                f"{frame_stack_count} frame-stacking candidate(s) found.",
            ))

        if safe_area_risk is True:
            findings.append(Finding("warn", "mobile-safe-area-risk", target, "Metrics report a mobile safe-area risk."))

        if ad_overlap_count is not None and ad_overlap_count > 0:
            findings.append(Finding(
                "fail",
                "mobile-ad-overlap",
                target,
                f"{ad_overlap_count} ad or monetization region(s) overlap critical UI or playfield.",
            ))

        if board_obstruction_count is not None and board_obstruction_count > 0:
            findings.append(Finding(
                "fail",
                "board-hud-obstruction",
                target,
                f"{board_obstruction_count} HUD, action, or ad region(s) obstruct the board or playfield.",
            ))

    return findings, metadata


def coverage_findings(image_meta: list[dict[str, Any]], metrics_meta: list[dict[str, Any]]) -> list[Finding]:
    findings: list[Finding] = []
    categories = {item.get("category") for item in image_meta + metrics_meta}
    has_mobile = "mobile" in categories
    has_desktop = "desktop" in categories
    if not has_mobile:
        findings.append(Finding("fail", "missing-mobile-evidence", "(coverage)", "No mobile screenshot or metrics viewport was found."))
    if not has_desktop:
        findings.append(Finding("fail", "missing-desktop-evidence", "(coverage)", "No desktop screenshot or metrics viewport was found."))
    if len(image_meta) + len(metrics_meta) < 2:
        findings.append(Finding("fail", "insufficient-evidence", "(coverage)", "Provide at least two viewport checks before calling UI complete."))
    return findings


def print_findings(findings: list[Finding], json_output: bool) -> None:
    counts = {"fail": 0, "warn": 0, "info": 0}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1

    if json_output:
        payload = {
            "summary": counts,
            "findings": [finding.__dict__ for finding in findings],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(f"Visual smoke check: {counts['fail']} fail, {counts['warn']} warn, {counts['info']} info")
    if not findings:
        print("No findings. Still review screenshots manually against visual-qa-checklist.md.")
        return
    order = {"fail": 0, "warn": 1, "info": 2}
    for finding in sorted(findings, key=lambda item: (order.get(item.severity, 9), item.rule, item.target)):
        print(f"[{finding.severity.upper()}] {finding.rule} :: {finding.target}")
        print(f"  {finding.message}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run heuristic visual QA checks on screenshots and browser metrics.")
    parser.add_argument("--screenshots", nargs="*", type=Path, default=[], help="Screenshot image files or folders.")
    parser.add_argument("--metrics", nargs="*", type=Path, default=[], help="Browser metrics JSON files or folders.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on warnings as well as failures.")
    parser.add_argument("--skip-coverage", action="store_true", help="Do not require mobile and desktop evidence.")
    args = parser.parse_args(argv)

    screenshot_paths = [path for path in iter_paths(args.screenshots) if path.suffix.lower() in IMAGE_EXTENSIONS]
    metrics_paths = [path for path in iter_paths(args.metrics) if path.suffix.lower() == ".json"]

    findings: list[Finding] = []
    image_meta: list[dict[str, Any]] = []
    metrics_meta: list[dict[str, Any]] = []
    Image = try_import_pillow()

    for path in screenshot_paths:
        image_findings, meta = analyze_screenshot(path, Image)
        findings.extend(image_findings)
        if meta:
            image_meta.append(meta)

    for path in metrics_paths:
        metric_findings, meta = analyze_metrics(path)
        findings.extend(metric_findings)
        metrics_meta.extend(meta)

    if not screenshot_paths and not metrics_paths:
        findings.append(Finding(
            "fail",
            "no-input",
            "(inputs)",
            "Pass --screenshots and/or --metrics. Visual QA needs real evidence.",
        ))

    if not args.skip_coverage:
        findings.extend(coverage_findings(image_meta, metrics_meta))

    print_findings(findings, args.json)

    has_fail = any(finding.severity == "fail" for finding in findings)
    has_warn = any(finding.severity == "warn" for finding in findings)
    if has_fail or (args.strict and has_warn):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
