"""Second lesson: state invariants, responsive UI, offline and served-asset checks."""
from pathlib import Path
from urllib.request import urlopen
import hashlib
import json
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/evidence/operations-v01'
OUT.mkdir(parents=True, exist_ok=True)
URI = (ROOT / 'operations.html').as_uri()
CHAPTERS = ['tool', 'port', 'chamber', 'process', 'transport', 'state', 'arrival', 'run', 'hold', 'reconcile']
report = {'checks': [], 'screens': [], 'errors': []}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
    page.on('pageerror', lambda error: report['errors'].append(str(error)))

    def go(section):
        page.goto(URI + '#' + section)
        expect(page.locator('#' + section)).to_be_visible()

    def capture(name):
        page.evaluate("window.scrollTo({top:0, behavior:'instant'})")
        page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
        page.screenshot(path=str(OUT / name), full_page=True)

    go('tool')
    expect(page.locator('#previous')).to_be_disabled()
    for section in CHAPTERS[1:]:
        page.locator('#next').click()
        expect(page.locator('#' + section)).to_be_visible()
        assert page.locator('.lesson:visible').count() == 1
    page.locator('#previous').click()
    expect(page.locator('#hold')).to_be_visible()
    page.go_back()
    expect(page.locator('#reconcile')).to_be_visible()
    report['checks'].append('All ten chapters, previous/next, browser history, single visible section')

    for width in [1440, 390]:
        page.set_viewport_size({'width': width, 'height': 1000 if width == 1440 else 844})
        go('arrival')
        page.locator('#arrival-reset').click()
        for destination in ['ETCH-03/LP2', 'ETCH-04/LP1']:
            page.locator('#destination').select_option(destination)
            page.locator('#arrival-next').click()
            expect(page.locator('#arrival-feedback')).to_contain_text('不符合')
            expect(page.locator('#arrival-location')).to_contain_text('STK-01')
        page.locator('#destination').select_option('ETCH-03/LP1')
        page.locator('#arrival-next').focus()
        page.keyboard.press('Enter')
        expect(page.locator('#arrival-location')).to_contain_text('OHT-01')
        expect(page.locator('#destination')).to_be_disabled()
        assert page.locator('#arrival-scene .small-foup').count() == 1
        capture(f'{width}-arrival-transit.png')
        page.locator('#arrival-next').click()
        expect(page.locator('#arrival-location')).to_contain_text('ETCH-03／LP1')
        expect(page.locator('#arrival-feedback')).to_contain_text('尚未開始')
        expect(page.locator('#arrival-next')).to_be_disabled()
        page.locator('#arrival-reset').click()
        expect(page.locator('#arrival-location')).to_contain_text('STK-01')

        go('run')
        page.locator('#run-reset').click()
        for recipe in ['ETCH-DEMO/v1', 'CLEAN-DEMO/v2']:
            page.locator('#recipe-choice').select_option(recipe)
            page.locator('#run-next').click()
            expect(page.locator('#run-feedback')).to_contain_text('不符合')
            expect(page.locator('#run-progress')).to_contain_text('0 / 3')
            assert page.locator('#run-slots .mini-wafer').count() == 3
            assert page.locator('#chamber-wafer .mini-wafer').count() == 0
        page.locator('#recipe-choice').select_option('ETCH-DEMO/v2')
        for index, wafer in enumerate(['W06', 'W07', 'W08']):
            page.locator('#run-next').click()
            expect(page.locator('#chamber-wafer')).to_have_text(wafer)
            assert page.locator('#run-slots .mini-wafer').count() == 2
            assert page.locator('#run-slots .vacant').count() == 1
            expect(page.locator('#recipe-choice')).to_be_disabled()
            expect(page.locator('#run-progress')).to_contain_text(f'{index} / 3')
            if wafer == 'W07':
                capture(f'{width}-run-W07-processing.png')
            page.locator('#run-next').click()
            expect(page.locator('#run-progress')).to_contain_text(f'{index + 1} / 3')
            assert page.locator('#run-slots .mini-wafer').count() == 3
            expect(page.locator('#chamber-state')).to_contain_text('Idle')
            if index < 2:
                expect(page.locator('#run-lot-state')).to_contain_text('Processing')
        expect(page.locator('#run-lot-state')).to_contain_text('S20 完成，待進 S30')
        assert page.locator('#run-history li').count() == 6
        expect(page.locator('#run-next')).to_be_disabled()
        capture(f'{width}-run-complete.png')
        page.locator('#run-reset').click()
        expect(page.locator('#run-progress')).to_contain_text('0 / 3')
        page.locator('#run-next').click()
        page.locator('#run-reset').click()
        expect(page.locator('#chamber-state')).to_contain_text('Idle')
        assert page.locator('#run-slots .mini-wafer').count() == 3
        assert page.locator('#run-history li').count() == 0

        go('hold')
        page.locator('#hold-reset').click()
        for decision in ['pending', 'more']:
            page.locator('#review-choice').select_option(decision)
            page.locator('#hold-apply').click()
            page.locator('#hold-start').click()
            expect(page.locator('#hold-status')).to_contain_text('Hold')
            expect(page.locator('#hold-feedback')).to_contain_text('不可開工')
        page.locator('#review-choice').select_option('approved')
        page.locator('#hold-apply').click()
        expect(page.locator('#hold-status')).to_contain_text('Ready')
        page.locator('#hold-start').click()
        expect(page.locator('#hold-feedback')).to_contain_text('不啟動加工')
        expect(page.locator('#hold .status-physical')).to_contain_text('F012／07')
        capture(f'{width}-hold-released.png')
        page.locator('#hold-reset').click()
        expect(page.locator('#hold-status')).to_contain_text('Hold')

        go('reconcile')
        page.locator('#map-reset').click()
        page.locator('#map-validate').click()
        expect(page.locator('#map-count')).to_contain_text('讀取 2 片')
        expect(page.locator('#map-decision')).to_contain_text('暫不放行')
        page.locator('#scan-choice').select_option('wrong')
        page.locator('#scan-apply').click()
        page.locator('#map-validate').click()
        expect(page.locator('#map-count')).to_contain_text('讀取 3 片')
        expect(page.locator('#map-decision')).to_contain_text('暫不放行')
        expect(page.locator('#map-rows .problem')).to_contain_text('W07')
        expect(page.locator('#map-rows .problem')).to_contain_text('W99')
        capture(f'{width}-map-wrong-identity.png')
        page.locator('#scan-choice').select_option('matched')
        page.locator('#scan-apply').click()
        expect(page.locator('#map-decision')).to_contain_text('尚未放行')
        page.locator('#map-validate').click()
        expect(page.locator('#map-decision')).to_contain_text('可進行下一項')
        page.locator('#scan-choice').select_option('missing')
        page.locator('#scan-apply').click()
        expect(page.locator('#map-decision')).to_contain_text('尚未放行')
        page.locator('#map-reset').click()
        expect(page.locator('#map-count')).to_contain_text('讀取 2 片')

    report['checks'] += [
        'Desktop/mobile A: invalid tool or port blocked, transit differs from arrival, identities stable, reset',
        'Desktop/mobile B: wrong recipe/version blocked, occupancy conserved, three completions required, history, mid-run reset',
        'Desktop/mobile C: pending/more reviews remain held, permitted release, no material move or implicit start',
        'Desktop/mobile D: missing versus wrong identity, count alone cannot pass, update invalidates previous decision, reset',
    ]

    for width in [1440, 900, 768, 390, 360]:
        page.set_viewport_size({'width': width, 'height': 1000 if width >= 900 else 844})
        for section in CHAPTERS:
            # Reload for a clean initial state rather than inheriting exercise or disclosure state.
            page.goto(URI + '#' + section)
            page.reload()
            expect(page.locator('#' + section)).to_be_visible()
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'), (width, section)
            if width in [1440, 390, 360]:
                capture(f'{width}-{section}.png')
                report['screens'].append(f'{width}-{section}.png')
            if width < 850:
                page.locator('#menu-toggle').click()
                expect(page.locator('#sidebar')).to_be_visible()
                page.locator(f'[data-step="{section}"]').click()
                expect(page.locator('#sidebar')).not_to_be_visible()
        page.locator('details').evaluate_all('(els) => els.forEach(el => el.open = true)')
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
    report['checks'].append('50 viewport/chapter layouts, 30 clean-state screenshots, mobile menu, expanded sources')

    page.goto((ROOT / 'index.html').as_uri())
    page.locator('.course-continue').click()
    expect(page.locator('#tool')).to_be_visible()
    page.locator('.course-jump a').first.click()
    expect(page.locator('#fab')).to_be_visible()
    report['checks'].append('Bidirectional course links')

    # Preview is separate from offline testing; verify bytes before exercising the served page.
    base = 'http://127.0.0.1:4175/'
    asset_names = ['operations.html', 'operations.js', 'operations.css', 'index.html', 'styles.css']
    report['http_assets'] = {name: hashlib.sha256(urlopen(base + name).read()).hexdigest() ==
                            hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in asset_names}
    assert all(report['http_assets'].values())
    page.goto(base + 'operations.html#run', wait_until='networkidle')
    page.locator('#run-next').click()
    expect(page.locator('#chamber-wafer')).to_have_text('W06')
    capture('live-mobile-run.png')
    report['checks'].append('Live HTTP assets match disk and processing interaction works')
    assert not report['errors'], report['errors']
    browser.close()

report['result'] = 'PASS'
(OUT / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
