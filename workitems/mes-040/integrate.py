from pathlib import Path
import shutil
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
dest=Path('assets/mes-040');dest.mkdir(parents=True,exist_ok=True)
for src,name in [('exec-279ff840-7e35-4903-95a6-7856d4c18587.png','product-hold-v1.png'),('exec-199eee44-3de2-40e0-8d41-f4e05a64ef23.png','product-hold-mobile-v1.png')]:shutil.copy2(base/src,dest/name)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=39','er-topic-content.js?v=40'),encoding='utf-8')
