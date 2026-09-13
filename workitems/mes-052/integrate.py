from pathlib import Path
import shutil
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
dest=Path('assets/mes-052');dest.mkdir(parents=True,exist_ok=True)
assets=[('250faf51-5538-4448-a0cb-562f0152d139','bmir-v3.png'),('7e7ee425-fbad-469b-83f6-6365f928541b','bmir-mobile-v1.png'),('bc3a42d0-cc71-46bf-a582-bb46009a0363','port-occupancy-v1.png'),('91a6195d-1c3a-415b-836a-a0e74b04eaf0','port-occupancy-mobile-v2.png'),('abce060e-71aa-4c1a-ab19-e37298e4a94a','lot-rqhbe-v2.png'),('edf5c1f8-17e8-4871-95df-93c67433150a','lot-rqhbe-mobile-v1.png'),('81662fde-187e-43fa-8493-4261e0d6d3e4','daily-snapshot-v1.png'),('5ab13b51-7f5a-49c5-b56e-5ba57083826f','daily-snapshot-mobile-v1.png')]
for src,name in assets:shutil.copy2(base/('exec-'+src+'.png'),dest/name)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=51','er-topic-content.js?v=52'),encoding='utf-8')
