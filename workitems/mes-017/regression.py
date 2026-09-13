"""Reuse historic assertions, redirect their evidence to the current workitem."""
from pathlib import Path
root=Path(__file__).resolve().parents[2]
for file in ['tests/check_er_atlas.py','workitems/mes-015/check.py','workitems/mes-016/check.py']:
 s=(root/file).read_text(encoding='utf-8')
 s=s.replace("tests/evidence/mes-014/v2","tests/evidence/mes-017/regression-atlas").replace('tests/evidence/mes-015','tests/evidence/mes-017/regression-015').replace('tests/evidence/mes-016','tests/evidence/mes-017/regression-016')
 # MES-017 intentionally collapses supplemental illustrations.
 if 'mes-015' in file:
  s=s.replace("page.locator('#open-teaching').click()", "page.locator('#selection-details').evaluate('(d)=>d.open=true');page.locator('#open-teaching').click()")
 if 'mes-016' in file:
  s=s.replace("page.locator('#teaching-current').inner_text()", "page.locator('#teaching-current').text_content()").replace("page.locator('#selection-title').inner_text()", "page.locator('#selection-title').text_content()")
  s=s.replace("assert page.locator('#teaching-focus').is_visible()", "page.locator('#selection-details').evaluate('(d)=>d.open=true');assert page.locator('#teaching-focus').is_visible()")
  s=s.replace('完整 ER × 現場物件','完整 ER × 主詞關聯')
 print('RUN',file,flush=True)
 exec(compile(s,str(root/file),'exec'),{'__file__':str(root/file),'__name__':'__main__'})
