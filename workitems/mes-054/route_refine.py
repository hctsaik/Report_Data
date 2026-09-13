from pathlib import Path
p=Path('learning.js');s=p.read_text(encoding='utf-8');s=s.replace("function unit(u){document.title", "function unit(u){const before=C.nextUnit(u.id,-1),after=C.nextUnit(u.id,1);document.title")
s=s.replace("u.id?link(url(u.id-1),'← 上一單元：'+C.units[u.id-1].title)","before?link(url(before.id),'← 上一單元：'+before.title)")
s=s.replace("u.id<9?link(url(u.id+1),'下一單元：'+C.units[u.id+1].title+' →','learn-button primary')","after?link(url(after.id),'下一單元：'+after.title+' →','learn-button primary')")
p.write_text(s,encoding='utf-8')
p=Path('site-shell.js');s=p.read_text(encoding='utf-8');s=s.replace("{href:'learning.html?unit='+Math.min(u.id+1,9),label:u.id<9?'下一單元：'+C.units[u.id+1].title:'綜合任務'}", "{href:C.nextUnit(u.id)?'learning.html?unit='+C.nextUnit(u.id).id:'tasks.html',label:C.nextUnit(u.id)?'下一單元：'+C.nextUnit(u.id).title:'綜合任務'}")
p.write_text(s,encoding='utf-8')
print('Next unit now follows the selected learner route; full curriculum remains accessible.')
