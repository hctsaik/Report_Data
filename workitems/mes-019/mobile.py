"""One-time responsive picture integration."""
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'er-atlas.html';s=p.read_text(encoding='utf-8').replace('<img id="teaching-image" alt="">','<picture><source id="teaching-mobile" media="(max-width:600px)"><img id="teaching-image" alt=""></picture>');p.write_text(s,encoding='utf-8')
p=r/'er-atlas.js';s=p.read_text(encoding='utf-8').replace("image:'assets/mes-019/group-wph-v1.png',","image:'assets/mes-019/group-wph-v1.png',mobile:'assets/mes-019/group-wph-mobile-v1.png',")
s=s.replace("$('teaching-image').src=t.image;", "$('teaching-mobile').srcset=t.mobile||t.image;$('teaching-image').src=t.image;")
s=s.replace("$('teaching-large').src=$('teaching-image').src;", "$('teaching-large').src=$('teaching-image').currentSrc||$('teaching-image').src;")
p.write_text(s,encoding='utf-8')
p=r/'workitems/mes-019/check.py';s=p.read_text(encoding='utf-8').replace(".endswith('assets/mes-019/group-wph-v1.png')", ".endswith('assets/mes-019/group-wph-mobile-v1.png' if width==390 else 'assets/mes-019/group-wph-v1.png')");p.write_text(s,encoding='utf-8')
