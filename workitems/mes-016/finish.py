from pathlib import Path
p=Path('er-atlas.js');s=p.read_text(encoding='utf-8');needle="$('status').textContent='已定位：'+n.labels.join(' / ');"
s=s.replace(needle,"if(teaching[teachingForNode(id)].meaning)$('meaning').textContent=teaching[teachingForNode(id)].meaning;"+needle);p.write_text(s,encoding='utf-8')
p=Path('AGENTS.md');s=p.read_text(encoding='utf-8');p.write_text('''# 最新接續：MES-016 ER 直接點擊與右圖同步

使用者指出點 ER 圖右圖沒有更新。已用真實 mouse/touch 測試五類節點，增加小節點命中容差、避免點擊微移變成拖曳，右图同步選取名稱與圖面焦點。不能只用 ER_ATLAS.selectNode() 測試宣稱點擊有效。驗證 python workitems/mes-016/check.py，證據 tests/evidence/mes-016。閱讀 workitems/mes-016/REVIEW.md。一次性 fix.py/finish.py 不重跑。

'''+s,encoding='utf-8')
