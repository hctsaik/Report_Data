from pathlib import Path
p=Path('learning.js');s=p.read_text(encoding='utf-8');old='input.oninput=draw;draw()}'
new='''input.oninput=draw;draw();fetch('ER/INTEGRATED/er-model-v2.json').then(r=>r.json()).then(m=>{const builtin={lot:['2671:lot'],carrier:['2671:cast'],equipment:['2671:eqp'],flow:['2673:flow'],recipe:['2677:recipe','2673:lr-eqp'],qtime:['2672:qtime'],predispatch:['2671:predispatch'],wph:['2673:wph']};for(const e of entries){const refs=topics[e.key]?.refs||builtin[e.key]||[];for(const ref of refs){const n=m.nodes.find(n=>n.id===m.mapping[ref]);if(n)e.search+=' '+n.labels.join(' ')}}draw()}).catch(()=>{});}'''
assert old in s;s=s.replace(old,new);p.write_text(s,encoding='utf-8')
