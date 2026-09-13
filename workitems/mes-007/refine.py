from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'course-remake.js';s=p.read_text(encoding='utf-8').replace('有效量測值 98–102（含邊界）合格；數值無實廠單位與製程含義。','有效線寬 98–102 nm（含邊界）合格；單位與門檻是本課假設，不是實廠規格。')
p.write_text(s,encoding='utf-8')
for name in ['check_courses.py','check_scenarios.cjs']:
 p=root/'tests'/name;s=p.read_text(encoding='utf-8').replace('tests/evidence/mes-004/regression','tests/evidence/mes-007/regression').replace('tests/evidence/mes-004','tests/evidence/mes-007')
 p.write_text(s,encoding='utf-8')
