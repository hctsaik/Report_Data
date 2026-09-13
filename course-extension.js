'use strict';
function addAdvancedLinks(){
  const nav=document.querySelector('.course-tabs');
  if(nav&&!nav.querySelector('[data-advanced]')){const a=document.createElement('a');a.href='advanced.html#qtime';a.textContent='時間與配方';a.dataset.advanced='true';nav.append(a);}
  if(nav&&!nav.querySelector('[data-er]')){const a=document.createElement('a');a.href='data-map.html';a.textContent='ER 圖導讀';a.dataset.er='true';nav.append(a);}

}
window.addEventListener('hashchange',()=>setTimeout(addAdvancedLinks,0));addAdvancedLinks();
