"""End-to-end checks of the actual offline teaching page.

Run: python -X utf8 tests/check_lesson.py
Requires Playwright and its Chromium browser. No dependency is needed to view the site.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'tests' / 'evidence'
EVIDENCE.mkdir(parents=True, exist_ok=True)
SECTIONS = ['fab', 'wafer', 'foup', 'slot', 'lot', 'explore', 'check']
report = {'checks': [], 'viewports': [], 'errors': []}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
    page.on('pageerror', lambda error: report['errors'].append(str(error)))
    page.goto((ROOT / 'index.html').as_uri())
    expect(page.locator('#fab')).to_be_visible()
    expect(page.locator('#previous')).to_be_disabled()
    for section in SECTIONS[1:]:
        page.locator('#next').click()
        expect(page.locator(f'#{section}')).to_be_visible()
        assert page.locator('.lesson:visible').count() == 1
    page.locator('#previous').click()
    expect(page.locator('#explore')).to_be_visible()
    report['checks'].append('Offline file loading and forward/backward chapter navigation')

    for slot, wafer in [(6, 'W06'), (8, 'W08'), (7, 'W07')]:
        page.locator(f'[data-slot="{slot}"]').click()
        expect(page.locator('#value-wafer')).to_have_text(wafer)
        expect(page.locator('#value-slot')).to_have_text(str(slot).zfill(2))
        expect(page.locator('#value-foup')).to_have_text('F012')
        expect(page.locator('#value-lot')).to_have_text('L023')
        expect(page.locator('#quick-selection')).to_contain_text(wafer)
    page.locator('[data-slot="5"]').click()
    expect(page.locator('#value-wafer')).to_have_text('—')
    expect(page.locator('#value-lot')).to_have_text('—')
    expect(page.locator('#value-slot')).to_have_text('05')
    report['checks'].append('Three wafer selections and empty slot have coherent records')

    page.locator('[data-slot="8"]').click()
    page.locator('#transfer').click()
    expect(page.locator('#value-wafer')).to_have_text('W08')
    expect(page.locator('#value-foup')).to_have_text('F018')
    expect(page.locator('#value-slot')).to_have_text('04')
    expect(page.locator('#value-lot')).to_have_text('L023')
    expect(page.locator('#transfer')).to_be_disabled()
    for slot, wafer in [(2, 'W06'), (3, 'W07'), (4, 'W08')]:
        page.locator(f'[data-slot="{slot}"]').click()
        expect(page.locator('#value-wafer')).to_have_text(wafer)
        expect(page.locator('#value-slot')).to_have_text(str(slot).zfill(2))
    page.screenshot(path=str(EVIDENCE / 'desktop-transfer.png'), full_page=True)
    page.locator('#reset').click()
    expect(page.locator('#value-wafer')).to_have_text('W07')
    expect(page.locator('#value-foup')).to_have_text('F012')
    expect(page.locator('#value-slot')).to_have_text('07')
    page.locator('[data-slot="9"]').click()
    page.locator('#transfer').click()
    expect(page.locator('#value-wafer')).to_have_text('W07')
    expect(page.locator('#transfer-result')).to_contain_text('空槽位不會被搬走')
    page.locator('#reset').click()
    report['checks'].append('Whole-lot transfer preserves identities, maps all slots, handles empty selection, resets')

    page.locator('[data-slot="6"]').focus()
    page.keyboard.press('Enter')
    expect(page.locator('#value-wafer')).to_have_text('W06')
    expect(page.locator('[data-slot="6"]')).to_be_focused()
    report['checks'].append('Keyboard wafer selection retains focus')

    page.goto((ROOT / 'index.html').as_uri() + '#fab')
    page.locator('#fab [data-zoom]').click()
    expect(page.locator('#image-dialog')).to_be_visible()
    page.locator('#zoom-size').click()
    assert page.locator('.zoom-viewport').evaluate('(el) => el.scrollWidth > el.clientWidth')
    page.keyboard.press('Escape')
    expect(page.locator('#image-dialog')).not_to_be_visible()
    expect(page.locator('#fab [data-zoom]')).to_be_focused()
    report['checks'].append('Image zoom, native-size scrolling, Escape and focus restoration')

    page.goto((ROOT / 'index.html').as_uri() + '#check')
    for quiz, wrong, right in [('location', 'lot', 'foup'), ('move', 'identity', 'position'), ('empty', 'gone', 'exists')]:
        page.locator(f'[data-quiz="{quiz}"] [data-answer="{wrong}"]').click()
        expect(page.locator(f'[data-quiz="{quiz}"] .feedback')).to_be_visible()
        page.locator(f'[data-quiz="{quiz}"] [data-answer="{right}"]').click()
        expect(page.locator(f'[data-quiz="{quiz}"] .feedback')).to_contain_text('答對了')
    expect(page.locator('#quiz-summary')).to_contain_text('3 / 3')
    page.locator('[data-quiz="location"] [data-answer="lot"]').click()
    expect(page.locator('#quiz-summary')).to_contain_text('2 / 3')
    report['checks'].append('Every quiz wrong/right explanation and recomputed summary')

    for width in [1440, 390, 360]:
        page.set_viewport_size({'width': width, 'height': 1000 if width == 1440 else 844})
        for section in SECTIONS:
            page.goto((ROOT / 'index.html').as_uri() + '#' + section)
            page.locator('details').evaluate_all('(els) => els.forEach(el => el.open = false)')
            expect(page.locator(f'#{section}')).to_be_visible()
            overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth')
            assert not overflow, (width, section, 'horizontal overflow')
            assert page.locator('img').evaluate_all('(imgs) => imgs.every(i => i.complete && i.naturalWidth > 0)')
            page.screenshot(path=str(EVIDENCE / f'{width}-{section}.png'), full_page=True)
            if width != 1440:
                page.locator('#menu-toggle').click()
                expect(page.locator('#sidebar')).to_be_visible()
                page.locator(f'[data-step="{section}"]').click()
                expect(page.locator('#sidebar')).not_to_be_visible()
            report['viewports'].append({'width': width, 'section': section, 'overflow': False})
        # Check expanded content too, including long links and image review.
        page.locator('details').evaluate_all('(els) => els.forEach(el => el.open = true)')
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
    report['checks'].append('21 chapter/viewport screenshots, no overflow, images loaded, mobile navigation and expanded content')

    page.goto((ROOT / 'index.html').as_uri() + '#view=lesson&lesson=fab&slide=6')
    expect(page.locator('#explore')).to_be_visible()
    page.goto((ROOT / 'index.html').as_uri() + '#unknown')
    expect(page.locator('#fab')).to_be_visible()
    report['checks'].append('Vision-AI-style deep link and invalid hash fallback')
    assert not report['errors'], report['errors']
    browser.close()

report['result'] = 'PASS'
(EVIDENCE / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
