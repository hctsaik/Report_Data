from pathlib import Path
import json,re,hashlib,subprocess,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2];O=R/'ER/INTEGRATED';O.mkdir(exist_ok=True)
NS='http://www.w3.org/2000/svg';ns={'s':NS};ET.register_namespace('',NS)
source=json.loads((R/'ER/NEW/transcription.json').read_text(encoding='utf-8'))
qualified=re.compile(r'^(?:SIVIEW|F12DM)\.[A-Z_][A-Z_0-9]*$',re.I)
bare=re.compile(r'^(?:FR[A-Z_0-9]+|MFG_EQP_BAY_BT|F12DM[A-Z_0-9]*|KER_[A-Z_0-9]+|DM_FLOW_LR_EQP_BT)$',re.I)
nodes={};mapping={};original_nodes=[];edges={}
palette={'lot':('#176ac2','#eef5ff','Lot 批次'),'carrier':('#008775','#edf9f5','FOUP 載具'),'equipment':('#b26018','#fff6eb','設備／Tool／EQP'),'flow':('#7756af','#f7f1ff','流程／配方'),'record':('#61748b','#f5f7fa','紀錄／統計'),'relation':('#6a7d8e','#ffffff','關係／鍵')}
def classify(labels,kind):
 if kind!='rect':return 'relation'
 text=' '.join(labels).upper()
 if any(s in text for s in ['HOLD','FORECAST','STREAM']):return 'record'
 if any(s in text for s in ['FRLOT_MTRLCONTNRS','FRCAST']):return 'carrier'
 if any(s.upper() in ['SIVIEW.FRLOT','FRLOT'] for s in labels):return 'lot'
 if any(s in text for s in ['FREQP','FRPORT','SIVIEW.PORT','FRPRCRSC','CSFRPRCRSC','CSFROHB','CSFREQP_STK']):return 'equipment'
 if any(s in text for s in ['FRPD','FRMRCP','FLOW','FRPRODSPEC','RECIPE','STAGE','SRTS','CTWPH']):return 'flow'
 return 'record'
for d in source:
 tree=ET.parse(R/f'ER/NEW/{d["name"]}.svg')
 for g in tree.findall("s:g[@id='nodes']/s:g",ns):
  labels=[''.join(t.itertext()).strip() for t in g.findall('s:text',ns)];kind=g.get('data-kind');ref=f'{d["name"]}:{g.get("id")}'
  tables=[s for s in labels if qualified.fullmatch(s) or bare.fullmatch(s)]
  # Contextual keys and all relationship diamonds remain separate.
  identity=tables[0].upper() if kind=='rect' and len(tables)==1 else None
  key='t_'+hashlib.sha1(identity.encode()).hexdigest()[:12] if identity and qualified.fullmatch(identity) else 'n_'+ref.replace(':','_')
  if key not in nodes:nodes[key]=dict(id=key,kind=kind,identity=identity,labels=[],refs=[],category=classify(labels,kind),schema_missing=bool(identity and '.' not in identity))
  n=nodes[key]
  for label in labels:
   if label.casefold() not in [x.casefold() for x in n['labels']]:n['labels'].append(label)
  n['refs'].append(dict(source=d['name'],node=g.get('id'),labels=labels));mapping[ref]=key
  original_nodes.append(dict(ref=ref,canonical=key,kind=kind,labels=labels))
for d in source:
 for i,e in enumerate(d['edges']):
  a=mapping[f'{d["name"]}:{e["a"]}'];b=mapping[f'{d["name"]}:{e["b"]}'];key='e_'+'_'.join(sorted([a,b]))
  if key not in edges:edges[key]=dict(id=key,a=a,b=b,refs=[])
  edges[key]['refs'].append(dict(source=d['name'],index=i,a=e['a'],b=e['b']))
def q(s):return json.dumps(s,ensure_ascii=False)
def emit(selected,name):
 dot=['graph ER {','graph [layout=dot, nodesep=0.5, ranksep=0.65, splines=true, outputorder=edgesfirst, bgcolor="#ffffff", pad="0.6", fontname="Microsoft JhengHei"];','node [fontname="Microsoft JhengHei",fontsize=20,margin="0.24,0.18",penwidth=2.5];','edge [color="#7c8c9c",penwidth=1.7];']
 for n in nodes.values():
  if n['id'] not in selected:continue
  color,fill,_=palette[n['category']];shape={'rect':'box','diamond':'diamond','circle':'ellipse'}[n['kind']]
  labels=n['labels'][:]
  if n['schema_missing']:labels.append('（未列 schema）')
  display=[]
  for line in labels:
   if len(line)>23 and re.fullmatch(r'[A-Za-z0-9_.@]+',line):
    parts=line.split('.')
    if len(parts)>1 and len(parts[0])<9:display.extend([parts[0]+'.','.'.join(parts[1:])])
    else:
     cut=line.rfind('_',0,22)+1
     display.extend([line[:cut],line[cut:]]) if cut>0 else display.append(line)
   else:display.append(line)
  label='\n'.join(display)
  dot.append(f'{q(n["id"])} [id={q(n["id"])},label={q(label)},shape={shape},style="filled",fillcolor={q(fill)},color={q(color)}];')
 for e in edges.values():
  if e['a'] in selected and e['b'] in selected:dot.append(f'{q(e["a"])} -- {q(e["b"])} [id={q(e["id"])}];')
 dot.append('}');(O/f'{name}.dot').write_text('\n'.join(dot),encoding='utf-8')
 exe=next((R/'tools/vendor/graphviz').rglob('neato.exe'))
 p=subprocess.run([str(exe),'-Tsvg',str(O/f'{name}.dot'),'-o',str(O/f'{name}.svg')],capture_output=True,text=True,encoding='utf-8');assert p.returncode==0,p.stderr
 tree=ET.parse(O/f'{name}.svg');svg=tree.getroot();svg.set('role','img');svg.set('aria-label','Fab 整合 ER 圖：實體、關係與鍵')
 for g in svg.findall('.//s:g',ns):
  nid=g.get('id')
  if nid in nodes:
   n=nodes[nid];g.set('data-node',nid);g.set('data-category',n['category']);g.set('tabindex','0');g.set('role','button');g.set('aria-label',' / '.join(n['labels']));g.set('style','cursor:pointer')
  elif nid in edges:g.set('data-edge',nid);g.set('data-a',edges[nid]['a']);g.set('data-b',edges[nid]['b'])
 tree.write(O/f'{name}.svg',encoding='utf-8',xml_declaration=True)
 return svg.get('viewBox')
proto={mapping[f'2671:{n}'] for n in ['lot','cast','port','eqp','cast-link','slot','port-link','has','location','predispatch','lot-eqp']}
emit(proto,'er-prototype-v2')
box=emit(set(nodes),'fab-er-v2')
model=dict(nodes=list(nodes.values()),edges=list(edges.values()),originalNodes=original_nodes,mapping=mapping,viewBox=box,palette=palette,sourceNotes=[dict(source=d['name'],text=n[2]) for d in source for n in d.get('notes',[])],sourceCount=7,sourceNodeCount=len(original_nodes),sourceEdgeCount=sum(len(e['refs']) for e in edges.values()))
(O/'er-model-v2.json').write_text(json.dumps(model,ensure_ascii=False,indent=2),encoding='utf-8')
print('canonical',len(nodes),'nodes',len(edges),'edges; source',len(original_nodes),sum(len(e['refs']) for e in edges.values()),'viewBox',box)
