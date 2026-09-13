"""MES-010: local teaching behavior, responsive evidence and source identity."""
from pathlib import Path
import json,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/evidence/mes-010';OUT.mkdir(exist_ok=True,parents=True)
checks=[]
def check(value,label):
    assert value,label
    checks.append(label)
BASE='http://127.0.0.1:4175/'
with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    for width in [1440,800,360]:
        page.set_viewport_size({'width':width,'height':1000 if width>760 else 800})
        for key in ['cw','subroute','move','monitor']:
            page.goto(BASE+'support.html#'+key)
            page.reload()
            page.wait_for_function("Array.from(document.images).filter(i=>i.getAttribute('src')).every(i=>i.complete&&i.naturalWidth>0)")
            check(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'{key}/{width} no overflow')
            page.screenshot(path=str(OUT/f'{key}-{width}.png'),full_page=True)
            page.locator('.visual').screenshot(path=str(OUT/f'{key}-visual-{width}.png'))
            if key=='cw':
                for job in ['monitor','dummy','seasoning']:
                    page.locator(f'[data-cw="{job}"]').click()
                    page.locator('.visual').screenshot(path=str(OUT/f'cw-{job}-{width}.png'))
                    check(page.locator(f'[data-cw="{job}"]').get_attribute('aria-pressed')=='true',f'CW {job}/{width} selection')
            quiz=page.locator('.quiz')
            for answer in [0,1]:
                quiz.locator('button').nth(answer).click()
                check(len(quiz.locator('.answer').inner_text())>10,f'{key}/{width} explanation {answer}')
            if width==360:page.locator('.concept-illustration summary').click()
            page.locator('button[data-zoom]').click()
            check(page.locator('#image-dialog').is_visible(),f'{key}/{width} image opens')
            page.keyboard.press('Escape')
            check(not page.locator('#image-dialog').is_visible(),f'{key}/{width} image closes')
        for key in ['qtime','future-hold','part-route','recipes','flow-versions']:
            page.goto(BASE+'advanced.html#'+key)
            check(page.locator('header a[href="support.html#cw"]').count()==1,f'advanced/{key}/{width} new entry')
            check(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'advanced/{key}/{width} no overflow')
            page.screenshot(path=str(OUT/f'entry-{key}-{width}.png'))
    for width in [1440,360]:
        page.set_viewport_size({'width':width,'height':1000 if width>760 else 800})
        page.goto(BASE+'support.html#subroute')
        page.reload()
        check('F-DEMO v1' in page.locator('#route-current').inner_text(),'Sub Route starts at main')
        page.locator('#route-next').click()
        check(page.locator('#route-current').inner_text()=='SR-ADD v1','Sub Route current route changes')
        page.screenshot(path=str(OUT/f'subroute-away-{width}.png'),full_page=True)
        page.locator('#route-next').click()
        page.locator('#route-wrong').click()
        check('不能直接回 S60' in page.locator('#route-feedback').inner_text(),'Wrong return blocked')
        check(page.locator('#route-current').inner_text()=='SR-ADD v1','Wrong return keeps state')
        page.locator('#route-next').click()
        check(page.locator('#route-current').inner_text()=='F-DEMO v1','Returns to main')
        check('S50' in page.locator('#route-position').inner_text(),'Returns to same S50')
        check('未自動過站' in page.locator('#route-position').inner_text(),'Return not completion')
        page.screenshot(path=str(OUT/f'subroute-return-{width}.png'),full_page=True)
        page.locator('#route-reset').click()
        check('尚未離開' in page.locator('#route-position').inner_text(),'Sub Route reset')
        page.goto(BASE+'support.html#move')
        page.reload()
        check(page.locator('#move-count').inner_text()=='3','Three initial moves')
        check(page.locator('#lot-count').inner_text()=='1','One unique lot')
        check(page.locator('#rework-count').inner_text()=='1','Rework included')
        page.locator('#move-rework').click()
        check(page.locator('#move-count').inner_text()=='4','Another rework increments move')
        page.locator('#move-duplicate').click()
        check(page.locator('#move-count').inner_text()=='4','Duplicate does not increment')
        page.screenshot(path=str(OUT/f'move-duplicate-{width}.png'),full_page=True)
        page.locator('#move-normal').click()
        check(page.locator('#move-count').inner_text()=='5','Normal increments move')
        check(page.locator('#lot-count').inner_text()=='1','Same lot remains one')
        page.locator('#move-reset').click()
        check(page.locator('#move-count').inner_text()=='3','Move reset')
        page.goto(BASE+'support.html#monitor')
        page.reload()
        page.locator('#try-process').click()
        check('不能生產加工' in page.locator('#process-result').inner_text(),'Expired MON blocks despite PM done')
        for phase in [1,2]:
            page.locator('#mon-next').click();page.locator('#try-process').click()
            check('不能生產加工' in page.locator('#process-result').inner_text(),f'MON phase {phase} does not bypass EMS')
        page.screenshot(path=str(OUT/f'monitor-accepted-not-updated-{width}.png'),full_page=True)
        page.locator('#mon-next').click();page.locator('#try-process').click()
        check('檢查已通過' in page.locator('#process-result').inner_text(),'EMS update clears this condition')
        page.locator('#other-hold').check();page.locator('#try-process').click()
        check('另有有效 Hold' in page.locator('#process-result').inner_text(),'Other Hold still blocks')
        page.locator('#other-hold').uncheck();page.locator('#pm-done').uncheck();page.locator('#try-process').click()
        check('PM 尚未完成' in page.locator('#process-result').inner_text(),'PM incomplete still blocks')
        page.screenshot(path=str(OUT/f'monitor-other-conditions-{width}.png'),full_page=True)
    page.goto(BASE+'support.html#unknown');page.wait_for_function("location.hash==='#cw'")
    check(page.locator('h1').inner_text().startswith('CW'),'Unknown hash fallback')
    files=['support.html','support.css','support.js','advanced.html','advanced.css']+[f'assets/mes-010/{k}.png' for k in ['cw','subroute','move','monitor']]
    hashes={}
    for name in files:
        r=page.request.get(BASE+name)
        check(r.status==200 and r.body()==(ROOT/name).read_bytes(),name+' disk matches HTTP')
        hashes[name]=hashlib.sha256(r.body()).hexdigest()
    check(not errors,'No JS errors')
    (OUT/'results.json').write_text(json.dumps({'count':len(checks),'checks':checks,'errors':errors,'files':hashes},ensure_ascii=False,indent=2),encoding='utf-8')
    browser.close()
print('PASS:',len(checks),'checks; evidence:',OUT)
