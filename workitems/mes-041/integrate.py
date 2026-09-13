from pathlib import Path
import shutil
base=Path('C:/Users/hctsa/.codex/generated_images/01a09892-9e9e-7fb3-90e6-f38a72d44d31')
dest=Path('assets/mes-041');dest.mkdir(parents=True,exist_ok=True)
for src,name in [('exec-310b6110-1b9a-4d6a-bd34-655c15362646.png','stream-arrival-v2.png'),('exec-b2d8f859-c046-4905-8ba8-c2864cd98179.png','stream-arrival-mobile-v1.png')]:shutil.copy2(base/src,dest/name)
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=40','er-topic-content.js?v=41'),encoding='utf-8')
p=Path('workitems/mes-041/check.py');s=Path('workitems/mes-040/check.py').read_text(encoding='utf-8').replace('mes-040','mes-041').replace('2673:product-hold','2673:stream').replace('2673:hold-link','2673:stream-link').replace("['PID','指定站點','統一處理']","['Flow','WPH','LDS']").replace('CSFRPRHold','Stream_fcst').replace('product-hold-mobile-v1.png','stream-arrival-mobile-v1.png').replace('product-hold-v1.png','stream-arrival-v2.png').replace('Product Hold','Stream');s=s.replace('  page.close()', '''  page.keyboard.press('Escape')
  page.evaluate('ER_ATLAS.selectNode(ER_ATLAS.model.mapping["2673:forecast"])')
  assert 'LDS' not in page.locator('#meaning').text_content()
  page.close()''');p.write_text(s,encoding='utf-8')
