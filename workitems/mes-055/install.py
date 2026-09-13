"""Install MES055 page hooks once; safe to rerun."""
from pathlib import Path
for name in ['index.html','topic.html','er-atlas.html']:
 p=Path(name);s=p.read_text(encoding='utf-8')
 if 'lesson-refresh.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="lesson-refresh.css?v=55"></head>')
 if name=='index.html' and 'lesson-refresh.js' not in s:s=s.replace('</head>','<script defer src="lesson-refresh.js?v=55"></script></head>')
 if name!='index.html' and 'topic-refresh.js' not in s:
  import re
  s=re.sub(r'(<script defer src="er-teaching-base.js[^<]*</script>)',r'\1<script defer src="topic-refresh.js?v=55"></script>',s)
 p.write_text(s,encoding='utf-8')
