from pathlib import Path
p=Path('er-atlas.js');s=p.read_text(encoding='utf-8')
s=s.replace('let focusedSubject=null;','let focusedSubject=null,walkFocused=false;')
s=s.replace('function focusStep(i){', '''function syncWalkSubject(id){
 const key=teachingForNode(id),t=teaching[key];showTeaching(key);
 inspect(walkIds,t.title||nodes.get(id).labels[0],t.meaning||nodes.get(id).labels.join(' / '));
 window.ER_FOCUS.show(id);focusedSubject=id;activeEntity=key;framedIds=[id];drawFrames();
 $('map-subject').textContent='目前主詞：'+nodes.get(id).labels.join(' / ');
 $('focus-current').disabled=false;
 if(key==='source')$('topic-detail').innerHTML=nodeContext(id);
}
function focusStep(i){''')
s=s.replace("const scale=.9,w=cw/scale", "walkFocused=true;syncWalkSubject(id);const scale=.9,w=cw/scale")
s=s.replace('function setupWalk(ids,es){','function setupWalk(ids,es){walkFocused=false;')
s=s.replace('focusPage:window.ER_FOCUS.getState().page,walkIndex,','focusPage:window.ER_FOCUS.getState().page,walkIndex,walkFocused,')
s=s.replace('if(v.focusPage!==undefined)window.ER_FOCUS.setPage(v.focusPage);if(v.walkIndex!==undefined&&walkIds.length)focusStep(v.walkIndex);','if(v.walkFocused&&v.walkIndex!==undefined&&walkIds.length)focusStep(v.walkIndex);if(v.focusPage!==undefined)window.ER_FOCUS.setPage(v.focusPage);')
p.write_text(s,encoding='utf-8')
