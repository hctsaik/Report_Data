"""One-time user terminology correction; archived source files remain unchanged."""
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'er-atlas.js';s=p.read_text(encoding='utf-8')
s=s.replace("title:'Lot 預到哪台設備？'", "title:'Lot 在這個站點有哪些可用機台？'")
s=s.replace('這裡起點是 Lot，關係表是 FRLOT_EQP；FOUP 預派則使用另一個關係表。批次安排與載具安排各自保留。','「帶到／FRLOT_EQP」表示 Lot 在這個站點有可用機台。它描述站點可用機台的關係，不表示預計到達、已到達或已開始加工；FOUP 預派是另一條關係。')
s=s.replace("model=m;window.ER_FOCUS.init", """const available=m.nodes.find(n=>n.id===m.mapping['2671:lot-eqp']);
if(available){available.labels=available.labels.map(t=>t==='預到'?'帶到':t);available.refs=available.refs.map(r=>({...r,labels:r.labels.map(t=>t==='預到'?'帶到':t)}));}
model=m;window.ER_FOCUS.init""")
s=s.replace("svg=document.importNode(parsed.documentElement,true);", """svg=document.importNode(parsed.documentElement,true);const availableGlyph=svg.getElementById(m.mapping['2671:lot-eqp']);if(availableGlyph){availableGlyph.querySelectorAll('text').forEach(t=>{if(t.textContent==='預到')t.textContent='帶到';});availableGlyph.setAttribute('aria-label','帶到：Lot 在這個站點的可用機台');}
""")
s=s.replace("$('status').textContent='已定位：'+n.labels.join(' / ');", "if(id===model.mapping['2671:lot-eqp'])$('meaning').textContent='「帶到／Siview.Frlot_EQP」表示 Lot 在這個站點有可用機台，不是預計到達；這條關係本身不表示已到機台或已開始加工。';$('status').textContent='已定位：'+n.labels.join(' / ');")
p.write_text(s,encoding='utf-8')
p=r/'er-focus.js';s=p.read_text(encoding='utf-8').replace("const more=$('focus-more');", "if(branches.some(b=>b.ids.includes(model.mapping['2671:lot-eqp'])))$('focus-note').append(' 「帶到」表示 Lot 在這個站點有可用機台，不是預計到達。');const more=$('focus-more');");p.write_text(s,encoding='utf-8')
p=r/'er-atlas.html';s=p.read_text(encoding='utf-8').replace('er-atlas.js?v=19','er-atlas.js?v=21').replace('er-focus.js?v=20','er-focus.js?v=21');p.write_text(s,encoding='utf-8')
# Other authored explanations must not retain the rejected interpretation.
p=r/'integrated-map.js';s=p.read_text(encoding='utf-8').replace('CSFRPREDISPATCH、Frlot_EQP 是預派／預到線索。','CSFRPREDISPATCH 是 FOUP 預派線索；Frlot_EQP 的「帶到」表示 Lot 在該站點有可用機台。');p.write_text(s,encoding='utf-8')
p=r/'subject-er.html';s=p.read_text(encoding='utf-8').replace('Lot 預到的設備與 FOUP 所在設備，可能是不同設備 ID。','「帶到」表示 Lot 在該站點有可用機台；這與 FOUP 所在位置是不同關係。');p.write_text(s,encoding='utf-8')
