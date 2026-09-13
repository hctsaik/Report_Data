from pathlib import Path
import shutil
p=Path('assets/mes-038');p.mkdir(parents=True,exist_ok=True)
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
for src,dst in [('exec-68d1eb07-024f-4913-89c1-3775b5c91b9f.png','lot-history-v2.png'),('exec-8cefb873-6350-4600-a325-85058188c5b4.png','lot-history-mobile-v1.png')]:shutil.copy2(base/src,p/dst)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=37','er-topic-content.js?v=38'),encoding='utf-8')
