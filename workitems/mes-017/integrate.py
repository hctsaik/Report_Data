"""One-time MES-017 integration; do not rerun over later changes."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[2]
base=root/'workitems/mes-017/baseline';base.mkdir(exist_ok=True)
for name in ['er-atlas.html','er-atlas.js','er-atlas.css']:
    shutil.copy2(root/name,base/name)
p=root/'er-atlas.html';s=p.read_text(encoding='utf-8')
s=s.replace('er-atlas.css?v=6','er-atlas.css?v=17').replace('<script defer src="er-atlas.js?v=6"></script>','<link rel="stylesheet" href="er-focus.css?v=17"><script defer src="er-focus.js?v=17"></script><script defer src="er-atlas.js?v=17"></script>')
s=s.replace('先看全圖，再找物件','選主詞，展開關聯 ER').replace('框選主要資料位置，保留所有連線；需要讀表名時，再放大。','左圖標示所在位置；右圖重新排列主詞、關係與相關實體。')
s=s.replace('<aside id="inspector"><p class="eyebrow">沿線讀圖</p>','''<aside id="inspector"><section id="focus-panel" aria-label="主詞關聯 ER"><p class="eyebrow">SUBJECT · RELATED ENTITIES</p><div class="focus-heading"><h2 id="focus-title">選一個主詞，展開關聯</h2><button id="focus-expand" disabled>放大關聯圖 ↗</button></div><p id="focus-note" role="status"></p><div id="focus-graph"></div><div id="focus-more"></div><p class="focus-takeaway">連線表示來源資料關係，不代表加工順序或已發生事件。</p></section><details id="selection-details"><summary>主詞說明與現場參考</summary>''')
s=s.replace('<div id="entity-targets"></div><h3>這一段關係</h3>','<div id="entity-targets"></div></details><h3>這一段關係</h3>')
s=s.replace('</main><dialog id="teaching-dialog">','</main><dialog id="focus-dialog"><form method="dialog"><button aria-label="關閉關聯圖">關閉 ×</button></form><div id="focus-large"></div></dialog><dialog id="teaching-dialog">')
p.write_text(s,encoding='utf-8')
p=root/'er-atlas.js';s=p.read_text(encoding='utf-8')
s=s.replace("inspect(framedIds,t.title,t.meaning);","inspect(framedIds,t.title,t.meaning);window.ER_FOCUS.show(model.mapping[key==='recipe'?'2677:recipe':t.refs[0]]);")
s=s.replace("inspect(ids,r.title,r.meaning);","inspect(ids,r.title,r.meaning);window.ER_FOCUS.show(ids[0]);")
s=s.replace("$('status').textContent='已定位：'+n.labels.join(' / ');fitIds(ids);","$('status').textContent='已定位：'+n.labels.join(' / ');window.ER_FOCUS.show(id);setView(allBox.slice());svg.querySelectorAll('[data-node],[data-edge]').forEach(g=>g.style.opacity='1');const subjectKey=teachingForNode(id);activeEntity=subjectKey==='overview'?'lot':subjectKey;framedIds=[id];drawFrames();")
s=s.replace("function overview(){clearFrames();","function overview(){window.ER_FOCUS.clear();clearFrames();")
s=s.replace("'完整 ER × 現場物件','先用左側大圖認識資料之間的關係，再按上方物件按鈕。彩色框指出資料位置；教學插圖說明它在現場代表什麼。'","'完整 ER × 主詞關聯','選擇上方主詞或直接點 ER 節點，右側會重新展開來源中的相關實體與關係。現場插圖保留為補充參考。'")
s=s.replace("model=m;nodes=new Map", "model=m;window.ER_FOCUS.init(m,{selectNode});nodes=new Map")
p.write_text(s,encoding='utf-8')
