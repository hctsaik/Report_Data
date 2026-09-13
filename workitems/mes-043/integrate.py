from pathlib import Path
import shutil
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
dest=Path('assets/mes-043');dest.mkdir(parents=True,exist_ok=True)
for src,name in [('exec-ce4c01c4-b3b0-4565-83d3-e877c8f3801d.png','recipe-group-v1.png'),('exec-df333e75-a734-4b79-88a8-8d1891f3ea74.png','recipe-group-mobile-v1.png')]:shutil.copy2(base/src,dest/name)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=42','er-topic-content.js?v=43'),encoding='utf-8')
s=Path('workitems/mes-040/check.py').read_text(encoding='utf-8').replace('mes-040','mes-043').replace('2673:product-hold','2673:recipe').replace('2673:hold-link','2673:recipe-link').replace("['PID','指定站點','統一處理']","['機台','多台','單台']").replace('CSFRPRHold','CSFRRCPGRPST').replace('product-hold-mobile-v1.png','recipe-group-mobile-v1.png').replace('product-hold-v1.png','recipe-group-v1.png').replace('Product Hold','Recipe Group')
Path('workitems/mes-043/check.py').write_text(s,encoding='utf-8')
