from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'freshness.js';s=p.read_text(encoding='utf-8')
old="v==='mart'?'這是 09:51 的 DEV，不能當成 10:01 的位置。改找 Native 或 TX；Mart 的歷史內容本身沒有因此變錯。':control?"
new="v==='mart'?(control?'這是 09:51 的 DEV，不能當成 10:01 的位置。現在要 Auto Hold，改由 TX／核准控制交易取得當下狀態，並在執行時重驗條件。':'這是 09:51 的 DEV，不能當成 10:01 的位置。改找 Native 或 TX；Mart 的歷史內容本身沒有因此變錯。'):control?"
assert old in s;s=s.replace(old,new);p.write_text(s,encoding='utf-8')
p=root/'tests/check_illustrated.py';s=p.read_text(encoding='utf-8');target="        assert page.locator('#query-age').inner_text()==age"
s=s.replace(target,target+"\n        if purpose=='control':assert '重驗' in page.locator('#ai-answer').inner_text()\n        if purpose=='control' and source=='mart':assert '改找 Native 或 TX' not in page.locator('#ai-answer').inner_text()")
p.write_text(s,encoding='utf-8')
p=root/'workitems/mes-007/REVIEW.md';s=p.read_text(encoding='utf-8').replace('另修正實頁問題：','另修正實頁問題：AI案例選Mart＋Auto Hold時，原通用回饋「改找Native或TX」太寬；改為明確要求TX／核准控制交易執行時重驗，並新增分支斷言。')
p.write_text(s,encoding='utf-8')
