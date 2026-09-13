import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8')
def prepend(path, text):
    p = ROOT / path
    write(path, text + '\n\n' + p.read_text(encoding='utf-8'))
def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

page_data = {
 'cw': ([19,19,19,19,9,8], ['三種用途對應量測、補位與調整工作。','材料用途和 MON 作業分開；三者可重疊。','各頁籤均有接手規範與工作結果。','三種用途同座標比較，交代不可任意互換。','桌面主圖與手機直向原生图可讀；手機三頁籤占較多高度。','seasoning 後粒子驗證題能檢查用途，但選項取捨較簡單。']),
 'subroute': ([19,19,20,18,9,8], ['L023 從 S50 追加量測再返回。','主 Route、目前 Route 和返回錨點分開保留。','可試錯返 S60，回 S50 後仍未自動完成。','比較切 Route 與過站事件；未涵蓋巢狀子路徑。','同一 Lot 與原站位置貫穿圖和互動；手機操作記錄較長。','原站完成條件題可檢查誤解，未要求自行設計返回規則。']),
 'move': ([20,19,20,19,9,8], ['三筆同 Lot 事件含一次重工，可逐筆追算。','事件數、不同 Lot、晶圓數和搬運數有具體區分。','新增重工與重送按鈕呈現不同結果，重送不重計。','同一事件集比較 Move 與 distinct Lot；撤銷沖銷依廠內規則。','整表統計箭頭已重製；手機逐筆加一清晰。','新情境含重工及重送，仍是兩選一入門題。']),
 'monitor': ([19,19,19,19,9,8], ['PM 已完、MON 逾期、EMS 擋生產構成具體困境。','工作完成、結果接受與 EMS 更新分開展示。','每階段可檢查生產條件，其他 Hold 仍獨立阻擋。','保養與監控的責任比較，未捏造每日固定時數。','桌面並列、手機直排，主圖原因對應阻擋。','補做但仍阻擋需查結果與更新；未使用真實 EMS 操作。'])
}
image_data = {
 'cw': ([24,24,19,18,9], ['同一 CW 大括號下可見探頭、補位片和腔壁。','三個用途畫出不同作用位置，非只換標題。','量測結果／補位／調整與結論一致。','三欄可平行比較；監控結果局部仍偏密。','蓝色是角色標示；設備為概念示意，不作實機結構證據。']),
 'subroute': ([24,24,19,19,9], ['同 L023 與 S50 左右重現，中段是追加量測。','去程與回程保留 F-DEMO v1/S50 錨點。','圖內寫明返回不等於過站完成。','三幕有方向與作業單；中間錨點重複但有助返回定位。','Route、Lot、Step 一致；量測頭屬示意。']),
 'move': ([25,24,20,18,9], ['三筆事件各具 ID，重工橘色突出。','整表括號通往 1+1+1=3；同一 Lot 保留。','並列 3 Move 與 1 不同 Lot，可直接追算。','大型數字易判讀；左側載具占比略大。','移除無關藍色晶圓，獨立作業單避免把 Lot 等同載具。']),
 'monitor': ([24,24,19,18,9], ['PM 綠色完成與 MON 橘色逾期、EMS 紅色阻擋可對照。','只有逾期檢查連向阻擋，未畫 PM 自動解鎖。','原因與停止手勢清楚，補做 MON 不在禁止範圍。','三欄有主從；中間平板仍以文字負責有效性。','移除未執行假欄位；PM 清單是示意，不代表特定機台規程。'])
}
native_data = {
 'cw': ([24,24,19,18,9], '三種頁籤各有探頭／補位／腔壁作用位置；手機先選用途再讀行動，頁籤區較高。'),
 'subroute': ([24,25,20,18,9], '目前 Route 隨操作變色、錨點不變、拒絕錯返、返回仍未完成；手機事件記錄較長。'),
 'move': ([25,25,20,18,9], '每筆事件 +1、重工獨立色，重送與新事件導致不同結果；原生圖以事件表為核心而非實物。'),
 'monitor': ([24,24,20,18,9], '三個獨立狀態隨操作更新，PM 與其他 Hold 可獨立阻擋；有效性是教學流程，不是 EMS 實際 API。')
}
review = {'round':'MES-010','rubric':'1.0','user_acceptance':'pending','learner_study':'not performed','scoring_scope':'作者對示例的自評；不是廠內系統認證。固定權重沿用，模型意義對應 MES 機制，比較對應工作責任與取捨。','pages':[],'images':[],'native_figures':[]}
for key,(scores,evidence) in page_data.items():
    review['pages'].append(dict(id=key,scores=scores,total=sum(scores),evidence=evidence,screenshots=[f'tests/evidence/mes-010/{key}-{w}.png' for w in [1440,800,360]],veto=[]))
