"""Read-only MES-008 scope/hash/arithmetic checks; does not grade visual quality."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'workitems/mes-008/evidence-manifest.json').read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for group in ['active_assets','evidence','documents','historical_previews','unchanged_other_courses']:
    for filename,expected in manifest[group].items():
        path=ROOT/filename
        assert path.is_file(),filename
        assert sha(path)==expected,(group,filename,'changed since capture')
report=json.loads((ROOT/'tests/evidence/mes-008/browser-tests.json').read_text(encoding='utf-8'))
review=json.loads((ROOT/'workitems/mes-008/review.json').read_text(encoding='utf-8'))
assert len(report['pages'])==18
assert {(p['id'],p['width']) for p in report['pages']}=={(id,width) for id in ['architecture','decision','ai','history','join','contract'] for width in [1440,800,360]}
assert len(report['interactions'])==190
assert not report['errors']
assert len(review['images'])==12 and len(review['pages'])==6
for kind,limits in [('images',[25,25,20,20,10]),('pages',[20,20,20,20,10,10])]:
    for row in review[kind]:
        assert len(row['scores'])==len(limits)
        assert all(0<=v<=maxv for v,maxv in zip(row['scores'],limits))
        assert sum(row['scores'])==row['total'],row['id']
        assert row['evidence'] and row['deduction']
        if kind=='images':
            assert row['asset'] in manifest['active_assets']
            assert row['screenshot'] in manifest['evidence']
            assert len(row['completion'])==5 and all(0<=x<=10 for x in row['completion'])
        else:
            assert row['desktop'] in manifest['evidence'] and row['mobile'] in manifest['evidence']
assert manifest['user_acceptance']==review['user_acceptance']=='pending'
assert len(manifest['image_style_measurements'])==12
assert 'architecture-mobile-v3.png' in (ROOT/'freshness-v2.js').read_text(encoding='utf-8')
assert 'decision-mobile-v2.png' in (ROOT/'freshness-v2.js').read_text(encoding='utf-8')
print(f"PASS: 6 lessons / 12 images / 18 layouts / 190 behavior checks; {len(manifest['unchanged_other_courses'])} other-course assets unchanged. Hashes and arithmetic consistent; no automated visual approval.")
