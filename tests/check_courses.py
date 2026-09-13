"""Actual rendered teaching pages, independent scenario journeys and layout evidence."""
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tests/evidence/mes-007/regression'
OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:4175/'
report={'layouts':[],'journeys':[],'errors':[],'assets':{}}

with sync_playwright() as p:
    browser=p.chromium.launch()
    for width in [1440,390,360]:
        page=browser.new_page(viewport={'width':width,'height':1000 if width==1440 else 844},reduced_motion='reduce')
        page.on('pageerror',lambda err:report['errors'].append(str(err)))
        for course in ['operations','flow']:
            page.goto((ROOT/f'{course}.html').as_uri(),wait_until='networkidle')
            chapters=page.evaluate('course.lessons.map(l=>l.id)')
            for i,chapter in enumerate(chapters):
                page.evaluate('(id)=>location.hash=id',chapter)
                expect(page.locator(f'article.lesson#{chapter}')).to_be_visible()
                expect(page.locator('.lesson')).to_have_count(1)
                expect(page.locator('.lesson h1')).to_have_count(1)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),(course,chapter,width)
                for img in page.locator('.art img').all():
                    expect(img).to_be_visible()
                    img.evaluate('(img)=>img.decode()')
                    assert img.evaluate('img=>img.complete&&img.naturalWidth>=800')
                    assert ('-mobile.png' in img.evaluate('img=>img.currentSrc')) == (width<=560)
                    img.click()
                    expect(page.locator('dialog')).to_be_visible()
                    page.locator('#zoom-toggle').click()
                    assert page.locator('.zoom-view').evaluate('el=>el.scrollWidth>=el.clientWidth')
                    page.keyboard.press('Escape')
                    expect(page.locator('dialog')).not_to_be_visible()
                if width in [1440,360]:
                    page.evaluate('window.scrollTo(0,0)')
                    page.screenshot(path=str(OUT/f'{course}-{chapter}-{width}.png'),full_page=True)
                report['layouts'].append({'course':course,'chapter':chapter,'width':width,'overflow':False})
            # Browser history and mobile menu must select the actual chapter.
            page.evaluate("location.hash='lab'")
            expect(page.locator('#lab')).to_be_visible()
            page.locator('#previous').click()
            expect(page.locator('article.lesson')).to_have_attribute('id',chapters[-2])
            page.go_back()
            expect(page.locator('#lab')).to_be_visible()
            if width<800:
                page.locator('#menu-toggle').click()
                expect(page.locator('#sidebar')).to_be_visible()
                page.locator(f'[data-lesson="{chapters[0]}"]').click()
                expect(page.locator('#sidebar')).not_to_be_visible()
                page.evaluate("location.hash='lab'")
                expect(page.locator('#lab')).to_be_visible()
            if width not in [1440,360]:
                continue
            cases=page.evaluate('SCENARIOS[courseKey].map(s=>s.id)')
            for case in cases:
                page.locator(f'[data-scenario="{case}"]').click()
                page.locator('#reset-scenario').click()
                assert page.evaluate('getEngine().nodeId')=='start'
                steps=0
                while steps<20:
                    choices=page.evaluate('getEngine().node.actions')
                    invalid=next((i for i,a in enumerate(choices) if not a['next']),None)
                    if invalid is not None:
                        before=page.evaluate('JSON.stringify(getEngine().state)')
                        page.locator(f'[data-action="{invalid}"]').click()
                        assert before==page.evaluate('JSON.stringify(getEngine().state)')
                        expect(page.locator('#scenario-feedback')).to_have_class('feedback reject')
                    valid=next((i for i,a in enumerate(choices) if a['next']),None)
                    if valid is None:break
                    button=page.locator(f'[data-action="{valid}"]')
                    if steps==0:
                        button.focus();page.keyboard.press('Enter')
                    else:button.click()
                    steps+=1
                    expect(page.locator('#scenario-feedback')).to_have_class('feedback accept')
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                    if case=='run' and page.evaluate('getEngine().nodeId')=='run1':
                        page.evaluate('window.scrollTo(0,0)')
                        page.screenshot(path=str(OUT/f'run-W07-{width}.png'),full_page=True)
                assert steps<20
                if case in ['rework','split','version','normal']:
                    page.evaluate('window.scrollTo(0,0)')
                    page.screenshot(path=str(OUT/f'{case}-complete-{width}.png'),full_page=True)
                report['journeys'].append({'course':course,'case':case,'width':width,'acceptedActions':steps,'lastNode':page.evaluate('getEngine().nodeId')})
                page.locator('#reset-scenario').click()
                assert page.evaluate('getEngine().events.length')==1
            # Explicit alternate quality/rework/time branches.
            if course=='flow':
                for case,path,expected in [('branch',[2],'fail'),('rework',[1,0,1],'limit'),('qtime',[1,1],'finish')]:
                    page.locator(f'[data-scenario="{case}"]').click();page.locator('#reset-scenario').click()
                    for action in path:page.locator(f'[data-action="{action}"]').click()
                    assert page.evaluate('getEngine().nodeId')==expected
                    assert 'Hold' in page.evaluate('getEngine().state.status')
        page.close()
    # Offline links and live assets both matter after the second-course replacement.
    page=browser.new_page(viewport={'width':390,'height':844})
    page.goto(BASE+'operations.html#arrival',wait_until='networkidle')
    expect(page.locator('#lab')).to_be_visible()
    assert page.evaluate('activeScenario')=='arrival'
    page.goto(BASE+'flow.html#lot-flow',wait_until='networkidle')
    expect(page.locator('article.lesson')).to_have_attribute('id','lot-flow')
    page.screenshot(path=str(OUT/'http-flow-390.png'),full_page=True)
    browser.close()

files=['index.html','operations.html','flow.html','course.css','course.js','course-content.js','scenarios.js']+[str(p.relative_to(ROOT)).replace('\\','/') for p in (ROOT/'assets/mes-v2').glob('*.png')]
for name in files:
    local=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    served=hashlib.sha256(urlopen(BASE+name).read()).hexdigest()
    assert local==served,name
    report['assets'][name]=local
assert not report['errors'],report['errors']
(OUT/'browser-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f"PASS: {len(report['layouts'])} chapter layouts, {len(report['journeys'])} UI journeys, alternate branches, modal, keyboard, history, HTTP assets; no JS errors")
