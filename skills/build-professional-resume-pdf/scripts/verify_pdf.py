#!/usr/bin/env python3
"""Verify resume PDF page geometry, text, and clickable URI annotations."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

try:
    from pypdf import PdfReader
except ImportError as exc:
    raise SystemExit("pypdf is required. Install it with: python3 -m pip install pypdf") from exc


def compact(value: str) -> str:
    return re.sub(r"\s+", "", value)


def annotations(reader: PdfReader) -> list[str]:
    values: list[str] = []
    for page in reader.pages:
        for annotation in page.get("/Annots", []) or []:
            obj = annotation.get_object()
            action = obj.get("/A")
            if action and action.get("/URI"):
                values.append(str(action.get("/URI")))
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--expected-pages", type=int)
    parser.add_argument("--required-text", action="append", default=[])
    parser.add_argument("--forbidden-text", action="append", default=[])
    parser.add_argument("--required-uri", action="append", default=[])
    parser.add_argument("--skip-a4-check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf = args.pdf.expanduser().resolve()
    if not pdf.is_file():
        raise SystemExit(f"PDF does not exist: {pdf}")

    reader = PdfReader(str(pdf))
    text = compact("".join((page.extract_text() or "") for page in reader.pages))
    uris = annotations(reader)
    failures: list[str] = []

    if args.expected_pages is not None and len(reader.pages) != args.expected_pages:
        failures.append(f"expected {args.expected_pages} pages, found {len(reader.pages)}")

    if not args.skip_a4_check:
        for index, page in enumerate(reader.pages, start=1):
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            if abs(width - 595.28) > 3 or abs(height - 841.89) > 3:
                failures.append(
                    f"page {index} is not A4 portrait: {width:.2f} x {height:.2f} pt"
                )

    for value in args.required_text:
        if compact(value) not in text:
            failures.append(f"required text missing: {value}")
    for value in args.forbidden_text:
        if compact(value) in text:
            failures.append(f"forbidden text present: {value}")
    for value in args.required_uri:
        if value not in uris:
            failures.append(f"required URI missing: {value}")

    print(f"PDF: {pdf}")
    print(f"Pages: {len(reader.pages)}")
    print(f"URIs: {uris}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("PASS: all requested checks succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
