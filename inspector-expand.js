// Expand the actual inspector so its current subject, controls and explanations stay live.
(() => {
  const panel=document.getElementById('inspector');
  const button=document.getElementById('inspector-expand');
  const dialog=document.getElementById('inspector-dialog');
  const anchor=document.createComment('inspector home');
  panel.before(anchor);
  let previousScroll=0,detailsWereOpen=false;
  button.addEventListener('click',()=>{
    if(dialog.open){dialog.close();return;}
    previousScroll=window.scrollY;
    detailsWereOpen=document.getElementById('selection-details').open;
    document.getElementById('selection-details').open=true;
    dialog.append(panel);
    button.textContent='收回介紹 ↙';
    button.setAttribute('aria-expanded','true');
    dialog.showModal();
    dialog.scrollTop=0;
    window.ER_FOCUS.refresh();
  });
  dialog.addEventListener('close',()=>{
    anchor.after(panel);
    document.getElementById('selection-details').open=detailsWereOpen;
    button.textContent='放大介紹 ↗';
    button.setAttribute('aria-expanded','false');
    window.ER_FOCUS.refresh();
    window.scrollTo(0,previousScroll);
    button.focus({preventScroll:true});
  });
})();
