"""Fail closed on missing/stale page review evidence. Never assigns quality scores."""
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REQUIRED={f'{course}/{id}' for course,ids in {
    'operations':['port','recipe','chamber','state','handoff','lab'],
    'flow':['stage','step','lot-flow','execution','branching','rework','split-merge','versions','lab']}.items() for id in ids}
ASSETS={'operations.html','flow.html','course-content.js','course-remake.js','course.js','scenarios.js','course.css','course-remake.css'}
CASES={'operations':{'arrival','reconcile','recipe','run','fault','hold'},'flow':{'bind','normal','branch','rework','split','version','qtime','skip','revisit','dispatch'}}
def validate(review,render):
    errors=[]
    rows=review.get('pages',[])
    ids=[r.get('id') for r in rows]
    if set(ids)!=REQUIRED or len(ids)!=15: errors.append('exact scope must contain the 15 user-requested URLs once each')
    if review.get('rubric')!='v1.0-fab-mapping-MES004': errors.append('missing frozen rubric mapping')
    if set(render.get('assets',{}))!=ASSETS: errors.append('missing render source coverage')
    for asset,digest in render.get('assets',{}).items():
        path=ROOT/asset
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest: errors.append('stale asset: '+asset)
    for r in rows:
        rid=r.get('id','?')
        for width in [1440,360]:
            matches=[x for x in render.get('pages',[]) if x['id']==rid and x['width']==width]
            if len(matches)!=1: errors.append(f'{rid}: missing unique {width}px evidence');continue
            for kind in ['page','scene']:
                e=matches[0]['evidence'][kind];p=ROOT/e['path']
                if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=e['sha256']: errors.append(f'{rid}: stale {kind} evidence')
                reviewpart=r.get(str(width),{}).get(kind,{})
                weights=[20,20,20,20,10,10] if kind=='page' else [25,25,20,20,10]
                scores=reviewpart.get('scores',[])
                if len(scores)!=len(weights) or any(type(s) not in (int,float) or not 0<=s<=w for s,w in zip(scores,weights)):
                    errors.append(f'{rid} {width} {kind}: invalid scores')
                elif sum(scores)<=90: errors.append(f'{rid} {width} {kind}: not above 90')
                evidence=reviewpart.get('evidence',[])
                if len(evidence)!=len(weights) or any(not isinstance(x,str) or len(x)<12 for x in evidence): errors.append(f'{rid}: missing item evidence')
                if not reviewpart.get('deductions') or not reviewpart.get('strengths'): errors.append(f'{rid}: missing strengths/deductions')
                if reviewpart.get('vetoes') or reviewpart.get('open_defects'): errors.append(f'{rid}: unresolved defects')
                if reviewpart.get('reviewed_hash')!=e['sha256']: errors.append(f'{rid}: review does not reference this screenshot')
                if kind=='scene':
                    completion=reviewpart.get('completion',[])
                    if len(completion)!=5 or any(not isinstance(x,dict) or x.get('score',0)<8 or not x.get('reason') for x in completion): errors.append(f'{rid}: incomplete visual quality review')
                    expected={x['path'] for x in render.get('frames',[]) if x['id']==rid and x['width']==width}
                    extra=reviewpart.get('additional_frames',[])
                    if {x.get('path') for x in extra}!=expected: errors.append(f'{rid}: missing interactive frame review')
                    for frame in extra:
                        p=ROOT/frame['path']
                        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=frame.get('sha256'): errors.append(f'{rid}: stale interactive frame evidence')
    for course,required_cases in CASES.items():
        for width in [1440,360]:
            states=[r for r in render.get('states',[]) if r['course']==course and r['width']==width]
            if {r['case'] for r in states}!=required_cases: errors.append(f'{course} {width}: scenario coverage incomplete')
            expected_count=25 if course=='operations' else 41
            # Node counts are frozen to the current 16-scenario engine; a new engine needs a scope update.
            if len(states)!=expected_count or len({(r['case'],r['node']) for r in states})!=len(states): errors.append(f'{course} {width}: node coverage incomplete')
            for state in states:
                p=ROOT/state['path']
                if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=state['sha256']: errors.append('stale scenario evidence: '+state['path'])
    if review.get('user_acceptance')!='pending': errors.append('self-review must not assert user acceptance')
    return errors

if __name__=='__main__':
    try:
        review=json.loads((ROOT/'workitems/mes-004/review.json').read_text(encoding='utf-8'))
        render=json.loads((ROOT/'tests/evidence/mes-004/render-check.json').read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError) as e:
        print('INCOMPLETE: '+str(e));sys.exit(1)
    errors=validate(review,render)
    if errors: print('\n'.join(errors));sys.exit(1)
    print('PASS: 15 pages, separate desktop/mobile scene and page reviews; evidence current. User acceptance pending.')
