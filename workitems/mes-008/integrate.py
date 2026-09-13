from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'freshness.html'
s=p.read_text(encoding='utf-8').replace('<script src="freshness.js" defer></script>','<link rel="stylesheet" href="freshness-v2.css"><script src="freshness-v2.js" defer></script><script src="freshness.js" defer></script>')
p.write_text(s,encoding='utf-8')
p=r/'freshness.js'
s=p.read_text(encoding='utf-8').replace('const freshnessViews={architecture,decision,ai,history,join,contract};','const freshnessViews=freshnessV2;')
s=s.replace("if(id==='join')updateJoin();", "if(id==='join')updateJoin();enhanceFreshLesson(id);")
s=s.replace("function updateHistory(){const complete=freshState.complete==='yes';", "function updateHistory(){const complete=freshState.complete==='yes';const coverage=document.querySelector('#coverage-fill');if(coverage)coverage.style.width=complete?'100%':'50%';")
p.write_text(s,encoding='utf-8')
