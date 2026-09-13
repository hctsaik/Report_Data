from pathlib import Path
R=Path(__file__).resolve().parents[2]
p=R/'er-atlas.js';s=p.read_text(encoding='utf-8');s=s.replace(":'這是原圖的資料對象。",":n.kind==='circle'?'這個橢圓保留原圖的概念／屬性註記；不直接當作已確認的資料表或欄位。':'這是原圖的資料對象。");p.write_text(s,encoding='utf-8')
p=R/'er-atlas.html';s=p.read_text(encoding='utf-8').replace('href="er-atlas.css"','href="er-atlas.css?v=2"').replace('src="er-atlas.js"','src="er-atlas.js?v=2"');p.write_text(s,encoding='utf-8')
