from pathlib import Path
R=Path(__file__).resolve().parents[2]
p=R/'data-map.html';s=p.read_text(encoding='utf-8');marker='<nav class="er-parts"'
s=s.replace(marker,'<div style="padding:18px 24px;background:#e6f1ff"><strong>跨圖整合理解：</strong> <a href="integrated-map.html?view=original">看整合大圖 →</a>　<a href="integrated-map.html?view=questions">跨圖聚焦題目 →</a></div>'+marker);p.write_text(s,encoding='utf-8')
p=R/'course.js';s=p.read_text(encoding='utf-8');marker='<a href="data-map.html?view=original#2676" data-er-sidebar>'
s=s.replace(marker,'<a href="integrated-map.html?view=original">ER 整合大圖</a><br><a href="integrated-map.html?view=questions">跨圖聚焦題目</a><br>'+marker);p.write_text(s,encoding='utf-8')
for name in ['operations.html','flow.html']:
 p=R/name;s=p.read_text(encoding='utf-8').replace('er-parts-20260913','er-integrated-20260913');p.write_text(s,encoding='utf-8')
p=R/'index.html';s=p.read_text(encoding='utf-8');s=s.replace('class="er-course-entry" href="data-map.html#2676"','class="er-course-entry" href="integrated-map.html?view=original"').replace('七張圖導讀：Lot／FOUP、Flow、設備、配方與 WIP','整合大圖與跨圖題目：Lot、Flow、設備、配方與 WIP');p.write_text(s,encoding='utf-8')
print('Integrated map linked from homepage, ER page and operations/flow sidebar')
