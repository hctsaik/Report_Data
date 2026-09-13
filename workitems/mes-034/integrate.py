from pathlib import Path
import shutil
p=Path('assets/mes-034');p.mkdir(parents=True,exist_ok=True)
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
for src,dst in [('exec-0185114a-c1b7-4a3e-b049-ff969fafeccb.png','eqp-bay-v1.png'),('exec-5c62311d-2f2d-4e8a-9378-43332a211819.png','eqp-bay-mobile-v1.png')]:shutil.copy2(base/src,p/dst)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=33','er-topic-content.js?v=34'),encoding='utf-8')
