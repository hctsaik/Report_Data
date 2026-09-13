"""Create the MES-008 evidence snapshot after visual review and validation."""
from pathlib import Path
from urllib.request import urlopen
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
W=ROOT/'workitems/mes-008'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def entry(paths): return {p.relative_to(ROOT).as_posix():sha(p) for p in paths}
review=json.loads((W/'review.json').read_text(encoding='utf-8'))
browser=json.loads((ROOT/'tests/evidence/mes-008/browser-tests.json').read_text(encoding='utf-8'))
assert len(browser['pages'])==18 and len(browser['interactions'])==190 and not browser['errors']
active=[ROOT/x['asset'] for x in review['images']]
active.extend(ROOT/f for f in ['freshness.html','freshness.js','freshness-v2.js','freshness-v2.css','course.css'])
for p in active:
    data=urlopen('http://127.0.0.1:4175/'+p.relative_to(ROOT).as_posix()).read()
    assert hashlib.sha256(data).hexdigest()==sha(p),p
style={}
for row in review['images']:
    p=ROOT/row['asset']
    with Image.open(p) as im:
        assert im.width>=800 and im.height>=800,(p,im.size)
        rgb=im.convert('RGB')
        # Sample existing pixels for analysis; do not alter or save the image.
        points=[rgb.getpixel((x,y)) for y in range(0,im.height,10) for x in range(0,im.width,10)]
        bright=sum(min(c)>224 for c in points)/len(points)
        bottom=[rgb.getpixel((x,y)) for y in range(int(im.height*.78),im.height,8) for x in range(0,im.width,8)]
        yellow=sum(a>225 and b>180 and c<224 and a>c+20 for a,b,c in bottom)/len(bottom)
        assert bright>.18,(p,'bright canvas',bright)
        assert yellow>.08,(p,'yellow footer',yellow)
        style[row['asset']]={'size':list(im.size),'bright_pixel_fraction':round(bright,3),'bottom_yellow_fraction':round(yellow,3),'meaning':'pixel style checks only; not a teaching score'}
evidence=sorted((ROOT/'tests/evidence/mes-008').glob('*'))
old_previews=[p for p in evidence if p.name.startswith(('preview-','precheck-'))]
current=[p for p in evidence if p not in old_previews and p.is_file()]
old=json.loads((W/'baseline/evidence-manifest.json').read_text(encoding='utf-8'))
unchanged={p:h for p,h in old['assets'].items() if not p.startswith('freshness')}
for p,h in unchanged.items(): assert sha(ROOT/p)==h,p
docs=[ROOT/f for f in ['AGENTS.md','README.md','WORKITEMS.md','CLAUDE.md','IMAGE_STYLE_GUIDE.md','TEACHING_WEBPAGE_GUIDE.md','TEACHING_SCORING_RUBRIC.md','TEACHING_REVIEW_LOG.md','openspec/changes/data-freshness/spec.md','workitems/mes-007/source-freshness.txt','workitems/mes-007/REVIEW.md','tests/check_freshness_v2.py','tools/verify_mes008_evidence.py']]
docs.extend(p for p in W.glob('*') if p.is_file() and p.name!='evidence-manifest.json')
for id in ['architecture','decision','ai','history','join','contract']:
    assert (ROOT/f'tests/evidence/mes-007/freshness-{id}-1440.png').exists()
assert urlopen('http://127.0.0.1:4175/workitems/mes-008/review.html').read()==(W/'review.html').read_bytes()
manifest={'version':'MES-008','user_acceptance':'pending','learner_study':'none','active_assets':entry(active),'evidence':entry(current),'documents':entry(set(docs)),'historical_previews':entry(old_previews),'unchanged_other_courses':unchanged,'image_style_measurements':style,'validation':{'layouts':18,'behavior_checks':190,'js_errors':0,'visual_status':'author reviewed; see REVIEW.md; user acceptance not inferred'}}
(W/'evidence-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Frozen {len(active)} active files, {len(current)} evidence files, 12 image measurements; other-course hashes unchanged: {len(unchanged)}.')
