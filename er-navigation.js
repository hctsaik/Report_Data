/* Navigation between ER views, distinct from relationship pagination. */
window.createErNavigation = api => {
 let ready=false,restoring=false,depth=0,entries=[],index=0,current={kind:'overview'};
 const bar=document.createElement('nav');bar.className='er-navigation';bar.setAttribute('aria-label','ER 閱讀位置與返回');
 const back=document.createElement('button'),home=document.createElement('button'),trail=document.createElement('div');
 back.id='er-back';home.id='er-home';home.textContent='回到 ER 全圖';trail.id='er-trail';
 bar.append(back,home,trail);document.getElementById('focus-panel').before(bar);
 const largeBack=document.createElement('button');largeBack.type='button';largeBack.id='er-large-back';document.getElementById('focus-dialog').querySelector('form').after(largeBack);
 function snapshot(){return {...current,...api.snapshot(),label:document.getElementById('selection-title').textContent};}
 function state(){return {entries,index};}
 function save(){entries[index]=snapshot();history.replaceState({...history.state,mesErNav:state()},'');}
 function urlFor(v){const u=new URL(location.href);for(const k of ['subject','erNode','erRoute','erEntity','erResume'])u.searchParams.delete(k);if(v.kind==='node')u.searchParams.set('erNode',v.arg);if(v.kind==='route')u.searchParams.set('erRoute',v.arg);if(v.kind==='entity')u.searchParams.set('erEntity',v.arg);return u;}
 function paint(){back.disabled=index===0;back.textContent=index?'← 返回：'+entries[index-1].label:'← 返回上一個檢視';largeBack.disabled=back.disabled;largeBack.textContent=back.textContent;trail.replaceChildren();
  const label=document.createElement('span');label.textContent='瀏覽路徑：';trail.append(label);
  entries.slice(Math.max(0,index-3),index+1).forEach((e,j)=>{const i=Math.max(0,index-3)+j,b=document.createElement('button');b.textContent=e.label||'ER 全圖';if(i===index){b.disabled=true;b.setAttribute('aria-current','location');}else b.onclick=()=>{save();history.go(i-index);};trail.append(b);});
 }
 function restore(v){restoring=true;const focusDialog=document.getElementById('focus-dialog'),wasOpen=focusDialog.open;current={kind:v.kind,arg:v.arg};api.restore(v);if(wasOpen&&!focusDialog.open&&v.kind!=='overview'){focusDialog.showModal();window.ER_FOCUS.refresh();}restoring=false;paint();}
 back.onclick=()=>{if(index){save();history.back();}};home.onclick=()=>api.home();
 largeBack.onclick=()=>back.onclick();
 window.addEventListener('popstate',e=>{const s=e.state?.mesErNav;if(!s)return;entries=s.entries;index=s.index;restore(entries[index]);});
 window.addEventListener('pagehide',()=>{if(ready)save();});
 document.addEventListener('click',e=>{const a=e.target.closest('a[href]');if(!ready||!a||a.download)return;const u=new URL(a.href,location.href);
  if(u.origin!==location.origin||!/(?:index|operations|flow|advanced|support|data-map|freshness)\.html$/.test(u.pathname))return;
  save();const token=Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,8);
  try{sessionStorage.setItem('mes-er-return:'+token,JSON.stringify({url:urlFor(current).href,label:entries[index].label,navigation:state()}));u.searchParams.set('erReturn',token);a.href=u.href;}catch{/* In-page navigation remains usable when storage is unavailable. */}
 },true);
 return {
  perform(kind,arg,fn){if(restoring||depth)return fn();if(ready)save();const same=current.kind===kind&&current.arg===arg;let result;depth++;try{result=fn();}finally{depth--;}current={kind,arg};
   if(ready){if(!same){entries=entries.slice(0,index+1);entries.push(snapshot());index++;history.pushState({mesErNav:state()},'',urlFor(current));}else save();paint();}return result;},
  ready(){ready=true;let saved=history.state?.mesErNav;const u=new URL(location.href),token=u.searchParams.get('erResume');
   if(token){try{saved=JSON.parse(sessionStorage.getItem('mes-er-return:'+token))?.navigation;}catch{}}
   if(saved?.entries?.length){entries=saved.entries;index=saved.index;if(token){const target=index;for(index=0;index<=target;index++){const method=index?'pushState':'replaceState';history[method]({mesErNav:{entries:entries.slice(0,index+1),index}},'',urlFor(entries[index]));}index=target;}restore(entries[index]);history.replaceState({mesErNav:state()},'',urlFor(current));}
   else {const id=u.searchParams.get('erNode'),route=u.searchParams.get('erRoute'),entity=u.searchParams.get('erEntity');restoring=true;if(id&&api.validNode(id)){current={kind:'node',arg:id};api.restore(current);}else if(route&&api.validRoute(route)){current={kind:'route',arg:route};api.restore(current);}else if(entity&&api.validEntity(entity)){current={kind:'entity',arg:entity};api.restore(current);}restoring=false;entries=[snapshot()];index=0;history.replaceState({mesErNav:state()},'',urlFor(current));paint();}
  }
 };
};
