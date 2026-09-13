from pathlib import Path
import shutil
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
dest=Path('assets/mes-042');dest.mkdir(parents=True,exist_ok=True)
for src,name in [('exec-0db60db9-ba62-44f6-9b6c-5b02b869e4ce.png','lot-forecast-v2.png'),('exec-0f828b66-7f05-41f3-a268-ba7dedf3478b.png','lot-forecast-mobile-v1.png')]:shutil.copy2(base/src,dest/name)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=41','er-topic-content.js?v=42'),encoding='utf-8')
s=Path('workitems/mes-041/check.py').read_text(encoding='utf-8').replace('mes-041','mes-042').replace('2673:stream','2673:forecast').replace("['Flow','WPH','LDS']","['Flow','WPH','預計到站時間']").replace('Stream_fcst','dm_tbl_lot_forecast').replace('stream-arrival-mobile-v1.png','lot-forecast-mobile-v1.png').replace('stream-arrival-v2.png','lot-forecast-v2.png').replace('PASS Stream','PASS Lot forecast')
Path('workitems/mes-042/check.py').write_text(s,encoding='utf-8')
