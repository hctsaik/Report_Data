"""Verify the running preview serves the maintained files and interactive state."""
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://127.0.0.1:4175/'
OUT = ROOT / 'tests/evidence'
OUT.mkdir(parents=True, exist_ok=True)
files = ['index.html', 'styles.css', 'app.js', 'examples/fab-physical-data-v01.png']
matches = {name: hashlib.sha256(urlopen(BASE + name).read()).digest() ==
           hashlib.sha256((ROOT / name).read_bytes()).digest() for name in files}
assert all(matches.values())

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
    page.goto(BASE + '#explore', wait_until='networkidle')
    page.get_by_role('button', name='F012 Slot 08，Wafer W08', exact=True).click()
    expect(page.locator('#quick-selection')).to_have_text('W08 · F012／Slot 08 · Lot L023')

    def capture(name):
        # Full-page captures after interaction need a stable top scroll position:
        # otherwise a sticky header can appear in the middle of the stitched image.
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
        page.screenshot(path=str(OUT / name), full_page=True)

    capture('live-mobile-explore.png')
    page.locator('#transfer').click()
    expect(page.locator('#value-slot')).to_have_text('04')
    capture('live-mobile-transferred.png')
    page.set_viewport_size({'width': 1440, 'height': 1000})
    page.goto(BASE + '#fab', wait_until='networkidle')
    page.mouse.move(0, 0)
    capture('live-desktop-fab.png')
    browser.close()

result = {'url': BASE, 'asset_hash_matches': matches, 'http_interaction': 'PASS'}
(OUT / 'http-results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
