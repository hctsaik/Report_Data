"""Recorded MES-004 first visual review corrections; no generated bitmap editing."""
from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'course-remake.js'
s=p.read_text(encoding='utf-8')
s=s.replace('--at:50%','--at:40%').replace('--at:87.5%','--at:90%')
s=s.replace('只展開追蹤的 3 槽','槽位展開示意 · 3 槽')
s=s.replace('<div data-frame-body>','<div data-frame-body aria-live="polite">')
s=s.replace('兩種處置都先保留原始差異，不能拿預期值覆蓋讀值。','兩種處置都先保留原始差異，不能拿預期值覆蓋讀值。')
p.write_text(s,encoding='utf-8')
