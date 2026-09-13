from pathlib import Path
import shutil
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
dest=Path('assets/mes-049');dest.mkdir(parents=True,exist_ok=True)
for src,name in [('exec-eafdac9d-a0e2-4e94-86ea-fbf19bb36dfa.png','ohb-near-tool-v1.png'),('exec-1003f2b9-8ac5-400c-87f7-79be13cbe732.png','ohb-near-tool-mobile-v1.png')]:shutil.copy2(base/src,dest/name)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=48','er-topic-content.js?v=49'),encoding='utf-8')
s=Path('workitems/mes-043/check.py').read_text(encoding='utf-8').replace('mes-043','mes-049').replace("['2673:recipe','2673:recipe-link']","['2674:ohb-eqp','2674:ohb-link','2674:ohb-status','2674:ohb-status-link']").replace('2673:recipe','2674:ohb-eqp').replace("['機台','多台','單台']","['OHB','暫置架','Stocker']").replace('CSFRRCPGRPST','csfrohb_eqp').replace('recipe-group-mobile-v1.png','ohb-near-tool-mobile-v1.png').replace('recipe-group-v1.png','ohb-near-tool-v1.png').replace('Recipe Group','OHB')
Path('workitems/mes-049/check.py').write_text(s,encoding='utf-8')
