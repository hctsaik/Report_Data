from pathlib import Path
p=Path('er-atlas.js');s=p.read_text(encoding='utf-8')
s=s.replace("let pinch=null;", "let focusedSubject=null;\nlet pinch=null;")
needle='function focusStep(i)'
start=s.index(needle)
s=s[:start]+'''// Keep the complete SVG, but move its viewport to the current subject.
function focusSubject(id){
 focusedSubject=id;fitIds([id],true);
 $('focus-current').disabled=false;
 $('map-subject').textContent='目前主詞：'+nodes.get(id).labels.join(' / ');
}
'''+s[start:]
s=s.replace("setView(allBox.slice());svg.querySelectorAll('[data-node],[data-edge]').forEach(g=>g.style.opacity='1');\n activeEntity=key;framedIds=[id];drawFrames();", "focusSubject(id);svg.querySelectorAll('[data-node],[data-edge]').forEach(g=>g.style.opacity='1');\n activeEntity=key;framedIds=[id];drawFrames();")
s=s.replace("if(innerWidth<=950&&!$('focus-dialog').open)$('focus-panel').scrollIntoView({block:'start'});", "if(!$('focus-dialog').open&&!$('inspector-dialog').open)$('map-subject').scrollIntoView({block:'start',behavior:'instant'});")
s=s.replace("function overview(){window.ER_FOCUS.clear();", "function overview(){focusedSubject=null;$('focus-current').disabled=true;$('map-subject').textContent='Table 總表 · 選擇主詞後自動放大';window.ER_FOCUS.clear();")
s=s.replace("右側會重新展開", "下方會重新展開")
s=s.replace("document.querySelector(`[data-entity=\"${key}\"]`).setAttribute('aria-pressed','true');", "document.querySelector(`[data-entity=\"${key}\"]`).setAttribute('aria-pressed','true');focusSubject(window.ER_FOCUS.getState().root);")
s=s.replace("fitIds(ids);document.querySelectorAll('[data-route]')", "focusSubject(window.ER_FOCUS.getState().root);document.querySelectorAll('[data-route]')")
s=s.replace("$('overview').onclick=()=>overview();", "$('overview').onclick=()=>{setView(allBox.slice());$('status').textContent='完整 ER 總覽；下方保留目前介紹。按「回目前主詞」恢復放大。'};$('focus-current').onclick=()=>{if(focusedSubject)focusSubject(focusedSubject)};")
s=s.replace("if(svg&&['overview','entity'].includes(displayMode))setView(allBox.slice())", "if(svg){if(focusedSubject)focusSubject(focusedSubject);else setView(allBox.slice())}")
p.write_text(s,encoding='utf-8')
p=Path('er-atlas.html');s=p.read_text(encoding='utf-8')
for old,new in [('er-atlas.css?v=28','er-atlas.css?v=56'),('er-focus.css?v=20','er-focus.css?v=56'),('er-atlas.js?v=54','er-atlas.js?v=56'),('inspector-expand.js?v=20','inspector-expand.js?v=56'),('左圖標示所在位置；右圖重新排列主詞、關係與相關實體。','上方總圖放大到目前主詞；下方閱讀關聯圖與教學說明。'),('展開右側','放大介紹')]:s=s.replace(old,new)
s=s.replace('<div class="map-side"><div class="toolbar">','<div class="map-side"><h2 id="map-subject">Table 總表 · 選擇主詞後自動放大</h2><div class="toolbar">')
s=s.replace('<button id="overview">全圖總覽</button>','<button id="overview">全圖總覽</button><button id="focus-current" disabled>回目前主詞</button><a href="#inspector">↓ 閱讀本主詞介紹</a>')
s=s.replace('<strong>圖與說明</strong>','<strong>主詞關聯與教學說明</strong><a href="#map-subject">↑ 回上方總圖</a>')
s=s.replace('<details id="selection-details">','<details id="selection-details" open>')
p.write_text(s,encoding='utf-8')
p=Path('inspector-expand.js');s=p.read_text(encoding='utf-8').replace('收回右側 ↙','收回介紹 ↙').replace('展開右側 ↗','放大介紹 ↗');p.write_text(s,encoding='utf-8')
