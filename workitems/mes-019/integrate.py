"""One-time WPH display correction. Source model retains original labels for audit."""
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'er-focus.js';s=p.read_text(encoding='utf-8')
s=s.replace('nodes=new Map(m.nodes.map(n=>[n.id,n]));','''nodes=new Map(m.nodes.map(n=>[n.id,n]));
    for(const [ref,labels] of [['2673:wph',['機群 WPH 定義','F12DM.DM_TBL_IE_CTWPH']],['2673:wph-link',['WPH 定義對應']]]){const id=m.mapping[ref];if(nodes.has(id))nodes.set(id,{...nodes.get(id),labels});}
    ''')
s=s.replace("const more=$('focus-more');", "if([model.mapping['2673:wph'],model.mapping['2673:wph-link']].includes(root))$('focus-note').append(' 業務定義：生管為機群訂定預期 WPH。下方是原資料關聯，不表示由 LR 定義個別機台的產出；請看專屬參考圖。');const more=$('focus-more');")
p.write_text(s,encoding='utf-8')
p=r/'er-atlas.html';s=p.read_text(encoding='utf-8').replace('er-atlas.js?v=17','er-atlas.js?v=19').replace('er-focus.js?v=18','er-focus.js?v=19');p.write_text(s,encoding='utf-8')
