from pathlib import Path
import shutil
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
dest=Path('assets/mes-050');dest.mkdir(parents=True,exist_ok=True)
for src,name in [('exec-f67ca049-8b94-4454-9164-25ba0cbe197a.png','ker-overview-v1.png'),('exec-3ca61a32-4ea1-458c-b2cb-da939d39eeef.png','ker-overview-mobile-v1.png')]:shutil.copy2(base/src,dest/name)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=49','er-topic-content.js?v=50'),encoding='utf-8')
s=Path('workitems/mes-043/check.py').read_text(encoding='utf-8').replace('mes-043','mes-050').replace("['2673:recipe','2673:recipe-link']","['2675:eqp','2675:group-link','2675:chamber','2675:chamber-link','2675:virtual','2675:virtual-link','2675:eqp-oee','2675:eqp-oee-link','2675:group-oee','2675:group-oee-link','2675:group-history','2675:group-history-link']").replace('2673:recipe','2675:eqp').replace("['機台','多台','單台']","['KER','Report']").replace('CSFRRCPGRPST','KER_EMP_EQP_GRP_CAP_UT').replace('recipe-group-mobile-v1.png','ker-overview-mobile-v1.png').replace('recipe-group-v1.png','ker-overview-v1.png').replace('Recipe Group','KER')
Path('workitems/mes-050/check.py').write_text(s,encoding='utf-8')
