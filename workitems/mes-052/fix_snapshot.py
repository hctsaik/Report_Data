from pathlib import Path
p=Path('er-atlas.js');s=p.read_text(encoding='utf-8')
s=s.replace('這張歷史 WIP 標明星期一07:20的快照。歷史 Lot_ID 關係不能讓這份快照變成現在的狀態。','KER_WIP_Y_BTH 每天早上07:20保存機群狀況與KPI快照；固定時點的版本不是目前即時狀況。')
needle='model=m;window.ER_FOCUS.init'
insert="const dailySnapshot=m.nodes.find(n=>n.id===m.mapping['2675:wip-history']);if(dailySnapshot){dailySnapshot.labels=dailySnapshot.labels.map(t=>t.includes('星期一')?'每天07:20機群與KPI快照':t);dailySnapshot.refs=dailySnapshot.refs.map(r=>({...r,labels:r.labels.map(t=>t.includes('星期一')?'每天07:20機群與KPI快照':t)}));}"
assert needle in s;s=s.replace(needle,insert+needle)
needle="$('canvas').replaceChildren(svg);"
insert="const dailyGlyph=svg.getElementById(m.mapping['2675:wip-history']);if(dailyGlyph){dailyGlyph.querySelectorAll('text').forEach(t=>{if(t.textContent.includes('星期一'))t.textContent='每天07:20機群與KPI快照';});dailyGlyph.setAttribute('aria-label','每天07:20機群與KPI快照 KER_WIP_Y_BTH');}"
assert needle in s;s=s.replace(needle,insert+needle);p.write_text(s,encoding='utf-8')
p=Path('er-atlas.html');s=p.read_text(encoding='utf-8');import re
s=re.sub(r'er-atlas.js\?v=\d+','er-atlas.js?v=52',s);p.write_text(s,encoding='utf-8')
