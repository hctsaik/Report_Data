from pathlib import Path
import re
p=Path('er-atlas.js');s=p.read_text(encoding='utf-8')
start=s.index('function teachingForNode(');end=s.index('function clearFrames()',start)
s=s[:start]+'''Object.assign(teaching, window.ER_TOPIC_CONTENT.topics);
teaching.source={title:'來源關係說明',color:'#52728e'};
function teachingForNode(id){
 for(const [key,t] of Object.entries(window.ER_TOPIC_CONTENT.topics))if(t.refs.some(ref=>model.mapping[ref]===id))return key;
 for(const key of ['qtime','predispatch','wph','recipe','equipment','carrier','lot','flow'])if(teaching[key].refs.some(ref=>model.mapping[ref]===id))return key;
 const recipeRefs=['2677:recipe-key','2677:recipe-eqp','2673:lr-eqp-link','2673:lr-link','2677:er','2677:lr'];
 if(recipeRefs.some(ref=>model.mapping[ref]===id))return 'recipe';
 return 'source';
}
function showTeaching(key){
 const t=teaching[key]||teaching.source,hasImage=Boolean(t.image);
 $('selection-details').dataset.topic=key;
 document.querySelector('.teaching-figure').hidden=!hasImage;
 $('teaching-mobile').removeAttribute('srcset');$('teaching-image').removeAttribute('src');
 if(hasImage){$('teaching-mobile').srcset=t.mobile||t.image;$('teaching-image').src=t.image;}
 $('teaching-image').alt=t.alt||'';$('teaching-caption').textContent=t.caption||'';
 $('teaching-link').hidden=!t.link;
 if(t.link)$('teaching-link').href=t.link;else $('teaching-link').removeAttribute('href');
 $('teaching-link').textContent=key==='wph'?'機群 WPH 定義（本頁）':key==='predispatch'?'Lot 預派說明（本頁）':'閱讀完整教學 →';
 $('topic-detail').innerHTML=t.details||'';
 if(key!=='overview')$('selection-details').open=true;
 const focus={lot:[68,63,28,16],carrier:[34,19,33,65],equipment:[1,19,33,65]}[key];
 $('teaching-focus').hidden=!focus;
 if(focus){const f=$('teaching-focus');f.style.left=focus[0]+'%';f.style.top=focus[1]+'%';f.style.width=focus[2]+'%';f.style.height=focus[3]+'%';f.style.borderColor=t.color;}
 $('teaching-current').textContent=hasImage?(t.title||'現場物件總覽'):'';
 $('teaching-current').hidden=!hasImage;$('teaching-current').style.borderColor=t.color||'#52728e';
}
function nodeContext(id){
 const n=nodes.get(id),connected=edges.filter(e=>e.a===id||e.b===id).map(e=>nodes.get(e.a===id?e.b:e.a));
 return '<section class="node-context"><h3>這個節點在圖中的角色</h3><p>'+esc(n.labels.join(' / '))+'</p>'+
 (connected.length?'<p>直接相連：</p><ul>'+connected.map(v=>'<li>'+esc(v.labels.join(' / '))+'</li>').join('')+'</ul>':'')+
 '<p>沿上方關聯圖閱讀兩端對象；同名鍵必須留在這條關係的上下文中，不自行推定唯一性或一對多。</p></section>';
}
''' +s[end:]
s=re.sub(r"showTeaching\(\(\{load:.*?\}\)\[id\]\|\|'lot'\)","showTeaching(window.ER_TOPIC_CONTENT.routeKeys[id]||'source')",s)
s=s.replace("r.id==='qtime'?model.mapping['2672:qtime']:","r.id==='hold'?model.mapping['2673:future']:r.id==='qtime'?model.mapping['2672:qtime']:")
start=s.index('function selectNode(');end=s.index('function overview()',start)
s=s[:start]+'''function selectNode(id){
 clearFrames();displayMode='node';document.querySelector('.walk-tools').hidden=false;
 const key=teachingForNode(id),t=teaching[key],n=nodes.get(id);showTeaching(key);
 let es=edges.filter(e=>e.a===id||e.b===id);
 if(n.kind==='rect'){const rel=es.find(e=>nodes.get(e.a===id?e.b:e.a).kind==='diamond')||es[0];if(rel){const other=rel.a===id?rel.b:rel.a;es=edges.filter(e=>e.a===other||e.b===other);}}
 const ids=[...new Set([id,...es.flatMap(e=>[e.a,e.b])])];mark(ids,es.map(e=>e.id));setupWalk(ids,es.map(e=>e.id));
 const meaning=t.meaning||(n.kind==='circle'?'這是「'+n.labels.join('／')+'」的概念／屬性註記，須配合相連資料對象閱讀；原圖未將它定義為獨立資料表。':'這個節點以「'+n.labels.join('／')+'」標示來源中的對象或關係。下面列出它實際相連的節點；具體欄位語意仍須核對來源定義。');
 inspect(ids,key==='wph'?t.title:key==='lotstep'?'Lot Step 歷史':key==='contents'?'FOUP 內容物（Wafer）歷史':n.labels[0],meaning);
 // Source-grounded details supplement the lesson; do not borrow another topic's image.
 if(key==='source')$('topic-detail').innerHTML=nodeContext(id);
 $('status').textContent='已定位：'+n.labels.join(' / ');window.ER_FOCUS.show(id);
 setView(allBox.slice());svg.querySelectorAll('[data-node],[data-edge]').forEach(g=>g.style.opacity='1');
 activeEntity=key;framedIds=[id];drawFrames();
 if(innerWidth<=950&&!$('focus-dialog').open)$('focus-panel').scrollIntoView({block:'start'});
}
''' +s[end:]
s=s.replace("window.ER_ATLAS={model,", "window.ER_ATLAS={teachingForNode,model,")
s=s.replace("if(new URLSearchParams(location.search).get('subject')==='qtime')", "if(new URLSearchParams(location.search).get('subject')==='future')selectNode(model.mapping['2673:future']);if(new URLSearchParams(location.search).get('subject')==='qtime')")
p.write_text(s,encoding='utf-8')
p=Path('er-atlas.html');s=p.read_text(encoding='utf-8').replace('<script defer src="er-atlas.js?v=25">','<script defer src="er-topic-content.js?v=26"></script><script defer src="er-atlas.js?v=26">').replace('er-atlas.css?v=17','er-atlas.css?v=26');p.write_text(s,encoding='utf-8')
p=Path('er-atlas.css');p.write_text(p.read_text(encoding='utf-8')+'\n/* Topic-specific prose remains readable in the expanded and mobile inspectors. */\n.teaching-figure[hidden],#teaching-current[hidden],#teaching-link[hidden]{display:none!important}\n.topic-reading{padding-left:1.6em;line-height:1.85}.topic-reading li{padding:0.4em 0}.topic-takeaway{background:#fff4cc;border-left:4px solid #e7b437;padding:1em;line-height:1.75}.node-context{overflow-wrap:anywhere}\n',encoding='utf-8')
