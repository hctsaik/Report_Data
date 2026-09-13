"""MES-007 actual page evidence and behavior; no automatic teaching score."""
from pathlib import Path
import json,hashlib
from urllib.request import urlopen
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tests/evidence/mes-007';OUT.mkdir(parents=True,exist_ok=True)
SCOPE={'operations':['port','recipe','chamber','state','handoff','lab'],'flow':['stage','step','lot-flow','execution','branching','rework','split-merge','versions','lab'],'freshness':['architecture','decision','ai','history','join','contract']}
report={'pages':[],'interactions':[],'errors':[],'assets':{}}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def screenshot(page,name):
    page.evaluate('window.scrollTo(0,0)');page.wait_for_timeout(150)
    path=OUT/(name+'.png');page.screenshot(path=str(path),full_page=True,animations='disabled')
    return {'path':str(path.relative_to(ROOT)).replace('\\','/'),'sha256':sha(path)}
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,360]:
  page=b.new_page(viewport={'width':width,'height':1000 if width==1440 else 844},reduced_motion='reduce')
  page.on('pageerror',lambda e:report['errors'].append(str(e)))
  for course,chapters in SCOPE.items():
   for chapter in chapters:
    page.goto(f'http://127.0.0.1:4175/{course}.html#{chapter}',wait_until='networkidle')
    page.wait_for_function('Array.from(document.images).filter(i=>i.getAttribute("src")).every(i=>i.complete&&i.naturalWidth>0)')
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(course,chapter,width,'overflow')
    assert page.locator('h1').count()==1
    row={'id':course+'/'+chapter,'width':width,'page':screenshot(page,f'{course}-{chapter}-{width}')}
    if course!='freshness':
     assert page.locator('.lesson-illustration').count()==1
     for im in page.locator('.lesson-illustration img').all():
      asset=im.get_attribute('src');report['assets'][asset]=sha(ROOT/asset)
     art=page.locator('.lesson-illustration')
     path=OUT/f'{course}-{chapter}-{width}-art.png';art.screenshot(path=str(path),style='.topbar{visibility:hidden!important}',animations='disabled')
     row['art']={'path':str(path.relative_to(ROOT)).replace('\\','/'),'sha256':sha(path)}
     if width==360:
      row['panels']=[]
      for i,panel in enumerate(page.locator('.illustrated-panel').all()):
       path=OUT/f'{course}-{chapter}-mobile-panel{i}.png';panel.screenshot(path=str(path),style='.topbar{visibility:hidden!important}')
       row['panels'].append(str(path.relative_to(ROOT)).replace('\\','/'))
     button=page.locator('.lesson-illustration .open-art:visible').first
     button.click();assert page.locator('#image-dialog').evaluate('(e)=>e.open')
     page.keyboard.press('Escape');assert not page.locator('#image-dialog').evaluate('(e)=>e.open')
     drill=page.locator('.evidence-drill')
     if drill.count():
      drill.locator('summary').first.click()
      for frame in page.locator('[data-frame]').all():
       frame.click();assert frame.get_attribute('aria-pressed')=='true'
       report['interactions'].append([course,chapter,width,'frame',frame.inner_text()])
     if chapter=='lab':
      page.locator('[data-start-lab]').click();assert not page.locator('.lab-introduction').evaluate('(e)=>e.open')
      for choice in page.locator('[data-scenario]').all():
       choice.click();assert choice.get_attribute('aria-pressed')=='true'
       assert page.locator('#sim-state').inner_text().strip()
       report['interactions'].append([course,width,'scenario',choice.get_attribute('data-scenario')])
    else:
     if page.locator('.fresh-figure').count():
      path=OUT/f'freshness-{chapter}-{width}-art.png';page.locator('.fresh-figure').screenshot(path=str(path),style='.topbar{visibility:hidden!important}')
      row['art']={'path':str(path.relative_to(ROOT)).replace('\\','/'),'sha256':sha(path)}
     if chapter=='decision':
      for v in ['analysis','monitor','control']:
       page.select_option('#decision-purpose',v);assert page.locator(f'[data-level="{v}"]').evaluate('(e)=>e.classList.contains("selected")')
       report['interactions'].append([chapter,width,v,screenshot(page,f'freshness-{chapter}-{v}-{width}')])
     if chapter=='ai':
      for source,time,step,age in [('native','10:00','ETCH','1 分鐘'),('mart','09:51','DEV','10 分鐘'),('tx','10:01','ETCH','0 分鐘')]:
       for purpose in ['monitor','control']:
        page.select_option('#ai-source',source);page.select_option('#ai-tolerance',purpose)
        assert page.locator('#query-time').inner_text()==time
        assert page.locator('#query-step').inner_text()==step
        assert page.locator('#query-age').inner_text()==age
        if purpose=='control':assert '重驗' in page.locator('#ai-answer').inner_text()
        if purpose=='control' and source=='mart':assert '改找 Native 或 TX' not in page.locator('#ai-answer').inner_text()
        report['interactions'].append([chapter,width,source,purpose,screenshot(page,f'freshness-ai-{source}-{purpose}-{width}')])
     if chapter=='history':
      for q in ['event','current']:
       for complete in ['yes','no']:
        page.select_option('#history-question',q);page.select_option('#history-complete',complete)
        if q=='event' and complete=='no':assert '不能回答' in page.locator('#history-answer').inner_text()
        report['interactions'].append([chapter,width,q,complete,screenshot(page,f'freshness-history-{q}-{complete}-{width}')])
     if chapter=='join':
      page.click('#refresh-table');assert page.locator('#join-refresh-time').inner_text()=='10:01';assert '09:51' in page.locator('.older-field').inner_text()
      report['interactions'].append([chapter,width,'refresh',screenshot(page,f'freshness-join-refreshed-{width}')])
      page.click('#reset-join');assert page.locator('#join-refresh-time').inner_text()=='10:00'
     if chapter=='contract':
      for choice in page.locator('[data-fresh-quiz]').all():
       choice.focus();page.keyboard.press('Enter');assert choice.get_attribute('aria-pressed')=='true'
       assert len(page.locator('#quiz-answer').inner_text())>25
       report['interactions'].append([chapter,width,'quiz',choice.get_attribute('data-fresh-quiz')])
    report['pages'].append(row)
  page.close()
 b.close()
for file in ['course-illustrated.js','course-illustrated.css','course.js','course-remake.js','course-remake.css','course-content.js','course.css','scenarios.js','operations.html','flow.html','freshness.html','freshness.js','freshness.css','index.html']:
 report['assets'][file]=sha(ROOT/file)
for file,digest in report['assets'].items():
 assert hashlib.sha256(urlopen('http://127.0.0.1:4175/'+file).read()).hexdigest()==digest,('HTTP mismatch',file)
assert not report['errors'],report['errors']
(OUT/'render-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'PASS: {len(report["pages"])} layouts, {len(report["interactions"])} interactions, {len(report["assets"])} disk/HTTP assets.')
