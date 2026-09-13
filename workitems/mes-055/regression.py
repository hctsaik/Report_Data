"""Run the existing all-topic gate against MES055 without replacing old evidence."""
from pathlib import Path
source=Path('workitems/mes-054/check_topics.py').read_text(encoding='utf-8')
source=source.replace("tests/evidence/mes-054/topics","tests/evidence/mes-055/regression")
source=source.replace("if key in ['lot','carrier','load']:","if key=='load': page.locator('.refresh-lab summary').click()\n   if key in ['lot','carrier','load']:")
exec(compile(source,'mes055-topic-regression','exec'))
