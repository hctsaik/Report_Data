from pathlib import Path
import shutil
root=Path('workitems/mes-016');(root/'baseline').mkdir(parents=True,exist_ok=True)
for f in ['er-atlas.js','er-atlas.html','er-atlas.css']:shutil.copy2(f,root/'baseline'/f)
p=Path('er-atlas.js');s=p.read_text(encoding='utf-8')
s=s.replace("startNode=e.target.closest('[data-node]')?.id", "startNode=hitNode(e)")
pos="const canvas=$('canvas');"
hit="""// Give tiny overview nodes a forgiving screen-space hit target.
function hitNode(e){const direct=e.target.closest('[data-node]');if(direct)return direct.id;
 let best=null,distance=11;
 svg.querySelectorAll('[data-node]').forEach(g=>{const b=g.getBoundingClientRect();const d=Math.hypot(Math.max(b.left-e.clientX,0,e.clientX-b.right),Math.max(b.top-e.clientY,0,e.clientY-b.bottom));if(d<distance){distance=d;best=g.id}});return best;
}
"""
s=s.replace(pos,hit+pos)
# Movement below the click threshold must not move the diagram under the pointer.
s=s.replace("if(Math.abs(dx)+Math.abs(dy)>4)moved=true;setView", "if(Math.hypot(dx,dy)>7)moved=true;if(!moved)return;setView")
# Use one pointer activation, rather than selecting again from a synthetic click.
s=s.replace("g.addEventListener('click',()=>{if(!moved)selectNode(g.id)});", "")
old="$('teaching-link').href=t.link;}"
new="""$('teaching-link').href=t.link;
const focus={lot:[68,63,28,16],carrier:[34,19,33,65],equipment:[1,19,33,65]}[key];
$('teaching-focus').hidden=!focus;if(focus){const f=$('teaching-focus');f.style.left=focus[0]+'%';f.style.top=focus[1]+'%';f.style.width=focus[2]+'%';f.style.height=focus[3]+'%';f.style.borderColor=t.color;}
$('teaching-current').textContent=t.title||'現場物件總覽';$('teaching-current').style.borderColor=t.color||'#52728e';
}"""
assert old in s;s=s.replace(old,new)
# Along-line navigation is also a node selection for the companion panel.
s=s.replace("const id=walkIds[walkIndex],b=box(id)","const id=walkIds[walkIndex];showTeaching(teachingForNode(id));const b=box(id)")
# Keep highlight with the enlarged image.
s=s.replace("$('teaching-dialog').showModal()", "$('teaching-large-focus').style.cssText=$('teaching-focus').style.cssText;$('teaching-large-focus').hidden=$('teaching-focus').hidden;$('teaching-dialog').showModal()")
p.write_text(s,encoding='utf-8')
p=Path('er-atlas.html');s=p.read_text(encoding='utf-8').replace('?v=4','?v=6')
s=s.replace('<figure class="teaching-figure">','<p id="teaching-current" role="status"></p><figure class="teaching-figure">')
s=s.replace('<img id="teaching-image" alt="">','<span class="physical-image"><img id="teaching-image" alt=""><i id="teaching-focus" hidden></i></span>')
s=s.replace('<img id="teaching-large" alt="">','<div class="physical-image"><img id="teaching-large" alt=""><i id="teaching-large-focus" hidden></i></div>')
p.write_text(s,encoding='utf-8')
p=Path('er-atlas.css');s=p.read_text(encoding='utf-8')+'''
.teaching-figure button .physical-image,.physical-image{display:block;position:relative;padding:0;background:white}.physical-image i{position:absolute;border:3px solid;box-shadow:0 0 0 2px white;border-radius:5px;pointer-events:none}#teaching-current{font-size:15px;font-weight:bold;padding:8px 12px;border-left:4px solid;background:#f0f6fc}#canvas [data-node]{cursor:pointer}
''';p.write_text(s,encoding='utf-8')
