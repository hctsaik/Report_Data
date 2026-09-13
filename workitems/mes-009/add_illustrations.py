from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'advanced.js'
t=p.read_text(encoding='utf-8')
marker="const take=t=>"
helper="""const conceptArt=(key,caption)=>`<details class="concept-illustration" ${innerWidth>760?'open':''}><summary>情境插畫 · ${caption}</summary><figure class="variant-art"><img src="assets/mes-009/${key}.png" alt="${caption}，教學示意" data-zoom="assets/mes-009/${key}.png"><figcaption><span>下方用同一案例操作與核對條件。</span><button class="btn" data-zoom="assets/mes-009/${key}.png">放大完整圖</button></figcaption></figure></details>`;
"""
if 'const conceptArt=' not in t:
    t=t.replace(marker,helper+marker)
    t=t.replace("它約束的是一段事件間隔，不是整個 Lot 的製造時間。')+","它約束的是一段事件間隔，不是整個 Lot 的製造時間。')+conceptArt('qtime','起點、等待與截止事件')+")
    t=t.replace("到指定事件才建立有效的 Hold。')+","到指定事件才建立有效的 Hold。')+conceptArt('future','登記、途中與到站攔截')+")
    t=t.replace("相同路徑也可能被多個產品共用。')+","相同路徑也可能被多個產品共用。')+conceptArt('part','產品、路徑與兩批 Lot')+")
    t=t.replace("查到名稱後，還要核對它屬於哪一層。')+","查到名稱後，還要核對它屬於哪一層。')+conceptArt('recipes','從邏輯要求到實際執行')+")
    t=t.replace('<div class="wafer coated"></div><strong id="q-end">','<div class="wafer" id="q-end-wafer"></div><strong id="q-end">')
    t=t.replace("document.querySelector('#q-end').textContent=", "document.querySelector('#q-end-wafer').className='wafer'+(state.stop==='out'?' coated':'');document.querySelector('#q-end').textContent=")
    p.write_text(t,encoding='utf-8')
