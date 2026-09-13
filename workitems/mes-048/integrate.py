from pathlib import Path
import shutil
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
dest=Path('assets/mes-048');dest.mkdir(parents=True,exist_ok=True)
for src,name in [('exec-a6e79850-af46-4e87-8a98-ac7d4cb14753.png','default-stocker-v1.png'),('exec-5ee5a8c6-1cd7-4750-ad7c-6630f030ad7b.png','default-stocker-mobile-v1.png')]:shutil.copy2(base/src,dest/name)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=47','er-topic-content.js?v=48'),encoding='utf-8')
s=Path('workitems/mes-043/check.py').read_text(encoding='utf-8').replace('mes-043','mes-048').replace('2673:recipe','2674:default').replace("['機台','多台','單台']","['Stocker','預設','FOUP']").replace('CSFRRCPGRPST','csfreqp_stk').replace('recipe-group-mobile-v1.png','default-stocker-mobile-v1.png').replace('recipe-group-v1.png','default-stocker-v1.png').replace('Recipe Group','Default Stocker')
Path('workitems/mes-048/check.py').write_text(s,encoding='utf-8')
