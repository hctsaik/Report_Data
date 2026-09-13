from pathlib import Path
import json,hashlib
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];out=root/'tests/evidence/mes-011';out.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page()
    page.on('pageerror',lambda e:errors.append(str(e)))
    for width in [1440,360]:
        page.set_viewport_size({'width':width,'height':1000})
        for n in range(2671,2678):
            page.goto(f'http://127.0.0.1:4175/data-map.html#{n}')
            page.wait_for_function("/目前聚焦|逐點讀圖/.test(document.querySelector('#map-caption').textContent)")
            assert page.locator('h1').inner_text()
            for i in [0,1]:
                page.locator(f'[data-case="{i}"]').click()
                assert page.locator(f'[data-case="{i}"]').get_attribute('aria-pressed')=='true'
                assert page.locator('.mapping article').count()==3
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                assert page.locator('#er-object').evaluate("o=>o.contentDocument.querySelectorAll('#nodes>g[style]').length>0")
                assert page.locator('[data-node]').count()>1
                page.screenshot(path=str(out/f'{n}-{width}-case{i}.png'),full_page=True)
                checks.append(f'{n}/{width}/case{i} rendered, no overflow, focus visible')
            before=page.locator('#er-object').evaluate("o=>o.contentDocument.documentElement.getAttribute('viewBox')")
            page.locator('#all-map').click()
            assert page.locator('#map-caption').inner_text().startswith('完整原圖')
            assert page.locator('#er-object').evaluate("o=>o.contentDocument.documentElement.getAttribute('viewBox')")!=before
            page.locator('#zoom-in').click();assert page.locator('#zoom-value').inner_text()=='150%'
            page.locator('#zoom-out').click();assert page.locator('#zoom-value').inner_text()=='100%'
            page.locator('#focus-map').click()
            page.locator('[data-node]').last.click()
            assert page.locator('#map-caption').inner_text().startswith('逐點讀圖')
            for answer in [0,1]:
                page.locator(f'[data-answer="{answer}"]').click()
                assert page.locator('#feedback').inner_text()
            checks.append(f'{n}/{width} full/focus/zoom/quiz')
        for entry in ['index.html#fab','advanced.html#recipes','support.html#monitor','operations.html#port','flow.html#stage','freshness.html']:
            page.goto('http://127.0.0.1:4175/'+entry)
            page.wait_for_selector('a[href^="data-map.html"]',state='attached')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),entry
            checks.append(f'{entry}/{width} entry exists and no overflow')
    page.goto('http://127.0.0.1:4175/data-map.html#invalid');page.wait_for_selector('[data-case]');assert '2671' in page.locator('.provenance').first.inner_text()
    browser.close()
assert not errors,errors
hashes=json.loads((root/'workitems/mes-011/original-svg-hashes.json').read_text())
for name,h in hashes.items():assert hashlib.sha256((root/'ER/NEW'/name).read_bytes()).hexdigest()==h
(out/'results.json').write_text(json.dumps({'checks':checks,'count':len(checks),'errors':errors,'original_svgs_unchanged':7},ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS:',len(checks),'checks; 7 original SVGs unchanged.')
