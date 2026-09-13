from pathlib import Path
import shutil
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
dest=Path('assets/mes-046');dest.mkdir(parents=True,exist_ok=True)
for src,name in [('exec-3f813f9a-59f7-4558-b86d-7882d5da6271.png','part-flow-version-v2.png'),('exec-155ca32e-fde7-4217-9092-12a6424ed55c.png','part-flow-version-mobile-v1.png')]:shutil.copy2(base/src,dest/name)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=45','er-topic-content.js?v=46'),encoding='utf-8')
s=Path('workitems/mes-043/check.py').read_text(encoding='utf-8').replace('mes-043','mes-046').replace('2673:recipe','2673:part').replace("['機台','多台','單台']","['Flow','進版','版本']").replace('CSFRRCPGRPST','frprodspec').replace('recipe-group-mobile-v1.png','part-flow-version-mobile-v1.png').replace('recipe-group-v1.png','part-flow-version-v2.png').replace('Recipe Group','PART')
Path('workitems/mes-046/check.py').write_text(s,encoding='utf-8')
