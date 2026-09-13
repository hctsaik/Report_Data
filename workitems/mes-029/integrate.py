from pathlib import Path
import shutil
assets=Path('assets/mes-029');assets.mkdir(parents=True,exist_ok=True)
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
for src,dst in [('exec-20a6974a-e943-4f2a-b395-b2132eeb7c1b.png','pd-definition-v2.png'),('exec-dcc27f7a-e340-4c9c-83b0-daeb852ea151.png','pd-definition-mobile-v1.png')]:shutil.copy2(base/src,assets/dst)
p=Path('er-atlas.js');s=p.read_text(encoding='utf-8')
s=s.replace("title:'PD 與設備對照'", "title:'PD（Process Definition）與設備對照'")
# All displayed FRPD nodes keep their original table labels and source references.
s=s.replace('model=m;window.ER_FOCUS.init', "for(const ref of ['2673:pd','2677:pd']){const n=m.nodes.find(n=>n.id===m.mapping[ref]);if(n)n.labels=n.labels[0]==='FRPD'?['PD（Process Definition）',...n.labels]:['PD（Process Definition）',...n.labels.slice(1)];}model=m;window.ER_FOCUS.init")
s=s.replace("if(new URLSearchParams(location.search).get('subject')==='future')", "if(new URLSearchParams(location.search).get('subject')==='pd')selectNode(model.mapping['2673:pd']);if(new URLSearchParams(location.search).get('subject')==='future')")
# Route meaning should teach the confirmed definition as well as the source path.
s=s.replace('inspect(ids,r.title,r.meaning);window.ER_FOCUS.show', "inspect(ids,r.title,r.id==='pd'?teaching.pd.meaning:r.meaning);window.ER_FOCUS.show")
p.write_text(s,encoding='utf-8')
p=Path('er-atlas.html');s=p.read_text(encoding='utf-8').replace('er-topic-content.js?v=26','er-topic-content.js?v=29').replace('er-atlas.js?v=28','er-atlas.js?v=29');p.write_text(s,encoding='utf-8')
