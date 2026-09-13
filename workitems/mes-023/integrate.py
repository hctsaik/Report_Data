"""One-time Lot predispatch business relation and reference illustration integration."""
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'er-focus.js';s=p.read_text(encoding='utf-8')
s=s.replace('init(m,options){model=m;',"init(m,options){model={...m,edges:[...m.edges,{id:'business-lot-predispatch',a:m.mapping['2671:lot'],b:m.mapping['2671:predispatch'],provenance:'user-confirmed-business',refs:[]}]};")
s=s.replace('return out.sort((a,b)=>rank(a)-rank(b));',"if(id===model.mapping['2671:predispatch']){const order=[model.mapping['2671:lot'],model.mapping['2671:eqp'],model.mapping['2671:cast']];return out.sort((a,b)=>order.indexOf(a.ids.at(-1))-order.indexOf(b.ids.at(-1)));}return out.sort((a,b)=>rank(a)-rank(b));")
s=s.replace("'stroke-width':1.8,'data-focus-edge':e.id", "'stroke-width':e.provenance?2.8:1.8,'stroke-dasharray':e.provenance?'8 5':'none','data-edge-provenance':e.provenance||'source','data-focus-edge':e.id")
s=s.replace("function nodeSpec(id,w){const n=nodes.get(id),diamond=n.kind==='diamond';", "function nodeSpec(id,w){let n=nodes.get(id);if(root===model.mapping['2671:predispatch']&&id===model.mapping['2671:cast'])n={...n,labels:['FOUP（輔助關聯）',...n.labels.slice(1)]};const diamond=n.kind==='diamond';")
s=s.replace("const more=$('focus-more');", "if(root===model.mapping['2671:predispatch']||branches.some(b=>b.edges.some(e=>e.provenance)))$('focus-note').append(' 預派以 Lot 為主，由派工系統預先安排目標機台；FOUP 是輔助關聯。虛線為已確認的業務關係，不表示資料表 Join 鍵。');const more=$('focus-more');")
s=s.replace('edges:b.edges.map(e=>e.id)',"edges:b.edges.map(e=>e.id),businessEdges:b.edges.filter(e=>e.provenance).map(e=>e.id)")
p.write_text(s,encoding='utf-8')
p=r/'er-atlas.js';s=p.read_text(encoding='utf-8')
s=s.replace('const teaching={',"""const teaching={
predispatch:{title:'Lot 預派：派工系統預先安排目標機台',refs:['2671:predispatch'],color:'#b26018',image:'assets/mes-023/lot-predispatch-v1.png',mobile:'assets/mes-023/lot-predispatch-mobile-v1.png',alt:'Lot 生產批次交由派工系統預先安排目標機台，預派不表示已到站或已加工',caption:'主要對象是 Lot：派工系統預先安排這一批將被派到的機台。FOUP 是輔助關聯；圖為概念示意，不是實際派工結果或搬送紀錄。',meaning:'「預派機台／SIVIEW.CSFRPREDISPATCH」表示派工系統預先安排這個 Lot 將被派到的目標機台。Lot 是主要對象，FOUP 是輔助關聯。這和「帶到／FRLOT_EQP」表示本站可用機台不同，也不表示已到機台或已開始加工。',link:'#selection-details'},""")
s=s.replace('function teachingForNode(id){',"function teachingForNode(id){\n if(model.mapping['2671:predispatch']===id)return 'predispatch';")
s=s.replace("if(key==='wph')$('selection-details').open=true;", "if(['wph','predispatch'].includes(key))$('selection-details').open=true;if(key==='predispatch')$('teaching-link').textContent='Lot 預派說明（本頁）';")
s=s.replace("title:'FOUP 預派到哪台設備？',refs:['2671:cast','2671:predispatch','2671:eqp'],meaning:'預派描述安排，與「位於」是兩條不同關係。即使端點都是 FOUP 與設備，也不能把兩條線合併。'", "title:'派工系統預先把 Lot 派到哪台機台？',refs:['2671:lot','2671:cast-link','2671:cast','2671:predispatch','2671:eqp'],meaning:'預派以 Lot 為主要對象，派工系統預先安排目標機台；FOUP 是輔助關聯。左側保留原資料的裝載及設備路徑，右側虛線補充 Lot 的已確認業務關係；預派不表示已到站或已加工。'")
s=s.replace("predispatch:'equipment'", "predispatch:'predispatch'")
s=s.replace('FOUP 預派是另一條關係。','派工系統對 Lot 的預派是另一條關係。')
s=s.replace('先分清批次與載具，再比較同一 FOUP 到設備的「預派」與「位於」兩條關係。','先看 Lot 被預派到哪台機台，再查載具實際位置；批次預派與載具位置是不同關係。')
s=s.replace('window.ER_FOCUS.show(ids[0]);',"window.ER_FOCUS.show(r.id==='predispatch'?model.mapping['2671:predispatch']:ids[0]);")
s=s.replace("if(new URLSearchParams(location.search).get('subject')==='wph')selectNode(model.mapping['2673:wph']);", "if(new URLSearchParams(location.search).get('subject')==='wph')selectNode(model.mapping['2673:wph']);if(new URLSearchParams(location.search).get('subject')==='predispatch')selectNode(model.mapping['2671:predispatch']);")
p.write_text(s,encoding='utf-8')
p=r/'er-atlas.html';s=p.read_text(encoding='utf-8').replace('er-atlas.js?v=22','er-atlas.js?v=23').replace('er-focus.js?v=22','er-focus.js?v=23');p.write_text(s,encoding='utf-8')
