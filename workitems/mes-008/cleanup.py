from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'freshness.js'
s=p.read_text(encoding='utf-8')
a=s.index('function architecture()')
b=s.index('const freshnessViews=')
s=s[:a]+s[b:]
for prefix in ['const verdict=','const arrow=','const note=']:
    s='\n'.join(line for line in s.split('\n') if not line.startswith(prefix))
p.write_text(s,encoding='utf-8')
p=r/'freshness.html'
s=p.read_text(encoding='utf-8').replace('<link rel="stylesheet" href="freshness.css">','')
p.write_text(s,encoding='utf-8')
