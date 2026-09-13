from pathlib import Path
p=Path('er-atlas.js');s=p.read_text(encoding='utf-8')
hook='''let navigation;
function installNavigation(){
 const original={node:selectNode,route,entity:frameEntity,overview};
 navigation=window.createErNavigation({
  snapshot:()=>({view:view?.slice(),focusPage:window.ER_FOCUS.getState().page,walkIndex,scrollY:window.scrollY,detailsOpen:$('selection-details').open,dialogScroll:$('inspector-dialog').scrollTop}),
  restore:v=>{const fn=original[v.kind]||original.overview;fn(v.arg);if(v.focusPage!==undefined)window.ER_FOCUS.setPage(v.focusPage);if(v.walkIndex!==undefined&&walkIds.length)focusStep(v.walkIndex);if(v.view)setView(v.view);if(v.detailsOpen!==undefined)$('selection-details').open=v.detailsOpen;requestAnimationFrame(()=>{window.scrollTo(0,v.scrollY||0);$('inspector-dialog').scrollTop=v.dialogScroll||0;});},
  home:()=>overview(),validNode:id=>nodes.has(id),validRoute:id=>routes.some(r=>r.id===id),validEntity:key=>['lot','carrier','equipment','flow','recipe'].includes(key)
 });
 selectNode=id=>navigation.perform('node',id,()=>original.node(id));
 route=id=>navigation.perform('route',id,()=>original.route(id));
 frameEntity=key=>navigation.perform('entity',key,()=>original.entity(key));
 overview=()=>navigation.perform('overview',undefined,()=>original.overview());
}
installNavigation();
'''
s=s.replace('start().catch(e=>',hook+'start().then(()=>navigation.ready()).catch(e=>');p.write_text(s,encoding='utf-8')
p=Path('er-focus.js');s=p.read_text(encoding='utf-8').replace('refresh:paint,','refresh:paint,\n    setPage(value){page=Math.max(0,Number(value)||0);paint();},').replace('目前第 ${page+1} / ${pages} 頁','目前第 ${page+1} / ${pages} 組關係').replace('b.textContent=`關係 ${p*pageSize()+1}', 'b.textContent=`第 ${p+1} 組：關係 ${p*pageSize()+1}');p.write_text(s,encoding='utf-8')
p=Path('er-atlas.html');s=p.read_text(encoding='utf-8').replace('<script defer src="er-atlas.js?v=26">','<script defer src="er-navigation.js?v=28"></script><script defer src="er-atlas.js?v=28">').replace('er-focus.js?v=27','er-focus.js?v=28').replace('er-atlas.css?v=26','er-atlas.css?v=28').replace('aria-label="關閉關聯圖">關閉 ×','aria-label="關閉關聯圖">關閉，回圖與說明 ×');p.write_text(s,encoding='utf-8')
p=Path('er-atlas.css');p.write_text(p.read_text(encoding='utf-8')+'\n.er-navigation{position:sticky;top:0;z-index:5;background:#fff;padding:12px 0;border-bottom:1px solid #c4d6e8;margin-bottom:16px;display:flex;flex-wrap:wrap;gap:8px}.er-navigation button{white-space:normal;text-align:left;max-width:100%;min-height:42px}#er-trail{flex-basis:100%;font-size:13px;display:flex;flex-wrap:wrap;gap:6px;align-items:center}#er-trail button{font-size:13px;padding:5px 8px}#er-large-back{margin:10px;max-width:95%}\n',encoding='utf-8')
