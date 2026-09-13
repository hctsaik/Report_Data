"""Visual review caught a rework-only history claim leaking into the revisit scenario."""
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'course-remake.js'
s=p.read_text(encoding='utf-8')
s=s.replace("s.current==='R10'?['S50','R10']", "s.current==='R10'?['R10','S50']")
s=s.replace("${s.current==='R10'?'<div class=\"migration-arrow\">R10 完成後返回 S50；原 S50 Fail 保留。</div>':''}",
            "${s.current==='R10'?`<div class=\"migration-arrow\">R10 完成後返回 S50。${s.visits?.includes('S50 #1 = Fail')?'原 S50 Fail 保留。':'S10 舊 Pass 不能取代 R10 本次證據。'}</div>`:''}")
p.write_text(s,encoding='utf-8')
