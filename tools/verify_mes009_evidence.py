"""Read-only provenance and arithmetic checks; no automatic quality grading."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
W=ROOT/'workitems/mes-009'
m=json.loads((W/'evidence-manifest.json').read_text(encoding='utf-8'))
for group in ['active','documents','evidence','baseline','rejected_drafts','unchanged_from_mes008']:
    for name,expected in m[group].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,(group,name)
r=json.loads((W/'review.json').read_text(encoding='utf-8'))
assert len(r['pages'])==5 and len(r['images'])==7 and len(r['native_figures'])==4
for group in ['pages','images','native_figures']:
    for row in r[group]:
        assert row['total']==sum(row['scores'])
        assert len(row['evidence'])==len(row['scores'])
        assert not row['veto']
        if 'visual_scores' in row:assert min(row['visual_scores'])>=8
assert r['user_acceptance']=='pending'
print('PASS: MES-009 evidence hashes and review arithmetic; user acceptance remains pending.')
