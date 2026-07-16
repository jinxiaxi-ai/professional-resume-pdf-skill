#!/usr/bin/env python3
"""Render a local HTML resume to PDF and optional PNG previews."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import tempfile
import time


def existing(paths: list[str | Path]) -> str | None:
    for value in paths:
        if not value:
            continue
        path = Path(value).expanduser()
        if path.is_file():
            return str(path)
        found = shutil.which(str(value))
        if found:
            return found
    return None


def find_chrome(explicit: str | None) -> str:
    candidates: list[str | Path] = []
    if explicit:
        candidates.append(explicit)
    if os.environ.get("CHROME_PATH"):
        candidates.append(os.environ["CHROME_PATH"])
    candidates.extend(
        [
            "google-chrome",
            "google-chrome-stable",
            "chromium",
            "chromium-browser",
            "chrome",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            Path.home() / "Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
    )
    chrome = existing(candidates)
    if not chrome:
        raise SystemExit(
            "Chrome/Chromium was not found. Install it or pass --chrome /path/to/browser."
        )
    return chrome


def find_pdftoppm(explicit: str | None) -> str:
    candidates: list[str | Path] = []
    if explicit:
        candidates.append(explicit)
    candidates.extend(
        [
            "pdftoppm",
            Path.home()
            / ".cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm",
        ]
    )
    command = existing(candidates)
    if not command:
        raise SystemExit(
            "pdftoppm was not found. Install Poppler or pass --pdftoppm /path/to/pdftoppm."
        )
    return command


def stop_process(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    try:
        if os.name == "nt":
            process.terminate()
        else:
            os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=3)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        if process.poll() is None:
            if os.name == "nt":
                process.kill()
            else:
                os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=3)


def wait_for_stable_pdf(process: subprocess.Popen[bytes], pdf: Path, timeout: int) -> bool:
    deadline = time.monotonic() + timeout
    last_size = -1
    stable_checks = 0
    while time.monotonic() < deadline:
        if pdf.is_file() and pdf.stat().st_size > 0:
            size = pdf.stat().st_size
            if size == last_size:
                stable_checks += 1
            else:
                stable_checks = 0
                last_size = size
            if stable_checks >= 5:
                return True
        if process.poll() is not None and not pdf.is_file():
            return False
        time.sleep(0.2)
    return False


def print_pdf(chrome: str, html: Path, pdf: Path, timeout: int) -> None:
    common = [
        chrome,
        "--disable-gpu",
        "--disable-background-networking",
        "--disable-component-update",
        "--disable-extensions",
        "--disable-sync",
        "--no-first-run",
        "--no-default-browser-check",
        "--allow-file-access-from-files",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf}",
        html.as_uri(),
    ]

    errors: list[str] = []
    for headless in ("--headless=new", "--headless"):
        with tempfile.TemporaryDirectory(prefix="resume-chrome-") as profile:
            command = common[:1] + [headless, f"--user-data-dir={profile}"] + common[1:]
            process = subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=os.name != "nt",
            )
            success = wait_for_stable_pdf(process, pdf, timeout)
            return_code = process.poll()
            stop_process(process)
            if success:
                return
            errors.append(f"{headless}: exit {return_code}; no stable PDF after {timeout}s")

    raise SystemExit("Chrome failed to create the PDF.\n" + "\n".join(errors))


def render_pages(pdftoppm: str, pdf: Path, render_dir: Path, dpi: int) -> list[Path]:
    render_dir.mkdir(parents=True, exist_ok=True)
    for old in render_dir.glob("page-*.png"):
        old.unlink()
    prefix = render_dir / "page"
    subprocess.run(
        [pdftoppm, "-png", "-r", str(dpi), str(pdf), str(prefix)],
        check=True,
    )
    pages = sorted(render_dir.glob("page-*.png"))
    if not pages:
        raise SystemExit("pdftoppm completed without producing page PNGs.")
    return pages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Local resume HTML")
    parser.add_argument("--output", required=True, type=Path, help="Destination PDF")
    parser.add_argument("--render-dir", type=Path, help="Optional PNG output directory")
    parser.add_argument("--dpi", type=int, default=160, help="Preview DPI (default: 160)")
    parser.add_argument("--chrome", help="Chrome or Chromium executable")
    parser.add_argument("--pdftoppm", help="pdftoppm executable")
    parser.add_argument("--timeout", type=int, default=90, help="Browser timeout in seconds")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    html = args.input.expanduser().resolve()
    pdf = args.output.expanduser().resolve()
    if not html.is_file():
        raise SystemExit(f"Input HTML does not exist: {html}")
    pdf.parent.mkdir(parents=True, exist_ok=True)
    pdf.unlink(missing_ok=True)

    chrome = find_chrome(args.chrome)
    print_pdf(chrome, html, pdf, args.timeout)
    print(f"PDF: {pdf} ({pdf.stat().st_size} bytes)")

    if args.render_dir:
        command = find_pdftoppm(args.pdftoppm)
        pages = render_pages(command, pdf, args.render_dir.expanduser().resolve(), args.dpi)
        for page in pages:
            print(f"Preview: {page}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
