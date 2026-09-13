from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
for name in ['flow.html','operations.html']:
    p=ROOT/name
    text=p.read_text(encoding='utf-8')
    if 'course-extension.js' not in text:
        text=text.replace('</head>','<script src="course-extension.js" defer></script></head>')
        p.write_text(text,encoding='utf-8')
