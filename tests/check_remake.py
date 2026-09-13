"""MES-004 live rendering evidence. This verifies behavior/coverage, not teaching quality."""
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tests/evidence/mes-004'
OUT.mkdir(parents=True,exist_ok=True)
SCOPE={'operations':['port','recipe','chamber','state','handoff','lab'],
       'flow':['stage','step','lot-flow','execution','branching','rework','split-merge','versions','lab']}
ASSETS=['operations.html','flow.html','course-content.js','course-remake.js','course.js','scenarios.js','course.css','course-remake.css']
BASE='http://127.0.0.1:4175/'
report={'pages':[],'states':[],'frames':[],'exercises':[],'errors':[],'assets':{}}
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
initial_assets={name:sha(ROOT/name) for name in ASSETS}
def evidence(page,name,scene=True):
    page.evaluate('window.scrollTo(0,0)')
    page.screenshot(path=str(OUT/(name+'-page.png')),full_page=True)
    if scene:
        # Fixed site chrome is not part of a diagram; preserve it in full-page evidence.
        page.locator('.teaching-scene').screenshot(path=str(OUT/(name+'-scene.png')),style='.topbar{visibility:hidden!important}')
    return {k:{'path':str((OUT/(name+'-'+k+'.png')).relative_to(ROOT)).replace('\\','/'),
               'sha256':sha(OUT/(name+'-'+k+'.png'))} for k in (['page','scene'] if scene else ['page'])}

with sync_playwright() as p:
    browser=p.chromium.launch()
    for width in [1440,360]:
        page=browser.new_page(viewport={'width':width,'height':1000 if width==1440 else 844},reduced_motion='reduce')
        page.on('pageerror',lambda e:report['errors'].append(str(e)))
        for course,lessons in SCOPE.items():
            for lesson in lessons:
                page.goto(BASE+course+'.html#'+lesson,wait_until='networkidle')
                assert page.locator('.teaching-scene').count()==1,(course,lesson)
                assert page.locator('.lesson h1').count()==1
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(course,lesson,width,'overflow')
                box=page.locator('.teaching-scene').bounding_box()
                assert box['width']>=290
                report['pages'].append({'id':course+'/'+lesson,'width':width,'sceneWidth':round(box['width']),
                                        'evidence':evidence(page,f'{course}-{lesson}-{width}')})
                for button in page.locator('[data-frame]').all():
                    button.click()
                    assert button.get_attribute('aria-pressed')=='true'
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(lesson,width,'frame overflow')
                    idx=button.get_attribute('data-frame-index')
                    path=OUT/f'{course}-{lesson}-frame{idx}-{width}.png'
                    page.locator('.teaching-scene').screenshot(path=str(path),style='.topbar{visibility:hidden!important}')
                    report['frames'].append({'id':course+'/'+lesson,'frame':idx,'width':width,'path':str(path.relative_to(ROOT)).replace('\\','/')})
                for button in page.locator('[data-answer]').all():
                    button.focus();page.keyboard.press('Enter')
                    assert page.locator('.exercise-response').inner_text().strip()
                    assert button.get_attribute('aria-pressed')=='true'
                    report['exercises'].append({'id':course+'/'+lesson,'width':width,'answer':button.get_attribute('data-answer')})
            page.goto(BASE+course+'.html#lab',wait_until='networkidle')
            cases=page.evaluate('SCENARIOS[courseKey].map(s=>({id:s.id,nodes:Object.keys(s.nodes)}))')
            for case in cases:
                page.locator(f'[data-scenario="{case["id"]}"]').click()
                for node in case['nodes']:
                    # Exhaustive snapshot display inspection supplements actual journey clicks in check_courses.py.
                    page.evaluate('(id)=>{getEngine().nodeId=id;renderLab()}',node)
                    s=page.evaluate('getEngine().state')
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(course,case['id'],node,width)
                    text=page.locator('.lab-story').inner_text()
                    assert s['lot'] in text and s['current'] in text and s['status'] in text
                    for h in s['hold']: assert h in text
                    if course=='operations' and case['id'] in ['run','fault','hold']:
                        ids=page.locator('.lab-story .station-line .silicon strong').all_text_contents()
                        assert sorted(x for x in ids if x!='空')==sorted(s['waferIds']),(case['id'],node,ids)
                        if s['chamber']: assert page.locator('.lab-story .chamber-body').inner_text().find(s['chamber'])>=0
                    if case['id']=='reconcile':
                        assert s['scan'][1].split('=')[1] in text
                    if case['id']=='revisit':
                        assert 'S50 Fail' not in text,'invented failure history leaked from rework'
                    if s.get('qtime',0)>30:
                        bar=page.locator('.qtime-track>span')
                        assert bar.evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgb(186, 109, 50)'
                        assert '30 分上限' in text
                    if s.get('lots'):
                        for lot in s['lots']:
                            assert lot['id'] in text and lot['current'] in text
                    path=OUT/f'{course}-lab-{case["id"]}-{node}-{width}.png'
                    page.locator('.lab-story').screenshot(path=str(path),style='.topbar{visibility:hidden!important}')
                    report['states'].append({'course':course,'case':case['id'],'node':node,'width':width,
                                            'path':str(path.relative_to(ROOT)).replace('\\','/'),'sha256':sha(path)})
        page.close()
    browser.close()
for name in ASSETS:
    assert sha(ROOT/name)==initial_assets[name],('source changed during capture; rerun',name)
    assert urlopen(BASE+name).read()==(ROOT/name).read_bytes(),name
    report['assets'][name]=sha(ROOT/name)
assert not report['errors'],report['errors']
(OUT/'render-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pages':len(report['pages']),'states':len(report['states']),'frames':len(report['frames']),
                  'exerciseChoices':len(report['exercises']),'assets':len(report['assets']),'status':'PASS'}))
