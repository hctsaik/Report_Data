"""MES-009 behavior and viewport evidence; does not assign teaching scores."""
from pathlib import Path
import json, hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tests/evidence/mes-009'
OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:4175/'
checks=[]
def check(value,label):
    assert value,label
    checks.append(label)
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    for width in [1440,800,360]:
        page.set_viewport_size({'width':width,'height':1000 if width>760 else 800})
        for lesson in ['qtime','future-hold','part-route','recipes','flow-versions']:
            page.goto(BASE+'advanced.html#'+lesson)
            page.wait_for_function("Array.from(document.images).filter(i=>i.getAttribute('src')).every(i=>i.complete&&i.naturalWidth>0)")
            check(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'{width}/{lesson}: no horizontal overflow')
            page.screenshot(path=str(OUT/f'{lesson}-{width}.png'),full_page=True)
            if lesson!='flow-versions':
                page.locator('.visual').screenshot(path=str(OUT/f'{lesson}-visual-{width}.png'))
                page.locator('.visual').scroll_into_view_if_needed()
                page.screenshot(path=str(OUT/f'{lesson}-reading-{width}.png'))
            if lesson=='flow-versions':
                for variant in ['original','a','b','c']:
                    page.locator(f'[data-variant="{variant}"]').click()
                    page.wait_for_function("Array.from(document.images).filter(i=>i.getAttribute('src')).every(i=>i.complete&&i.naturalWidth>0)")
                    page.screenshot(path=str(OUT/f'flow-{variant}-{width}.png'),full_page=True)
            q=page.locator('.quiz')
            q.locator('button').nth(0).click()
            check(len(q.locator('.answer').inner_text())>10,f'{width}/{lesson}: alternative reasoning')
            q.locator('button').nth(1).click()
            check('正確' in q.locator('.answer').inner_text(),f'{width}/{lesson}: correct reasoning')
    page.set_viewport_size({'width':1440,'height':1000})
    page.goto(BASE+'advanced.html#qtime')
    for minute,expected in [(20,'10'),(30,'0'),(45,'15')]:
        page.locator(f'[data-minute="{minute}"]').click()
        check(page.locator('#q-remaining').inner_text()==expected,f'qtime {minute} arithmetic')
    page.locator('#q-hold').check()
    check('起點維持 10:00' in page.locator('#q-result').inner_text(),'Hold does not reset clock')
    page.locator('#q-stop').select_option('out')
    check('進站不會結束' in page.locator('#q-result').inner_text(),'Move Out differs from Move In')
    page.screenshot(path=str(OUT/'qtime-overdue.png'),full_page=True)
    page.goto(BASE+'advanced.html#future-hold')
    check(page.locator('#future-pending').inner_text()=='待觸發','Future Hold pending')
    check(page.locator('#future-release').is_disabled(),'No early release')
    for i in range(3):page.locator('#future-next').click()
    check(page.locator('#future-pending').inner_text()=='已觸發','Future Hold triggers at S50')
    check(page.locator('#future-next').is_disabled(),'Cannot bypass triggered Hold')
    page.screenshot(path=str(OUT/'future-hold-triggered.png'),full_page=True)
    page.locator('#future-release').click()
    check('其他有效限制' in page.locator('#future-result').inner_text(),'Release is not unconditional permission')
    page.locator('#future-reset').click()
    check(page.locator('#future-pending').inner_text()=='待觸發','Future Hold reset')
    page.goto(BASE+'advanced.html#part-route')
    page.locator('[data-lot="L024"]').click()
    check('S20' in page.locator('#part-ticket').inner_text(),'L024 at S20')
    check('F-DEMO v1' in page.locator('#part-ticket').inner_text(),'Route identity preserved')
    page.goto(BASE+'advanced.html#recipes')
    page.locator('#recipe-equipment').select_option('ETCH-02')
    check(page.locator('#recipe-expected').inner_text()=='ETCH_A_TOOL2','Equipment changes mapping')
    page.locator('#recipe-mismatch').check()
    check('不一致' in page.locator('#recipe-result').inner_text(),'Version mismatch detected')
    page.screenshot(path=str(OUT/'recipe-mismatch.png'),full_page=True)
    page.goto(BASE+'advanced.html#flow-versions')
    page.locator('[data-variant="c"]').click()
    page.locator('#save-variant').click()
    check(page.evaluate("localStorage.getItem('mes-flow-preferred-version')")=='c','Preference saved locally')
    page.reload()
    check('C｜定義對照進度' in page.locator('#variant-saved').inner_text(),'Preference visible after reload')
    page.locator('button[data-zoom]').click()
    check(page.locator('#image-dialog').is_visible(),'Image dialog opens')
    page.keyboard.press('Escape')
    check(not page.locator('#image-dialog').is_visible(),'Image dialog closes with Escape')
    page.goto(BASE+'advanced.html#missing')
    page.wait_for_function("location.hash==='#qtime'")
    check(page.locator('h1').inner_text().startswith('QTime'),'Invalid hash fallback')
    for path,anchor in [('flow.html','stage'),('operations.html','recipe')]:
        page.goto(BASE+path+'#'+anchor)
        check(page.locator('[data-advanced-note] a').count()==1,path+' extension link')
        page.screenshot(path=str(OUT/(path.replace('.html','')+'-entry.png')),full_page=True)
    check(not errors,'No JavaScript errors')
    files=['advanced.html','advanced.css','advanced.js','course-extension.js']+[f'assets/mes-009/{name}.png' for name in ['flow-a','flow-b','flow-c','qtime','future','part','recipes']]
    hashes={}
    for file in files:
        response=page.request.get(BASE+file)
        check(response.status==200,file+' HTTP 200')
        check(response.body()==(ROOT/file).read_bytes(),file+' served bytes equal disk')
        hashes[file]=hashlib.sha256(response.body()).hexdigest()
    (OUT/'results.json').write_text(json.dumps({'checks':checks,'count':len(checks),'errors':errors,'files':hashes},ensure_ascii=False,indent=2),encoding='utf-8')
    browser.close()
print(f'PASS: {len(checks)} checks; screenshots in {OUT}')
