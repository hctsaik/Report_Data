from pathlib import Path
p=Path('er-atlas.js');s=p.read_text(encoding='utf-8')
s=s.replace("if(teachingForNode(id)==='overview').textContent=", "if(teachingForNode(id)==='overview')document.getElementById('teaching-caption').textContent=")
p.write_text(s,encoding='utf-8')
