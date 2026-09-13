from pathlib import Path
import json,subprocess,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2];O=R/'ER/SUBJECTS';m=json.loads((R/'ER/INTEGRATED/er-model-v2.json').read_text(encoding='utf-8'))
nodes={n['id']:n for n in m['nodes']};edges={e['id']:e for e in m['edges']};q=lambda s:json.dumps(s,ensure_ascii=False)
NS={'s':'http://www.w3.org/2000/svg'};ET.register_namespace('',NS['s'])
def render(t,v,key):
 lines=['graph ER {','graph [rankdir=LR, nodesep=.4, ranksep=.65, splines=polyline, outputorder=edgesfirst, pad=.3, bgcolor="white"];','node [fontname="Microsoft JhengHei",fontsize=18,margin=".16,.12"];','edge [color="#70869a",penwidth=1.8];']
 for nid in v['nodes']:
  n=nodes[nid];color,fill,*_=m['palette'][n['category']];shape={'rect':'box','diamond':'diamond','circle':'ellipse'}[n['kind']]
  label=('本圖主詞\n' if nid==t['subject'] else '')+'\n'.join(n['labels'])
  lines.append(f'{q(nid)} [id={q(nid)},label={q(label)},shape={shape},color={q(color)},fillcolor={q(fill)},style=filled,penwidth={4 if nid==t["subject"] else 2}];')
 # Orient for layout only; edges remain undirected and are identified by original ID.
 dist={t['subject']:0}
 for _ in v['nodes']:
  for eid in v['edges']:
   e=edges[eid]
   for a,b in [(e['a'],e['b']),(e['b'],e['a'])]:
    if a in dist:dist[b]=min(dist.get(b,999),dist[a]+1)
 for eid in v['edges']:
  e=edges[eid];a,b=e['a'],e['b']
  if dist.get(a,999)>dist.get(b,999):a,b=b,a
  lines.append(f'{q(a)} -- {q(b)} [id={q(eid)}];')
 lines.append('}');name=t['key']+'-'+key
 (O/(name+'.dot')).write_text('\n'.join(lines),encoding='utf-8')
 exe=next((R/'tools/vendor/graphviz').rglob('dot.exe'))
 subprocess.run([str(exe),'-Tsvg',str(O/(name+'.dot')),'-o',str(O/(name+'.svg'))],check=True,capture_output=True)
 tree=ET.parse(O/(name+'.svg'));svg=tree.getroot();svg.set('role','img');svg.set('aria-label',t['title']+' ER 主題圖')
 for g in svg.findall('.//s:g',NS):
  nid=g.get('id')
  if nid in nodes:g.set('data-node',nid);g.set('role','button');g.set('tabindex','0');g.set('aria-label',' / '.join(nodes[nid]['labels']))
  elif nid in edges:g.set('data-edge',nid)
 tree.write(O/(name+'.svg'),encoding='utf-8',xml_declaration=True)
 return name
if __name__=='__main__':
 data=json.loads((O/'subjects.json').read_text(encoding='utf-8'))
 topics=data if isinstance(data,list) else data['subjects']
 for t in topics:
  print(render(t,t['core'],'core'))
  for v in t['branches']:print(render(t,v,v['key']))
