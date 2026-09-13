from pathlib import Path
r=Path(__file__).resolve().parents[2]
for p in (r/'ER/SUBJECTS').glob('*.svg'):
 s=p.read_text(encoding='utf-8')
 if '預到' in s:p.write_text(s.replace('預到','帶到'),encoding='utf-8')
p=r/'ER/SUBJECTS/subjects.json';s=p.read_text(encoding='utf-8').replace('預到','帶到（本站可用機台）');p.write_text(s,encoding='utf-8')
p=r/'subject-er.js';s=p.read_text(encoding='utf-8').replace('model=m;topics=data.subjects;',"const corrected=m.nodes.find(n=>n.id===m.mapping['2671:lot-eqp']);if(corrected){corrected.labels=corrected.labels.map(t=>t==='預到'?'帶到':t);}model=m;topics=data.subjects;");p.write_text(s,encoding='utf-8')
p=r/'subject-er.html';s=p.read_text(encoding='utf-8').replace('subject-er.js?v=1','subject-er.js?v=21');p.write_text(s,encoding='utf-8')