for key,(scores,evidence) in image_data.items():
    review['images'].append(dict(id=key,path=f'assets/mes-010/{key}.png',scores=scores,total=sum(scores),evidence=evidence,visual_scores=[9,9,9,8,9],visual_evidence=['明亮白藍場景與金屬材質完整。','物件、作用、結果與結論均在圖內。','身分及因果可核對；實機結構不在主張範圍。','三欄資訊集中；細節密度是扣分處。','藍標題、結果色及單一黃色結論建立層級。'],scope='原圖與桌面顯示；手機另評原生主線，非以缩圖冒充可讀。',veto=[]))
for key,(scores,reason) in native_data.items():
    review['native_figures'].append(dict(id=key,scores=scores,total=sum(scores),evidence=reason,visual_scores=[8,9,9,8,9],visual_evidence=['乾淨的白藍色與一致邊框，實物細節不及插畫。','案例狀態、行動與結果齊全。','資料標籤與操作責任清晰。','手機留白和直排增加頁長。','當前狀態強調、操作與結論分層。'],scope='桌面及360px手機；CW 包括三個頁籤。',veto=[]))
write('workitems/mes-010/review.json',json.dumps(review,ensure_ascii=False,indent=2)+'\n')
lines=['# MES-010 成品檢視與固定量表評比','', '量表 v1.0；作者自評，使用者驗收 pending。沒有真人學習成效測試。廠內分類與行為採使用者六點補充及「加量＝追加量測」回答；操作名稱、事件 ID 與機台外形均為教學示例。','', '## 實際修正','', '- Move 首稿錯把單筆事件指向整體統計；重畫為整表括號，再導向 3 Move／1 Lot。移除從 CW 參考沿用的藍色片。','- MON 首稿自行生成四個「未執行」欄位；逾期不代表沒做過。重畫為有效性與 EMS 阻擋，沒有設定 24 小時或自動解除。','- Sub Route 依最新回答明確標示追加量測；返回 F-DEMO v1/S50，未自動跳 S60。','', '## 分數與範圍','', '分項、正面證據與扣分理由見 [review.json](review.json)。頁面權重 20/20/20/20/10/10；圖片與原生圖 25/25/20/20/10，未調權重。','', '| 單元 | 頁面 | 情境插畫 | 原生互動圖 |','|---|---:|---:|---:|']
for key in page_data:
    lines.append(f'| {key} | {sum(page_data[key][0])} | {sum(image_data[key][0])} | {sum(native_data[key][0])} |')
