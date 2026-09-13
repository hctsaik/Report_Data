'use strict';
function addAdvancedLinks(){
  const nav=document.querySelector('.course-tabs');
  if(nav&&!nav.querySelector('[data-advanced]')){const a=document.createElement('a');a.href='advanced.html#qtime';a.textContent='時間與配方';a.dataset.advanced='true';nav.append(a);}
  const main=document.querySelector('main');
  if(main&&!main.querySelector('[data-advanced-note]')){const p=document.createElement('p');p.dataset.advancedNote='true';p.className='decision';const a=document.createElement('a');a.href=location.pathname.endsWith('flow.html')?'advanced.html#flow-versions':'advanced.html#recipes';a.textContent=location.pathname.endsWith('flow.html')?'新增：比較 Stage／Step／Flow 的另外三種教法 →':'新增：LR、ER 與 Physical Recipe 的分層說明 →';p.append(a);const lead=main.querySelector('.lead');if(lead)lead.after(p);else main.append(p);}
}
window.addEventListener('hashchange',()=>setTimeout(addAdvancedLinks,0));addAdvancedLinks();
