from pathlib import Path
import shutil
p=Path('assets/mes-036');p.mkdir(parents=True,exist_ok=True)
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
for src,dst in [('exec-61fa1951-7de6-4c32-9359-54835f31258f.png','foup-query-lot-v1.png'),('exec-8f00ac65-18ce-4a79-be46-650451b3454d.png','foup-query-lot-mobile-v1.png')]:shutil.copy2(base/src,p/dst)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=35','er-topic-content.js?v=36'),encoding='utf-8')
