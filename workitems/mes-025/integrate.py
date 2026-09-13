"""One-time Qtime Lot context and teaching integration."""
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'er-focus.js';s=p.read_text(encoding='utf-8')
s=s.replace('walk([id],[]);',"""walk([id],[]);
    if([model.mapping['2672:qtime'],model.mapping['2672:qtime-link']].includes(id)){
      const refs=id===model.mapping['2672:qtime']?['2672:qtime','2672:qtime-link','2672:step','2672:summary','2671:lot']:['2672:qtime-link','2672:step','2672:summary','2671:lot'];
      const ids=refs.map(ref=>model.mapping[ref]);
      const es=ids.slice(1).map((v,i)=>model.edges.find(e=>(e.a===ids[i]&&e.b===v)||(e.b===ids[i]&&e.a===v)));
      if(es.every(Boolean)){const i=out.findIndex(b=>b.ids[1]===ids[1]);if(i>=0)out.splice(i,1);out.unshift({ids,edges:es});}
    }
""")
s=s.replace("if(id===model.mapping['2672:step'])return", "if([model.mapping['2672:step'],model.mapping['2672:qtime'],model.mapping['2672:qtime-link']].includes(id))return")
s=s.replace("const more=$('focus-more');", "if([model.mapping['2672:qtime'],model.mapping['2672:qtime-link']].includes(root))$('focus-note').append(' 這是同一 Lot 的 Qtime 與站點歷史關聯；保留 Lot、Lot_id 及 Lot_ID／Ope_no 的來源路徑。');const more=$('focus-more');")
p.write_text(s,encoding='utf-8')
p=r/'er-atlas.js';s=p.read_text(encoding='utf-8')
s=s.replace('const teaching={',"""const teaching={
qtime:{title:'QTime：Lot 的製程時間限制',refs:['2672:qtime','2672:qtime-link'],color:'#7756af',image:'assets/mes-009/qtime.png',mobile:'assets/mes-025/qtime-mobile-v1.png',alt:'同一Lot的QTime教學示例：10:00起算、最大30分鐘，10:20已用20分鐘，10:30為本例最晚進站時間',caption:'教學示例：Lot L023 在10:00清洗出站起算，最大時限30分鐘，指定下一站進站為停止事件。本例10:30是截止時間，不是已發生的進站紀錄；實際事件與限值依製程規則。',meaning:'QTime 是同一 Lot 在指定起算事件與停止事件之間的時間限制，用來管控製程間隔。起訖可能是某站出站到指定站進站，也可能跨站或以出站停止；不能一律當成排隊時間，也不是整個 Lot 的總製造時間。',details:'<h3>怎麼讀 Qtime 歷史？</h3><p>先確認是哪個 Lot、哪個站點，再核對起算事件、停止事件、時間與允許間隔。依規則比較已用時間與限值，不能只看到歷史表就判定現在是否超時。</p><h3>同一 Lot 的教學示例</h3><p>假設最大時限 30 分鐘，10:00 起算：10:20 已用 20 分鐘，尚餘 10 分鐘；若指定停止事件在 10:35 才發生，已用 35 分鐘，超過本例限值 5 分鐘。</p><p>若停止事件是「出站」，只有「進站」還不算結束計時。Hold 不會自動重設；超時依廠內規則處理，不自行改時間。</p>',link:'advanced.html#qtime'},""")
s=s.replace('function teachingForNode(id){',"function teachingForNode(id){\n if(teaching.qtime.refs.some(ref=>model.mapping[ref]===id))return 'qtime';")
s=s.replace("if(['wph','predispatch'].includes(key))", "$('topic-detail').innerHTML=t.details||'';if(['wph','predispatch','qtime'].includes(key))")
s=s.replace("qtime:'flow'", "qtime:'qtime'")
s=s.replace("title:'Step 與 Qtime 歷史',refs:['2672:step','2672:qtime-link','2672:qtime'],meaning:'原圖透過 Lot_ID／Ope_no 從 Step 歷史連到 Qtime 歷史。起訖事件、限值與超時處置仍需按實際規則判讀。'", "title:'這個 Lot 的 Qtime 與站點歷史',refs:['2671:lot','2672:summary','2672:step','2672:qtime-link','2672:qtime'],meaning:'QTime 是同一 Lot 指定起訖事件之間的時間限制。原圖由 Lot 經站點 Summary／Lot_id、Step 歷史，再經 Lot_ID／Ope_no 接到 Qtime 歷史；判讀時要核對同一 Lot 的事件、時間與限值。'")
s=s.replace("r.id==='predispatch'?model.mapping['2671:predispatch']:ids[0]", "r.id==='qtime'?model.mapping['2672:qtime']:r.id==='predispatch'?model.mapping['2671:predispatch']:ids[0]")
s=s.replace("if(new URLSearchParams(location.search).get('subject')==='lot-step')", "if(new URLSearchParams(location.search).get('subject')==='qtime')selectNode(model.mapping['2672:qtime']);if(new URLSearchParams(location.search).get('subject')==='lot-step')")
p.write_text(s,encoding='utf-8')
p=r/'er-atlas.html';s=p.read_text(encoding='utf-8').replace('<div id="meaning"></div>','<div id="meaning"></div><div id="topic-detail"></div>').replace('er-atlas.js?v=24','er-atlas.js?v=25').replace('er-focus.js?v=24','er-focus.js?v=25');p.write_text(s,encoding='utf-8')
