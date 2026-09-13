from pathlib import Path
R=Path(__file__).resolve().parents[2];B=R/'workitems/mes-014/baseline';B.mkdir(exist_ok=True)
p=R/'integrated-map.html';backup=B/p.name
if not backup.exists():backup.write_bytes(p.read_bytes())
p.write_text('''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fab 整合 ER</title><script>location.replace('er-atlas.html'+location.search+location.hash)</script></head><body><a href="er-atlas.html">開啟 Fab 整合 ER 圖與聚焦題目</a></body></html>''',encoding='utf-8')
print('Existing integrated-map URL now opens the actual ER atlas, preserving mode and question')
