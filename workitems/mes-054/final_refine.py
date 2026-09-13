from pathlib import Path
p=Path('data-map.js');s=p.read_text(encoding='utf-8');s=s.replace('快照保存某個時點工廠內的在製批次；之後 Lot 可能已過站或離開。快照仍有分析價值，但不能直接當今天此刻的位置。','KER_WIP_Y_BTH 每天早上07:20保存機群狀況與相關KPI；快照可回看當時資料，不能直接當作目前即時狀況。').replace('歷史快照回答當時有哪些 WIP；現在的行動需要符合時效的資料。','每日快照回答當時的機群與KPI；現在的行動需要符合時效的資料。').replace('使用者確認標題為「星期一的七點二十分的 WIP」。','使用者確認：每天早上07:20保存機群狀況與KPI。');p.write_text(s,encoding='utf-8')
p=Path('course.js');s=p.read_text(encoding='utf-8').replace("sessionStorage.getItem('mes-scenarios:'","localStorage.getItem('mes-scenarios:v54:'").replace("sessionStorage.setItem('mes-scenarios:'","localStorage.setItem('mes-scenarios:v54:'");p.write_text(s,encoding='utf-8')
p=Path('catalog.js');s=p.read_text(encoding='utf-8').replace('v.hash===u.hash',"v.hash.split('?')[0]===u.hash.split('?')[0]");p.write_text(s,encoding='utf-8')
p=Path('site-shell.js');s=p.read_text(encoding='utf-8').replace('v.hash===here.hash',"v.hash.split('?')[0]===here.hash.split('?')[0]");p.write_text(s,encoding='utf-8')
p=Path('learning.js');s=p.read_text(encoding='utf-8');s=s.replace("if(!C.routes[route])route='newcomer';","if(!C.routes[route])route='newcomer';set('mes-route',route);")
# The route controls the recommendation list; full unit order remains always available.
p.write_text(s,encoding='utf-8')
print('Corrected snapshot semantics, persistent scenario progress and lab-case curriculum matching.')
