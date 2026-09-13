"""Focused final check after mobile arrow and state-copy review."""
from pathlib import Path
from urllib.request import urlopen
import hashlib
import json
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/evidence/operations-v01'
BASE = 'http://127.0.0.1:4175/'
results = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(reduced_motion='reduce')
    for width in [1440, 390, 360]:
        page.set_viewport_size({'width': width, 'height': 1000 if width == 1440 else 844})
        for section in ['transport', 'state', 'run']:
            page.goto(BASE + 'operations.html#' + section)
            expect(page.locator('#' + section)).to_be_visible()
            if section == 'state':
                expect(page.locator('#state')).to_contain_text('仍需核對配方等條件')
                expect(page.locator('#state')).to_contain_text('已開始本站作業，尚未全部完成')
            if width < 600 and section == 'transport':
                assert page.locator('.path-arrow').first.evaluate("el => getComputedStyle(el).fontSize") == '0px'
                assert '↓' in page.locator('.path-arrow').first.evaluate("el => getComputedStyle(el, '::after').content")
            if width < 600 and section == 'run':
                assert '⇅' in page.locator('.transfer-direction').evaluate("el => getComputedStyle(el, '::after').content")
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
            page.mouse.move(0, 0)
            page.evaluate("window.scrollTo({top:0, behavior:'instant'})")
            page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
            page.screenshot(path=str(OUT / f'{width}-{section}.png'), full_page=True)
            results.append([width, section, 'PASS'])
    browser.close()
names = ['operations.html', 'operations.js', 'operations.css', 'index.html', 'styles.css']
hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names}
assert all(hashlib.sha256(urlopen(BASE + name).read()).hexdigest() == digest for name, digest in hashes.items())
(OUT / 'final-layout.json').write_text(json.dumps({'result': 'PASS', 'checks': results, 'verified_http_sha256': hashes}, indent=2), encoding='utf-8')
print('PASS: nine final layout checks, state wording, vertical arrows, served asset hashes')