lines += ['', '這些分數不代表使用者已認可。插畫與原生圖分開評：手機以直排互動主線閱讀，完整插畫為可展開的補充。未將桌面插畫得分套到手機縮圖。','', '## 成品證據','', '- 已逐張檢視四張啟用插畫、四頁桌面主線、手機原生圖與 Sub Route 返回畫面。CW 三種用途的原生圖也分別檢視。','- `tests/check_support.py`：154 項通過；1440／800／360 寬度、導航、放大與 Escape、答案、Sub Route 去回與錯返、Move 重工與重送、MON 多階段及其他阻擋條件。','- 既有 advanced 五節新增入口在三種寬度檢查；九個 HTTP 檔案與磁碟位元組相同；無 JavaScript 錯誤。','- 截圖及逐項結果位於 `tests/evidence/mes-010`。800px 已做工具檢查與保存，但不宣稱每一張800px截圖都作獨立人工評分。','- 舊版主體沿用 hash 核對；advanced.html 只追加新單元連結。旧 manifest 保留為歷史快照。','', '## 剩餘界線','', 'AAA 正式用語、AVL／Eff／Lost／Up 定義未經確認，未新增其公式或狀態圖。Daily MON 計時起點、週期與解除交易依廠內規範，互動只說明責任分離。Part／LR／ER 先前未確認事項仍維持待確認。','', '## 本輪停止原因','', '已完成本輪已確認的四個單元、重製缺陷圖及實際檢查；目前無已辨識的阻擋缺陷。使用者後續若指出理解或畫面缺口，重開該版本評比，不能用自評高分反駁。']
write('workitems/mes-010/REVIEW.md','\n'.join(lines)+'\n')
pointer='# 最新接續：MES-010\n\n已新增 support.html 四節：CW、Sub Route（加量＝追加量測，回原站）、Move（Lot 過站事件，重工計入）、MON／PM／Daily MON／EMS。先讀 workitems/mes-010/CONTENT.md、PLAN.md、REVIEW.md。驗證 python tests/check_support.py：154項通過。使用者驗收 pending；AAA 及 AVL／Eff／Lost／Up 定義未確認。advanced.html 僅新增入口，其餘既有前端以歷史 hash 核對。舊 manifest 不再代表本輪修改後的共用文件，不覆寫歷史證據。'
prepend('AGENTS.md',pointer)
prepend('WORKITEMS.md',pointer)
prepend('TEACHING_REVIEW_LOG.md','# MES-010｜四個新單元完成，使用者審閱 pending\n\n使用 teaching-review-cycle 與專案 Markdown。六點補充全部採納；加量已確認為追加量測。CW 先做單圖原型，再擴展；Move 整表統計箭頭與 MON 逾期誤畫未執行各重製一次。分項、截圖、扣分與未評範圍見 workitems/mes-010/REVIEW.md、review.json；功能154項通過不當作視覺得分證據。\n\n學習寫回：IMAGE_STYLE_GUIDE 的有效性與事件集合規則；TEACHING_WEBPAGE_GUIDE 的材料用途／作業／狀態分離。下輪先查這些關係再產圖，逐圖追箭頭及畫面額外生成的小字。以下 MES-010 進行中記錄保留為歷史，由本條取代其進度。')
prepend('IMAGE_STYLE_GUIDE.md','MES-010補充：畫「逾期」時只能呈現有效性失效，不能自行補成「未執行」。統計圖的箭頭起點必須覆蓋實際計算的事件集合，不能由單筆指向整體結果。參考圖沿用的顏色與物件角色須逐一清除或重新說明，避免上一主題的標記混入新案例。')
prepend('TEACHING_WEBPAGE_GUIDE.md','MES-010補充：材料用途、作業類型、有效性與放行條件分開教；材料存在或工作完成不能代替有效結果。路徑切換、返回原站與過站完成分別呈現，不由畫面的來回箭頭推算事件數。互動狀態應同時保留物件身分與返回錨點，以實測錯誤返回及重複事件驗證。')
prepend('README.md','本輪新增：[CW](support.html#cw) · [Sub Route／追加量測](support.html#subroute) · [Move](support.html#move) · [MON／PM／EMS](support.html#monitor)。檢查紀錄：[MES-010 REVIEW](workitems/mes-010/REVIEW.md)。')
old=json.loads((ROOT/'workitems/mes-009/evidence-manifest.json').read_text(encoding='utf-8'))
unchanged={**old['active'],**old['unchanged_from_mes008']}
unchanged.pop('advanced.html',None)
for p,h in unchanged.items():
    assert sha(p)==h,p
baseline='workitems/mes-010/baseline/advanced.html'
assert sha(baseline)==old['active']['advanced.html']
link='<a href="support.html#cw">CW 與設備監控</a>'
current=(ROOT/'advanced.html').read_text(encoding='utf-8')
assert current.count(link)==1
assert current.replace(link,'').strip()==(ROOT/baseline).read_text(encoding='utf-8').strip()
files=['support.html','support.css','support.js','advanced.html','advanced.css','tests/check_support.py','AGENTS.md','WORKITEMS.md','README.md','TEACHING_REVIEW_LOG.md','IMAGE_STYLE_GUIDE.md','TEACHING_WEBPAGE_GUIDE.md','openspec/changes/cw-subroute-monitor/spec.md']
for directory in ['workitems/mes-010','tests/evidence/mes-010','assets/mes-010']:
    files.extend(p.relative_to(ROOT).as_posix() for p in (ROOT/directory).rglob('*') if p.is_file() and p.name!='evidence-manifest.json')
manifest={'round':'MES-010','user_acceptance':'pending','validation_count':154,'files':{p:sha(p) for p in sorted(set(files))},'unchanged_from_previous':unchanged,'advanced_change':'Only support.html#cw header link appended; removing exact link restores baseline text.'}
write('workitems/mes-010/evidence-manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Review and evidence frozen:',len(manifest['files']),'files;',len(unchanged),'prior files unchanged')
