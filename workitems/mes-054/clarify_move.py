from pathlib import Path
p=Path('support.js');s=p.read_text(encoding='utf-8');start=s.index('function move()');end=s.index('function monitor()',start);part=s[start:end].replace('過站','進機');s=s[:start]+part+s[end:];p.write_text(s,encoding='utf-8')
