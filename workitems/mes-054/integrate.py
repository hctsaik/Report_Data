from pathlib import Path
root=Path(__file__).resolve().parents[2]
files=['index.html','operations.html','flow.html','freshness.html','advanced.html','support.html','er-atlas.html','data-map.html','subject-er.html','ER/NEW/index.html']
backup=root/'workitems/mes-054/baseline';backup.mkdir(parents=True,exist_ok=True)
for name in files:
 p=root/name;s=p.read_text(encoding='utf-8');b=backup/name;b.parent.mkdir(parents=True,exist_ok=True);b.write_text(s,encoding='utf-8')
 prefix='../../' if '/' in name else ''
 tags=f'<link rel="stylesheet" href="{prefix}site-shell.css?v=54"><script defer src="{prefix}catalog.js?v=54"></script><script defer src="{prefix}site-shell.js?v=54"></script>'
 if name=='index.html':
  s=s.replace('<head>','<head>\n<script>if(!location.hash&&!new URLSearchParams(location.search).has("erReturn"))location.replace("learning.html"+location.search);</script>',1)
 s=s.replace('</head>',tags+'</head>',1);p.write_text(s,encoding='utf-8')
for name in ['course.js','course-remake.js','support.js','data-map.js','course-extension.js','course-content.js']:
 p=root/name;s=p.read_text(encoding='utf-8');(backup/name).write_text(s,encoding='utf-8')
 if name=='course.js':s=s.replace('✓ Stage A、B、C 都完成；L023 Finished。','✓ 本教學 Flow 已完成；這不表示 Lot E 已出貨。')
 if name=='course-remake.js':s=s.replace('✓ 六站都有完成紀錄 · Finished','✓ 六站都有完成紀錄 · 本教學 Flow 完成，非 Lot E 出貨')
 if name=='support.js':s=s.replace('AAA 正式縮寫、AVL／Eff／Lost／Up 的狀態或計算方式','AAA 正式縮寫、EFF 公式與指標彙總方式；已確認 AVL 為期間 Availability、設備 Lost 為閒置、UP 為加工中')
 if name=='data-map.js':s=s.replace('星期一 07:20','每天 07:20').replace('星期一07:20','每天07:20')
 if name=='course-extension.js':
  start=s.index('  const main=');end=s.index('\n}',start);s=s[:start]+s[end:]
 p.write_text(s,encoding='utf-8')
print('Integrated shared navigation into 10 legacy entries; preserved original source ER and legacy hashes.')
