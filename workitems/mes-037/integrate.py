from pathlib import Path
import shutil
p=Path('assets/mes-037');p.mkdir(parents=True,exist_ok=True)
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
for src,dst in [('exec-754c486f-effb-45ce-a617-a800ad07847a.png','predispatch-history-v2.png'),('exec-18a5b207-5edd-4434-8b9c-7fdb7261102c.png','predispatch-history-mobile-v1.png')]:shutil.copy2(base/src,p/dst)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=36','er-topic-content.js?v=37'),encoding='utf-8')
