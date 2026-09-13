from pathlib import Path
p=Path(__file__).resolve().parents[2]/'advanced.js'
t=p.read_text(encoding='utf-8')
t=t.replace('<div class="arrow">←','<div class="arrow reverse">←')
start="const VARIANTS="
fn="""const compactLot=(n,lot)=>`<div class="compact-lot"><h3>${lot} · 目前 ${STEPS[n][0]}</h3><div class="compact-progress">${STEPS.map(([id],i)=>`<span class="${i<n?'done':i===n?'current':''}">${id}</span>`).join('')}</div><p>綠色已完成 · 藍色目前 · 灰色未到</p></div>`;
"""
if 'const compactLot=' not in t:t=t.replace(start,fn+start)
t=t.replace('<h3>Lot L023 · 目前 S50</h3>${track(4,\'L023\')}<h3>Lot L024 · 目前 S20</h3>${track(1,\'L024\')}',"${compactLot(4,'Lot L023')}${compactLot(1,'Lot L024')}")
p.write_text(t,encoding='utf-8')
