from pathlib import Path
import shutil
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
dest=Path('assets/mes-045');dest.mkdir(parents=True,exist_ok=True)
for src,name in [('exec-ae9eb2b0-0fd9-4f7b-8579-592bc19c2ad3.png','srts-sampling-v1.png'),('exec-68595fba-bdf4-4dbd-80ab-d92256f0204e.png','srts-sampling-mobile-v2.png')]:shutil.copy2(base/src,dest/name)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=44','er-topic-content.js?v=45'),encoding='utf-8')
s=Path('workitems/mes-043/check.py').read_text(encoding='utf-8').replace('mes-043','mes-045').replace('2673:recipe','2673:srts').replace("['機台','多台','單台']","['Sampling rule','Part','30%']").replace('CSFRRCPGRPST','csfrsrts').replace('recipe-group-mobile-v1.png','srts-sampling-mobile-v2.png').replace('recipe-group-v1.png','srts-sampling-v1.png').replace('Recipe Group','SRTS')
Path('workitems/mes-045/check.py').write_text(s,encoding='utf-8')
