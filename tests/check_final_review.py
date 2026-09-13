"""Focused final review after mobile table, route disclosure and copy fixes."""
import hashlib,json
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/evidence/mes-003';BASE='http://127.0.0.1:4175/'
result={'layouts':[],'assets':{},'errors':[]}
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390,360]:
  page=b.new_page(viewport={'width':width,'height':900},reduced_motion='reduce')
  page.on('pageerror',lambda e:result['errors'].append(str(e)))
  for course,chapter in [('operations','transport'),('operations','tool'),('operations','reconcile'),('flow','flow'),('flow','stage'),('flow','lab?case=version')]:
   page.goto(BASE+course+'.html#'+chapter,wait_until='networkidle')
   expect(page.locator('.lesson h1')).to_have_count(1)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   for image in page.locator('.art img').all():image.evaluate('(i)=>i.decode()')
   if chapter=='transport' and width<560:
    assert page.locator('table').evaluate('e=>e.scrollWidth<=e.clientWidth+1')
    expect(page.locator('td[data-label="到站後"]').first).to_be_visible()
   if chapter=='reconcile':
    expect(page.locator('.process-banner').first).to_have_text('F012 · 預期槽位')
    expect(page.locator('#sim-state')).to_contain_text('07=W99')
   if chapter.startswith('lab'):
    for target in ['published','newlot','finish']:
     idx=page.evaluate('(target)=>getEngine().node.actions.findIndex(a=>a.next===target)',target)
     page.locator(f'[data-action="{idx}"]').click()
    assert page.evaluate('getEngine().state.current')=='S45'
    route=page.locator('.route-details')
    assert route.evaluate('e=>e.open')==(width>560)
    if width<=560:route.locator('summary').click()
    expect(route.locator('.node.current')).to_contain_text('S45')
    expect(route.locator('.node')).to_have_count(7)
   page.evaluate('document.activeElement.blur();window.scrollTo(0,0)')
   page.screenshot(path=str(OUT/f'final-{course}-{chapter.replace("?case=","-")}-{width}.png'),full_page=True)
   result['layouts'].append([course,chapter,width])
  page.close()
 b.close()
files=['index.html','operations.html','flow.html','course.css','course.js','course-content.js','scenarios.js']+[str(f.relative_to(ROOT)).replace('\\','/') for f in (ROOT/'assets/mes-v2').glob('*.png')]
for name in files:
 local=hashlib.sha256((ROOT/name).read_bytes()).hexdigest();served=hashlib.sha256(urlopen(BASE+name).read()).hexdigest();assert local==served;result['assets'][name]=local
assert not result['errors'];result['status']='PASS'
(OUT/'final-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 18 final layouts, mobile paired table, expected/read distinction, v2 S45, responsive route disclosure, headings and 13 HTTP assets')
