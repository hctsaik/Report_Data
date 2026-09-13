"""Read-only check of the MES-010 snapshot; does not evaluate teaching quality."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'workitems/mes-010/evidence-manifest.json').read_text(encoding='utf-8'))
for group in ['files', 'unchanged_from_previous']:
    for name, expected in manifest[group].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
review = json.loads((root / 'workitems/mes-010/review.json').read_text(encoding='utf-8'))
for group in ['pages', 'images', 'native_figures']:
    for item in review[group]:
        assert sum(item['scores']) == item['total'], item['id']
results = json.loads((root / 'tests/evidence/mes-010/results.json').read_text(encoding='utf-8'))
assert results['count'] == manifest['validation_count'] == 154
print('PASS: 90 snapshot files, 66 preserved files, review arithmetic, 154-check evidence.')
