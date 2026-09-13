from pathlib import Path
p=Path('er-atlas.js');s=p.read_text(encoding='utf-8')
needle='Object.assign(teaching, window.ER_TOPIC_CONTENT.topics);'
s=s.replace(needle,needle+'''
for(const key of ['lot','carrier','load'])Object.assign(teaching[key],{
 title:key==='lot'?'Lot 與 Wafer：同一批中的不同晶圓':key==='carrier'?'FOUP 內容物：Lot、Wafer 與 Slot':'裝載關係：Lot、Wafer 與 FOUP',
 meaning:window.ER_LOT_WAFER.description,details:window.ER_LOT_WAFER.details,
 image:undefined,mobile:undefined,link:undefined
});
''')
s=s.replace("$('topic-detail').innerHTML=t.details||'';", "$('topic-detail').innerHTML=t.details||'';window.ER_LOT_WAFER.mount();")
s=s.replace("const focus={lot:[68,63,28,16],carrier:[34,19,33,65],equipment:[1,19,33,65]}[key];", "const focus=hasImage?{equipment:[1,19,33,65]}[key]:null;")
s=s.replace("r.id==='pd'?teaching.pd.meaning:r.meaning", "r.id==='pd'?teaching.pd.meaning:r.id==='load'?teaching.load.meaning:r.meaning")
p.write_text(s,encoding='utf-8')
p=Path('er-atlas.html');s=p.read_text(encoding='utf-8').replace('<script defer src="er-atlas.js?v=29">','<link rel="stylesheet" href="er-lot-wafer.css?v=30"><script defer src="er-lot-wafer.js?v=30"></script><script defer src="er-atlas.js?v=30">');p.write_text(s,encoding='utf-8')
