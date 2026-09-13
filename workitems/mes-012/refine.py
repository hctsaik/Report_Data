from pathlib import Path
R=Path(__file__).resolve().parents[2];p=R/'integrated-map.js';s=p.read_text(encoding='utf-8')
marker='function showCase(id)'
s=s.replace(marker,"function quickTopics(ids){$('quick-topics').innerHTML=ids.map(id=>`<button data-quick=\"${id}\">${data.groups.find(g=>g.id===id).title}</button>`).join('');document.querySelectorAll('[data-quick]').forEach(b=>b.onclick=()=>topic(b.dataset.quick));}\n"+marker)
s=s.replace("const refs=[...new Set(c.groups", "topic(c.groups[0],false);quickTopics(c.groups);const refs=[...new Set(c.groups")
s=s.replace("topic('lot',false);if(questionMode)","topic('lot',false);quickTopics(data.groups.map(g=>g.id));if(questionMode)")
p.write_text(s,encoding='utf-8')
