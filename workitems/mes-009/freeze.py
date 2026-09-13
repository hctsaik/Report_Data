from pathlib import Path
import json, hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
W=ROOT/'workitems/mes-009'
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=json.loads((W/'review.json').read_text(encoding='utf-8'))
native_visual={'qtime':[8,9,9,9,9],'future-hold':[8,9,9,8,9],'part-route':[8,9,9,8,9],'recipes':[8,9,9,9,9]}
for row in review['native_figures']:
    row['visual_scores']=native_visual[row['id']]
    row['visual_reasons']=['明亮統一配色；原生資料圖的造形表現較插畫保守。','指定互動責任與所有狀態完整。','精確欄位、條件與示例身分一致。','主要差異在同一操作區可比；長文另列。','標題、物件、輸出及黃色結論有固定閱讀順序。']
(W/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
p=W/'REVIEW.md'
t=p.read_text(encoding='utf-8')
if '原生圖完成度補記' not in t:
    t+='\n## 原生圖完成度補記\n\n'
    for name,scores in native_visual.items():t+=f'- {name}：美感／完整／專業／密度／層級 = {scores}。亮色與層級一致，精確操作完整；造形較插畫保守。具體理由見 review.json。\n'
    p.write_text(t,encoding='utf-8')
if '54 個既有章節導航版面' not in t:
    t+='\n新增入口另驗證 18 節 × 3 尺寸 = 54 個既有章節導航版面。此範圍只驗新連結與頁首布局，不重新宣稱舊章節內容已獲使用者驗收。\n'
    p.write_text(t,encoding='utf-8')
old=json.loads((ROOT/'workitems/mes-008/evidence-manifest.json').read_text(encoding='utf-8'))
unchanged={**old['active_assets'],**old['unchanged_other_courses']}
for name in ['operations.html','flow.html']:
    # Explicit scope change: only add the reviewed extension script to these entry files.
    expected=unchanged.pop(name)
    assert digest(W/'baseline'/name)==expected,name+' baseline differs from MES-008'
    before=(W/'baseline'/name).read_text(encoding='utf-8')
    after=(ROOT/name).read_text(encoding='utf-8')
    assert after.replace('<script src="course-extension.js" defer></script>','')==before,name+' unexpected entry edits'
for name,value in unchanged.items():assert digest(ROOT/name)==value,f'Previously unchanged asset changed: {name}'
validation=json.loads((ROOT/'tests/evidence/mes-009/results.json').read_text(encoding='utf-8'))
active=list(validation['files'])+['flow.html','operations.html']
measurements={}
for item in review['images']:
    name=item['path']
    im=Image.open(ROOT/name).convert('RGB');width,height=im.size
    assert abs(width/height-16/9)<.03
    thumb=im.resize((160,90))
    pixels=list(thumb.getdata())
    brightness=sum(sum(p)/3 for p in pixels)/len(pixels)
    bottom=list(thumb.crop((0,79,160,90)).getdata())
    yellow=sum(r>210 and g>200 and 90<b<245 and r>b+8 for r,g,b in bottom)/len(bottom)
    assert brightness>145,(name,brightness)
    assert yellow>.25,(name,yellow)
    measurements[name]={'size':[width,height],'mean_brightness':round(brightness,2),'bottom_yellow_fraction':round(yellow,3)}
documents=['AGENTS.md','WORKITEMS.md','README.md','TEACHING_REVIEW_LOG.md','IMAGE_STYLE_GUIDE.md','TEACHING_WEBPAGE_GUIDE.md','tests/check_advanced.py','tests/check_advanced_links.py','tools/verify_mes009_evidence.py','openspec/changes/mes-advanced-concepts/spec.md']+[str(p.relative_to(ROOT)).replace('\\','/') for p in W.glob('*') if p.suffix in ['.md','.json','.py'] and p.name!='evidence-manifest.json']
evidence={str(p.relative_to(ROOT)).replace('\\','/'):digest(p) for p in (ROOT/'tests/evidence/mes-009').rglob('*') if p.is_file()}
baseline={str(p.relative_to(ROOT)).replace('\\','/'):digest(p) for p in (W/'baseline').glob('*') if p.is_file()}
drafts={str(p.relative_to(ROOT)).replace('\\','/'):digest(p) for p in (ROOT/'assets/mes-009').glob('*draft*.png')}
manifest={'round':'MES-009','user_acceptance':'pending','internal_dictionary_confirmation':'pending','active':{name:digest(ROOT/name) for name in active},'documents':{name:digest(ROOT/name) for name in documents},'evidence':evidence,'baseline':baseline,'rejected_drafts':drafts,'unchanged_from_mes008':unchanged,'image_measurements':measurements,'validation_count':validation['count']}
(W/'evidence-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Frozen:',len(active),'active files,',len(evidence),'evidence files,',len(unchanged),'prior assets unchanged.')
