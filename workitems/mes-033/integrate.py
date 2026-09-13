from pathlib import Path
import shutil
p=Path('assets/mes-033');p.mkdir(parents=True,exist_ok=True)
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
for src,dst in [('exec-779d282e-c257-4704-826e-4de060bdaf40.png','transfer-history-v1.png'),('exec-afb93e3e-e1b9-4950-9d62-837adca18966.png','transfer-history-mobile-v1.png')]:shutil.copy2(base/src,p/dst)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=32','er-topic-content.js?v=33'),encoding='utf-8')
