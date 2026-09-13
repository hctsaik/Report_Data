"""One-time inspector integration."""
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'er-atlas.html';s=p.read_text(encoding='utf-8')
s=s.replace('er-focus.css?v=17','er-focus.css?v=20').replace('er-focus.js?v=19','er-focus.js?v=20')
s=s.replace('</head>','<script defer src="inspector-expand.js?v=20"></script></head>')
s=s.replace('<aside id="inspector">','<aside id="inspector"><div class="inspector-toolbar"><strong>圖與說明</strong><button id="inspector-expand" aria-expanded="false" aria-controls="inspector-dialog">展開右側 ↗</button></div>')
s=s.replace('</main><dialog id="focus-dialog">','</main><dialog id="inspector-dialog" aria-label="展開右側圖與說明"></dialog><dialog id="focus-dialog">')
p.write_text(s,encoding='utf-8')
p=r/'er-focus.js';s=p.read_text(encoding='utf-8').replace('window.ER_FOCUS={','window.ER_FOCUS={\n    refresh:paint,');p.write_text(s,encoding='utf-8')
