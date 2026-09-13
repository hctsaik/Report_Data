from pathlib import Path
import shutil
p=Path('assets/mes-035');p.mkdir(parents=True,exist_ok=True)
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
for src,dst in [('exec-27342274-4496-4f9e-b90c-0ce7ad44744a.png','load-port-v1.png'),('exec-81974ed8-7678-4de5-86ee-03cafeed12d5.png','load-port-mobile-v1.png')]:shutil.copy2(base/src,p/dst)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=34','er-topic-content.js?v=35'),encoding='utf-8')
p=Path('er-atlas.js');s=p.read_text(encoding='utf-8').replace("r.id==='transfer'?teaching.mcs.meaning:r.meaning", "r.id==='transfer'?teaching.mcs.meaning:r.id==='port'?teaching.port.meaning:r.meaning");p.write_text(s,encoding='utf-8')
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-atlas.js?v=31','er-atlas.js?v=35'),encoding='utf-8')
