"""Freeze reviewed output, without inventing quality scores."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((root/'tests/evidence/mes-007/render-check.json').read_text(encoding='utf-8'))
s=json.loads((root/'tests/evidence/mes-007/drills/render-check.json').read_text(encoding='utf-8'))
for data in [r,s]:
 for name,digest in data['assets'].items():assert sha(root/name)==digest,('source changed',name)
evidence={}
def collect(obj):
 if isinstance(obj,dict):
  if 'path' in obj and 'sha256' in obj:
   assert sha(root/obj['path'])==obj['sha256'];evidence[obj['path']]=obj['sha256']
  for val in obj.values():collect(val)
 elif isinstance(obj,list):
  for val in obj:collect(val)
collect(r);collect(s)
for name in ['render-check.json','drills/render-check.json','state-tests.json','regression/browser-tests.json']:
 path='tests/evidence/mes-007/'+name;evidence[path]=sha(root/path)
docs=['workitems/mes-007/REVIEW.md','workitems/mes-007/PLAN.md','workitems/mes-007/BRIEFS.md','workitems/mes-007/source-freshness.txt','workitems/mes-007/prompts.json','workitems/mes-007/revision-prompts.json']
m={'version':'MES-007','user_acceptance':'pending','review':'workitems/mes-007/REVIEW.md','assets':r['assets'],'evidence':evidence,'documents':{name:sha(root/name) for name in docs},'validation':{'layouts':42,'interactions':92,'expanded_pages':30,'state_snapshots':132,'frames':26,'exercise_choices':60,'state_engine':{'scenarios':16,'states':66,'edges':85},'earlier_full_ui_regression':{'layouts':54,'journeys':32,'note':'Full UI regression before final illustration/mobile/text refinements; final render and exhaustive state evidence above supersede its screenshots.'}}}
(root/'workitems/mes-007/evidence-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
print('Evidence manifest frozen:',len(evidence),'evidence files;',len(r['assets']),'assets')
