from pathlib import Path
R=Path(__file__).resolve().parents[2]
for f in ['er-atlas.html','er-atlas.js']:
 p=R/f;s=p.read_text(encoding='utf-8').replace('fab-er-v1','fab-er-v2').replace('er-model-v1','er-model-v2')
 if f.endswith('.html'):
  s=s.replace('橢圓是屬性註記','橢圓保留概念／屬性註記')
  s=s.replace('<div id="canvas"','<div class="walk-tools"><button id="path-overview">本段全貌</button><button id="step-prev">← 沿線上一點</button><span id="step-label"></span><button id="step-next">沿線下一點 →</button></div><div id="canvas"')
 else:
  s=s.replace("let pinch=null;","let pinch=null;let walkIds=[],walkEdges=[],walkIndex=0;")
  start=s.index('function fitIds(');end=s.index('\nfunction mark',start)
  s=s[:start]+'''function fitIds(ids,allowTiny=false){const bs=ids.map(box),x=Math.min(...bs.map(b=>b.x)),y=Math.min(...bs.map(b=>b.y)),r=Math.max(...bs.map(b=>b.x+b.w)),bt=Math.max(...bs.map(b=>b.y+b.h));const cw=$('canvas').clientWidth,ch=$('canvas').clientHeight;let w=Math.max(r-x+80,cw/1.2),h=Math.max(bt-y+80,ch/1.2);if(w/h<cw/ch)w=h*cw/ch;else h=w*ch/cw;if(!allowTiny&&cw/w<.8){focusStep(Math.min(1,walkIds.length-1));return false;}setView([x+(r-x-w)/2,y+(bt-y-h)/2,w,h]);return true;}
function focusStep(i){if(!walkIds.length)return;walkIndex=Math.max(0,Math.min(walkIds.length-1,i));const id=walkIds[walkIndex],b=box(id),cw=$('canvas').clientWidth,ch=$('canvas').clientHeight;const scale=.9,w=cw/scale,h=ch/scale;setView([b.x+b.w/2-w/2,b.y+b.h/2-h/2,w,h]);$('step-label').textContent=`${walkIndex+1} / ${walkIds.length} · ${nodes.get(id).labels[0]}`;$('status').textContent='沿線閱讀：'+nodes.get(id).labels.join(' / ')+'。保留90%可讀尺寸；超出畫面的相鄰節點可用上一點／下一點定位。';document.querySelectorAll('[data-inspect]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.inspect===id));}
function setupWalk(ids,es){walkIds=ids;walkEdges=es;walkIndex=0;$('step-label').textContent=`${ids.length} 個節點 · 可沿線逐點讀`;}
''' +s[end:]
  start=s.index('function inspect(');end=s.index('\nfunction route',start)
  s=s[:start]+'''function inspect(ids,title,meaning){$('selection-title').textContent=title;$('meaning').textContent=meaning;const actual=edges.filter(e=>ids.includes(e.a)&&ids.includes(e.b));$('path-list').innerHTML=actual.map(e=>`<div class="edge-pair"><button data-inspect="${e.a}">${nodes.get(e.a).labels.map(esc).join('<br>')}</button><span>— 原圖連線 —</span><button data-inspect="${e.b}">${nodes.get(e.b).labels.map(esc).join('<br>')}</button></div>`).join('');$('sources').innerHTML=ids.map(id=>{const n=nodes.get(id);return `<article><strong>${n.labels.map(esc).join(' / ')}</strong>${n.schema_missing?'<p>原圖未列 schema；保留此來源的獨立節點。</p>':''}${n.refs.map(r=>`<p><a href="data-map.html?view=original#${r.source}">來源 ${r.source}</a> · ${esc(r.node)}<br>${r.labels.map(esc).join('<br>')}</p>`).join('')}</article>`}).join('')+(model.sourceNotes||[]).filter(note=>ids.some(id=>nodes.get(id).refs.some(r=>r.source===note.source))).map(note=>`<p>${esc(note.text)}</p>`).join('');document.querySelectorAll('[data-inspect]').forEach(b=>b.onclick=()=>{const i=walkIds.indexOf(b.dataset.inspect);i>=0?focusStep(i):selectNode(b.dataset.inspect)});}
''' +s[end:]
  s=s.replace("mark(ids,edgeIds);fitIds(ids);inspect(ids,r.title,r.meaning);$('status').textContent=r.title+' · '+ids.length+' 個節點／'+edgeIds.length+' 條原始關係';", "mark(ids,edgeIds);setupWalk(ids,edgeIds);inspect(ids,r.title,r.meaning);$('status').textContent=r.title+' · '+ids.length+' 個節點／'+edgeIds.length+' 條原始關係';fitIds(ids);")
  s=s.replace("mark(ids,es.map(e=>e.id));fitIds(ids);inspect", "mark(ids,es.map(e=>e.id));setupWalk(ids,es.map(e=>e.id));inspect")
  s=s.replace("$('status').textContent='已定位：'+n.labels.join(' / ');}","$('status').textContent='已定位：'+n.labels.join(' / ');fitIds(ids);}")
  s=s.replace("全圖：119 個節點、128 條關係都在圖上。", "全圖：121 個節點、128 條關係都在圖上。")
  s=s.replace("getView:()=>view.slice()", "getView:()=>view.slice(),focusStep,getWalk:()=>walkIds.slice()")
  s=s.replace("$('overview').onclick", "$('path-overview').onclick=()=>{fitIds(walkIds,true);$('status').textContent='本段全貌：用來辨識路徑結構；按沿線上一點／下一點回到可讀尺寸。'};$('step-prev').onclick=()=>focusStep(walkIndex-1);$('step-next').onclick=()=>focusStep(walkIndex+1);\n$('overview').onclick")
 p.write_text(s,encoding='utf-8')
p=R/'er-atlas.css';s=p.read_text(encoding='utf-8')+'\n.walk-tools{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:10px 14px;background:#f0f6fc;border-top:1px solid #d4e1ee}.walk-tools span{font-size:13px;color:#3f617f}.edge-pair{padding:8px;margin:10px 0;border:1px solid #d3dfeb;border-radius:8px}.edge-pair span{font-size:12px;color:#60778a;display:block;text-align:center}\n';p.write_text(s,encoding='utf-8')
