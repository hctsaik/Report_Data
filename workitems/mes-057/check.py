from pathlib import Path
import hashlib
import json
import subprocess
from playwright.sync_api import sync_playwright

out = Path('tests/evidence/mes-057')
out.mkdir(parents=True, exist_ok=True)
checks, errors, metrics = [], [], {}

def check(value, label):
    assert value, label
    checks.append(label)

with sync_playwright() as p:
    browser = p.chromium.launch()
    for width in [1440, 390]:
        page = browser.new_page(viewport={'width': width, 'height': 1000}, has_touch=True)
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto('http://127.0.0.1:4175/er-atlas.html?mesFrom=mu1i1b25a547qm&erNode=t_cfc81de70314', wait_until='networkidle')
        page.wait_for_function('window.ER_ATLAS && ER_FOCUS.getState().root')
        check(page.evaluate('ER_FOCUS.getState().root') == 't_cfc81de70314', f'{width} exact deep link')
        check(page.evaluate('MES_CATALOG.locate(location.href)') is None, f'{width} no incorrect course unit')
        check(page.evaluate("MES_CATALOG.locate('er-atlas.html?view=questions').id") == 8, f'{width} question unit preserved')
        check(page.evaluate("MES_CATALOG.locate('topic.html?topic=lot').id") == 1, f'{width} Lot topic unit preserved')
        rect = page.locator('#canvas').bounding_box()
        metrics[width] = {'canvas_top': rect['y'], 'visible_height': min(rect['height'], 1000-rect['y'])}
        check(metrics[width]['visible_height'] >= 250, f'{width} diagram visible in first screen')
        page.screenshot(path=str(out / f'after-{width}.png'))
        page.locator('.toolbar a[href="#inspector"]').click()
        page.wait_for_timeout(200)
        check(page.locator('#inspector').bounding_box()['y'] < 50, f'{width} jump to explanation')
        page.screenshot(path=str(out / f'related-{width}.png'))
        page.locator('#selection-details').evaluate('(el)=>el.scrollIntoView({block:"start",behavior:"instant"})')
        page.screenshot(path=str(out / f'lesson-{width}.png'))
        page.locator('.map-guide summary').click()
        check(page.locator('.map-guide a[download]').is_visible(), f'{width} original download available')
        check(page.locator('.legend').is_visible(), f'{width} legend available')
        check('?' * 5 not in page.locator('body').inner_text(), f'{width} text encoding')
        check(page.evaluate('document.documentElement.scrollWidth<=innerWidth'), f'{width} no overflow')
        page.close()
    browser.close()
for path in ['ER/INTEGRATED/fab-er-v2.svg', 'ER/INTEGRATED/er-model-v2.json']:
    baseline = subprocess.check_output(['git', 'rev-parse', '15654c9:' + path]).strip()
    current = subprocess.check_output(['git', 'hash-object', '--path=' + path, path]).strip()
    check(baseline == current, path + ' unchanged (Git newline normalization)')
check(not errors, 'No JavaScript errors')
(out / 'checks.json').write_text(json.dumps({'checks': checks, 'metrics': metrics, 'errors': errors}, ensure_ascii=False, indent=2), encoding='utf-8')
print('PASS', len(checks), metrics)
