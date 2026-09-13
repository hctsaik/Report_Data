from pathlib import Path
import shutil
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
dest=Path('assets/mes-044');dest.mkdir(parents=True,exist_ok=True)
for src,name in [('exec-f162a69c-ace1-4161-ac18-ac17d990716b.png','module-stage-step-v2.png'),('exec-c4bf2618-5aea-4f4a-80b2-31f7e29ca2a2.png','module-stage-step-mobile-v2.png')]:shutil.copy2(base/src,dest/name)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=43','er-topic-content.js?v=44'),encoding='utf-8')
s=Path('workitems/mes-043/check.py').read_text(encoding='utf-8').replace('mes-043','mes-044').replace('2673:recipe','2673:stage').replace("['機台','多台','單台']","['黃光','多個 Stage','Step']").replace('CSFRRCPGRPST','dm_tbl_info_stage').replace('recipe-group-mobile-v1.png','module-stage-step-mobile-v2.png').replace('recipe-group-v1.png','module-stage-step-v2.png').replace('Recipe Group','Stage Module')
Path('workitems/mes-044/check.py').write_text(s,encoding='utf-8')
