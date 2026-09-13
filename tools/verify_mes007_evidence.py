"""Read-only evidence consistency check. This does not grade teaching quality."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
 m=json.loads((ROOT/'workitems/mes-007/evidence-manifest.json').read_text(encoding='utf-8'))
 for group in ['assets','evidence','documents']:
  for path,digest in m[group].items():
   assert sha(ROOT/path)==digest,('stale evidence',path)
 r=json.loads((ROOT/'tests/evidence/mes-007/render-check.json').read_text(encoding='utf-8'))
 assert len(r['pages'])==42 and len({x['id'] for x in r['pages']})==21
 assert not r['errors'] and len(r['interactions'])==92
 assert len([p for p in r['assets'] if p.endswith('.png')])==29
 assert len([p for p in r['pages'] if p['id'].startswith('freshness/') and 'art' in p])==10
 for path,digest in r['assets'].items():assert sha(ROOT/path)==digest,path
 s=json.loads((ROOT/'tests/evidence/mes-007/drills/render-check.json').read_text(encoding='utf-8'))
 assert len(s['states'])==132 and len(s['pages'])==30 and not s['errors']
 assert {x['width'] for x in s['states']}=={1440,360}
 review=(ROOT/'workitems/mes-007/REVIEW.md').read_text(encoding='utf-8')
 rows=re.findall(r'\| ([^|\n]+) \| ((?:\d+/){4,5}\d+) = (\d+) \|',review)
 assert len(rows)==55,('expected 15 desktop + 14 portrait + 5 data figures + 21 pages',len(rows))
 for name,parts,total in rows:
  assert sum(map(int,parts.split('/')))==int(total),('score arithmetic',name)
 assert m['user_acceptance']=='pending'
 print('PASS: 21 URLs, 29 generated assets, 5 data figures, 132 state snapshots; hashes and review arithmetic consistent. Not user acceptance.')
if __name__=='__main__':verify()
