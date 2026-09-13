from pathlib import Path
import shutil
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
dest=Path('assets/mes-047');dest.mkdir(parents=True,exist_ok=True)
for src,name in [('exec-729226c8-92b9-4f5c-8189-6d9f103aaf40.png','eqp-owner-v1.png'),('exec-b6cd965d-1bae-4e6b-b87f-8d7c035ed616.png','eqp-owner-mobile-v1.png')]:shutil.copy2(base/src,dest/name)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=46','er-topic-content.js?v=47'),encoding='utf-8')
s=Path('workitems/mes-043/check.py').read_text(encoding='utf-8').replace('mes-043','mes-047').replace('2673:recipe','2674:owner').replace("['機台','多台','單台']","['機群','管理單位','廠商名稱']").replace('CSFRRCPGRPST','MFG_EQP_OWNER_BT').replace('recipe-group-mobile-v1.png','eqp-owner-mobile-v1.png').replace('recipe-group-v1.png','eqp-owner-v1.png').replace('Recipe Group','EQP owner')
Path('workitems/mes-047/check.py').write_text(s,encoding='utf-8')
