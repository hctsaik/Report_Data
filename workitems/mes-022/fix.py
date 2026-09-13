"""One-time application of the user's FOUP contents history definition."""
from pathlib import Path
r=Path(__file__).resolve().parents[2]
meaning='Siview.fhwlths 記錄 FOUP 內容物（Wafer）的歷史：在什麼時間點，這個 FOUP 放了哪些 Wafer。每次 Split／Merge 進 FOUP 時更新。查詢時要對應時間，不能直接把歷史內容當成目前裝載狀態。'
p=r/'er-atlas.js';s=p.read_text(encoding='utf-8')
s=s.replace("title:'Slot 與裝載關係'", "title:'FOUP 在某個時間點放了哪些 Wafer？'")
s=s.replace('「在 Slot／fhwlths」與「放在／FRCAST_LOT」是原圖中分開的兩條關係。不能因為都描述裝載就把資料對象合併。',meaning)
s=s.replace('model=m;window.ER_FOCUS.init',"const contents=m.nodes.find(n=>n.id===m.mapping['2671:slot']);if(contents){contents.labels=contents.labels.map(t=>t==='在 Slot'?'內容物歷史':t);contents.refs=contents.refs.map(r=>({...r,labels:r.labels.map(t=>t==='在 Slot'?'內容物歷史':t)}));}model=m;window.ER_FOCUS.init")
s=s.replace("svg=document.importNode(parsed.documentElement,true);", "svg=document.importNode(parsed.documentElement,true);const historyGlyph=svg.getElementById(m.mapping['2671:slot']);if(historyGlyph){historyGlyph.querySelectorAll('text').forEach(t=>{if(t.textContent==='在 Slot')t.textContent='內容物歷史';});historyGlyph.setAttribute('aria-label','FOUP內容物歷史：各時間點的Wafer，Split／Merge進FOUP時更新');}")
s=s.replace("$('status').textContent='已定位：'+n.labels.join(' / ');", "if(id===model.mapping['2671:slot']){$('selection-title').textContent='FOUP 內容物（Wafer）歷史';$('meaning').textContent='"+meaning+"';$('teaching-caption').textContent='此插圖僅說明 FOUP、Wafer 與 Slot 的實物關係，不是內容物歷史紀錄或 Split／Merge 事件示例。';$('selection-details').open=true;}$('status').textContent='已定位：'+n.labels.join(' / ');")
p.write_text(s,encoding='utf-8')
p=r/'er-focus.js';s=p.read_text(encoding='utf-8').replace('來源未列 Wafer entity，本圖不補造其連線。','原 ER 未獨立畫出 Wafer 實體；FOUP 內容物歷史仍記錄 Wafer。')
s=s.replace("const more=$('focus-more');", "if(root===model.mapping['2671:slot']||branches.some(b=>b.ids.includes(model.mapping['2671:slot'])))$('focus-note').append(' 內容物歷史：記錄各時間點 FOUP 裡的 Wafer，每次 Split／Merge 進 FOUP 時更新。');const more=$('focus-more');")
p.write_text(s,encoding='utf-8')
p=r/'data-map.js';s=p.read_text(encoding='utf-8').replace("['晶圓槽位','Siview.fhwlths','原圖另列「在 Slot」；追單片位置時，還需核對晶圓與槽位及其有效時間。']", "['FOUP 內容物歷史','Siview.fhwlths','記錄在各時間點 FOUP 放了哪些 Wafer；每次 Split／Merge 進 FOUP 時更新，查詢時須對應時間。']");p.write_text(s,encoding='utf-8')
# Maintain the additional subject views without changing the archived seven source diagrams.
for p in (r/'ER/SUBJECTS').glob('*'):
 if p.suffix not in ['.svg','.dot','.json']:continue
 s=p.read_text(encoding='utf-8')
 if '在 Slot' in s:p.write_text(s.replace('在 Slot','內容物歷史'),encoding='utf-8')
p=r/'subject-er.js';s=p.read_text(encoding='utf-8').replace('model=m;topics=data.subjects;',"const contents=m.nodes.find(n=>n.id===m.mapping['2671:slot']);if(contents){contents.labels=contents.labels.map(t=>t==='在 Slot'?'內容物歷史':t);}model=m;topics=data.subjects;");p.write_text(s,encoding='utf-8')
p=r/'er-atlas.html';s=p.read_text(encoding='utf-8').replace('er-atlas.js?v=21','er-atlas.js?v=22').replace('er-focus.js?v=21','er-focus.js?v=22');p.write_text(s,encoding='utf-8')
