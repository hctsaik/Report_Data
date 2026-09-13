"""Project preflight coverage; not a substitute for reading the actual style reference."""
from pathlib import Path
from validate_teaching_review import REQUIRED
ROOT=Path(__file__).resolve().parents[1]
brief=(ROOT/'workitems/mes-004/BRIEFS.md').read_text(encoding='utf-8')
missing=[rid for rid in REQUIRED if f'| {rid} |' not in brief]
assert not missing,missing
for file in ['CLAUDE.md','IMAGE_STYLE_GUIDE.md','TEACHING_WEBPAGE_GUIDE.md','TEACHING_SCORING_RUBRIC.md','TEACHING_REVIEW_LOG.md','workitems/mes-003/style-reference.png','workitems/mes-004/PLAN.md']:
    assert (ROOT/file).is_file(),file
assert 'user_acceptance' in (ROOT/'tools/validate_teaching_review.py').read_text(encoding='utf-8')
print('PASS: 15 page briefs, reference and five intent documents present. Visual review remains separate.')
