from pathlib import Path
import shutil
p=Path('assets/mes-039');p.mkdir(parents=True,exist_ok=True)
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
for src,dst in [('exec-f3142aa4-5e67-4fdb-9e2b-96529e258450.png','move-uses-v2.png'),('exec-2b6bacd7-ddb9-4cc8-8ea0-ea952d3e7d1c.png','move-uses-mobile-v2.png')]:shutil.copy2(base/src,p/dst)
p=Path('er-atlas.js');p.write_text(p.read_text(encoding='utf-8').replace("r.id==='port'?teaching.port.meaning:r.meaning", "r.id==='port'?teaching.port.meaning:r.id==='move'?teaching.move.meaning:r.meaning"),encoding='utf-8')
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=38','er-topic-content.js?v=39').replace('er-atlas.js?v=35','er-atlas.js?v=39'),encoding='utf-8')
