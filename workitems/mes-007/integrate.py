from pathlib import Path
root=Path(__file__).resolve().parents[2]
for name in ['operations.html','flow.html']:
    p=root/name
    s=p.read_text(encoding='utf-8-sig')
    s=s.replace('<script src="course.js" defer>', '<link rel="stylesheet" href="course-illustrated.css"><script src="course-illustrated.js" defer></script><script src="course.js" defer>')
    p.write_text(s,encoding='utf-8')
p=root/'index.html';s=p.read_text(encoding='utf-8')
s=s.replace('<p class="eyebrow">第一課 · 基本物件</p>','<a class="course-link" href="freshness.html">第四部分：資料新鮮度與來源選擇 →</a>\n      <p class="eyebrow">第一課 · 基本物件</p>')
p.write_text(s,encoding='utf-8')
p=root/'course.js';s=p.read_text(encoding='utf-8')
s=s.replace('</a></div><button class="button mobile-menu"','</a><a href="freshness.html">04 資料新鮮度</a></div><button class="button mobile-menu"')
s=s.replace('第三部分 · Flow 深入</a></div></aside>','第三部分 · Flow 深入</a><br><a href="freshness.html">第四部分 · 資料新鮮度</a></div></aside>')
p.write_text(s,encoding='utf-8')
print('Integrated illustrations and fourth course entry.')
