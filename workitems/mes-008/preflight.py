from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=(r/'workitems/mes-008/PLAN.md').read_text(encoding='utf-8')
for f in ['CLAUDE.md','IMAGE_STYLE_GUIDE.md','TEACHING_WEBPAGE_GUIDE.md','TEACHING_SCORING_RUBRIC.md','TEACHING_REVIEW_LOG.md','examples/fab-physical-data-v01.png','workitems/mes-007/source-freshness.txt']:
    assert (r/f).is_file(),f
for s in ['ai / D / 3','architecture / C / 3','decision / D / 3','history / D / 3','join / C / 3','contract / C / 3','user_acceptance: pending','#FFF4CC']:
    assert s in p,s
print('PASS: six briefs, source packet, reference and five guides present; no visual approval inferred.')
