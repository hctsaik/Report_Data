"""Regression cases for the repeated scope/evidence failure, without changing real files."""
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from validate_teaching_review import validate

class ReviewGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review=json.loads((ROOT/'workitems/mes-004/review.json').read_text(encoding='utf-8'))
        cls.render=json.loads((ROOT/'tests/evidence/mes-004/render-check.json').read_text(encoding='utf-8'))

    def test_current_evidence(self):
        self.assertEqual(validate(self.review,self.render),[])

    def test_missing_page(self):
        r=copy.deepcopy(self.review);r['pages'].pop()
        self.assertTrue(validate(r,self.render))

    def test_duplicate_page_cannot_hide_missing_page(self):
        r=copy.deepcopy(self.review);r['pages'][-1]=copy.deepcopy(r['pages'][0])
        self.assertTrue(validate(r,self.render))

    def test_image_scores_cannot_replace_page_scores(self):
        r=copy.deepcopy(self.review);del r['pages'][0]['1440']['page']
        self.assertTrue(validate(r,self.render))

    def test_ninety_is_not_above_ninety(self):
        r=copy.deepcopy(self.review);r['pages'][0]['1440']['page']['scores']=[18,18,18,18,9,9]
        self.assertTrue(validate(r,self.render))

    def test_missing_mobile_review(self):
        r=copy.deepcopy(self.review);del r['pages'][0]['360']
        self.assertTrue(validate(r,self.render))

    def test_stale_asset(self):
        r=copy.deepcopy(self.render);r['assets']['course-remake.js']='old'
        self.assertTrue(validate(self.review,r))

    def test_missing_asset_manifest(self):
        r=copy.deepcopy(self.render);r['assets']={}
        self.assertTrue(validate(self.review,r))

    def test_review_bound_to_another_screenshot(self):
        r=copy.deepcopy(self.review);r['pages'][0]['360']['scene']['reviewed_hash']='another-image'
        self.assertTrue(validate(r,self.render))

    def test_unresolved_visual_defect(self):
        r=copy.deepcopy(self.review);r['pages'][0]['1440']['scene']['open_defects']=['unreadable evidence']
        self.assertTrue(validate(r,self.render))

    def test_missing_scenario_state(self):
        r=copy.deepcopy(self.render);r['states'].pop()
        self.assertTrue(validate(self.review,r))

    def test_self_review_is_not_user_acceptance(self):
        r=copy.deepcopy(self.review);r['user_acceptance']='accepted'
        self.assertTrue(validate(r,self.render))

    def test_stale_interactive_frame(self):
        r=copy.deepcopy(self.review)
        row=next(x for x in r['pages'] if x['id']=='operations/chamber')
        row['360']['scene']['additional_frames'][0]['sha256']='old-frame'
        self.assertTrue(validate(r,self.render))

if __name__=='__main__': unittest.main()
