from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':390,'height':1000},has_touch=True)
 page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
 page.locator('[data-entity="carrier"]').tap();page.locator('#overview').click()
 nid=page.evaluate('ER_ATLAS.model.mapping["2671:cast"]');node=page.locator(f'#canvas [data-node="{nid}"]');node.scroll_into_view_if_needed();page.wait_for_timeout(300);r=node.bounding_box();x=r['x']+r['width']/2;y=r['y']+r['height']/2
 print(r,page.evaluate('([x,y])=>({hit:document.elementFromPoint(x,y).outerHTML,scroll:scrollY,canvas:document.querySelector("#canvas").getBoundingClientRect().toJSON()})',[x,y]),flush=True)
 page.evaluate('''window.logs=[];for(const type of ['pointerdown','pointerup','click'])document.addEventListener(type,e=>logs.push([type,e.detail,e.clientX,e.clientY,e.target.closest('[data-node]')?.id,e.target.closest('[data-focus-node]')?.dataset.focusNode,scrollY,startNode]),true);const orig=window.ER_FOCUS.show;window.ER_FOCUS.show=id=>{logs.push(['show',id,new Error().stack]);return orig(id)};''')
 page.touchscreen.tap(x,y);print(page.evaluate('logs'),flush=True);print(page.evaluate('ER_FOCUS.getState().root'),flush=True)
 page.locator('#canvas').screenshot(path='tests/evidence/mes-017/debug-canvas.png');b.close()
