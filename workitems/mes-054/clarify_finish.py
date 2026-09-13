from pathlib import Path
p=Path('scenarios.js');s=p.read_text(encoding='utf-8');needle='最後才標為 Finished';assert needle in s;s=s.replace(needle,'最後才標為 Finished（本教學 Flow 完成，不代表 Lot E 已出貨）');p.write_text(s,encoding='utf-8')
