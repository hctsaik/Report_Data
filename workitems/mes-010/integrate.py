from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'advanced.html'
t=p.read_text(encoding='utf-8')
link='<a href="support.html#cw">CW 與設備監控</a>'
if link not in t:t=t.replace('<a href="freshness.html">資料新鮮度</a>','<a href="freshness.html">資料新鮮度</a>'+link)
p.write_text(t,encoding='utf-8')
p=root/'support.js';t=p.read_text(encoding='utf-8')
for a,b in [('量测','量測'),('满足','滿足'),('监控','監控')]:t=t.replace(a,b)
p.write_text(t,encoding='utf-8')
