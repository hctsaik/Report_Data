'use strict';
function addDataMapLink(){const nav=document.querySelector('.course-tabs');if(nav&&!nav.querySelector('[data-er]')){const a=document.createElement('a');a.href='data-map.html#2675';a.textContent='ER 圖導讀';a.dataset.er='true';nav.append(a);}}
addDataMapLink();window.addEventListener('hashchange',()=>setTimeout(addDataMapLink,0));
