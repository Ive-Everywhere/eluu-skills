#!/usr/bin/env python3
"""render.py — render a marketing-visual HTML composition to PNG.

Self-contained: uses headless Chromium via Playwright. No external services,
no capture.py, no harness. Runs entirely inside your own sandbox.

Setup (once per sandbox):
    pip install playwright
    playwright install chromium

Usage:
    python3 render.py <composition.html> [-o out.png]
        [--element '#stage'] [--w 1600] [--h 900] [--scale 2] [--wait 600]

Behaviour:
- Loads the HTML file directly (file:// URL), so a relative
  <link rel="stylesheet" href="../../assets/marketing.css"> and local <img> paths
  resolve normally.
- Waits for web fonts and the network to settle, then screenshots the
  #stage element at the given device-scale (2x = crisp PNG for downscale-on-export).
- If --element is empty or the element is missing, it shots the full viewport.

Export aspects (author once at the format's base size, re-render per aspect):
    OG 1200x630 · square 1080x1080 · portrait 1080x1350 · email hero 1120x480 · wide 1600x900.
Keep the focal element inside a safe margin so it survives every crop.
"""
import argparse
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--element", default="#stage")
    ap.add_argument("--w", type=int, default=1600)
    ap.add_argument("--h", type=int, default=900)
    ap.add_argument("--scale", type=float, default=2)
    ap.add_argument("--wait", type=int, default=600)
    a = ap.parse_args()

    src = Path(a.html).resolve()
    if not src.exists():
        sys.exit(f"error: html not found: {src}")
    out = Path(a.out).resolve() if a.out else src.with_suffix(".png")
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("error: playwright not installed. Run:\n"
                 "  pip install playwright && playwright install chromium")

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb"])
        page = browser.new_page(
            viewport={"width": a.w, "height": a.h},
            device_scale_factor=a.scale,
        )
        page.goto(src.as_uri(), wait_until="networkidle")
        # let webfonts settle so the intermediate weight scale renders
        page.evaluate("() => (document.fonts && document.fonts.ready) "
                      "? document.fonts.ready.then(() => true) : true")
        page.wait_for_timeout(a.wait)

        target = None
        if a.element:
            try:
                target = page.query_selector(a.element)
            except Exception:
                target = None
        if target is not None:
            target.screenshot(path=str(out))
        else:
            page.screenshot(path=str(out))
        browser.close()

    print(str(out))


if __name__ == "__main__":
    main()
