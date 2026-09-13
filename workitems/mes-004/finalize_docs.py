from pathlib import Path
import json

root = Path(__file__).resolve().parents[2]
plan = root / 'workitems/mes-004/PLAN.md'
text = plan.read_text(encoding='utf-8').replace('- [ ]', '- [x]')
text += '\n## 最終檢查\n\n15 頁的桌面與手機整頁、主圖已分開檢視。port 手機主圖重新擷取並確認沒有頁首遮擋，整頁仍保留正常頁首以檢查真實版面。四組互動快照另留證據。第一次集中補 brief 的時間晚於部分首稿，詳見 BRIEFS.md，不改寫為全部先寫 brief。\n\n狀態檢查 16 情境／66 狀態／85 邊；介面回歸 54 版面／32 旅程、0 錯誤；本輪定向檢查 30 版面、132 狀態渲染、26 快照、60 練習選項及 8 份 HTTP／磁碟一致資產。防漏工具 13 項測試通過。逐頁與逐圖分項、自評扣分及截圖 hash 見 review.json；自評完成，使用者驗收 pending。\n'
plan.write_text(text, encoding='utf-8')
review = json.loads((root / 'workitems/mes-004/review.json').read_text(encoding='utf-8'))
rows = []
for page in review['pages']:
    scores = [sum(page[w][kind]['scores']) for kind in ('page', 'scene') for w in ('1440', '360')]
    rows.append('| ' + page['id'] + ' | ' + ' | '.join(map(str, scores)) + ' |')
entry = '''## MES-004 最終更新｜2026-09-12

已完成指定 15 頁重製與桌面／手機自評；使用者審閱 pending。以下取代 MES-003 的整批完成結論，歷史測試與分數僅保留原範圍。讀取五份共用 Markdown、teaching-review-cycle 與 planned-code-modifier，並實看 VisionAI DefectFill r03 參考後製作。

重製 13 個概念主圖、4 組互動快照、2 個實際狀態驅動的 lab，新增 15 個改條件判斷練習；保留全部 16 個操作情境。圖解使用精確 HTML/CSS 表達身分、槽位、歷程與路徑，本輪沒有新增 15 張 AI 點陣插畫。

### 實看後退回與修正

- 固定頁首遮住主圖截圖：另取無遮擋主圖，並保留正常整頁截圖，兩種證據分開。
- Stage 間缺方向、分支量尺位置不準、手機重工兩欄太窄：補跨階段箭頭、校正刻度與標記、手機結果改直向。
- Step 混入無關 S40，S10 已完成卻仍顯示當前 S10：改成共用 CLEAN 的 S10／R10 時點對照，完成 S10 後位置為 S20。
- 待收證據與超時條仍顯示綠色：待收用中性色／橘色，Q-time 使用 0–60 軸及 30 分鐘界線，45 分鐘顯示超時。
- 重訪情境引用不存在的 S50 Fail：依實際 visits 決定歷程說明，新增檢查防止案例事實互相污染。
- 第一個選項預設主色暗示答案：選項改同等視覺權重，操作後才顯示有條件理由。
- 擷取中途程式變動：工具實際拒絕混合版本的證據；修正完成後重新擷取，未沿用失效截圖。

### 逐頁與逐圖自評

沿用 v1.0 權重及 PLAN.md 的 Fab 適用對照。以下由實作負責者檢視後評分，並非獨立評審或真人學習成效。每項證據、保留理由、扣分、完成度、原始截圖與 hash 見 [review.json](workitems/mes-004/review.json)。不能用表中總分替代這些分項。

| 頁面 | 整頁 1440 | 整頁 360 | 主圖 1440 | 主圖 360 |
|---|---:|---:|---:|---:|
'''
entry += '\n'.join(rows)
entry += '''

### 驗證與防重犯

狀態引擎：16 情境、66 狀態、85 邊。介面回歸：54 版面、32 實際操作旅程，錯誤 0。本輪定向驗證：30 頁面／寬度組合、132 狀態渲染、26 互動快照、60 練習選項、8 份 HTTP 與磁碟一致資產。實看所有指定頁的桌面／手機整頁與主圖，以及全部 16 情境的重要狀態；不宣稱 132 個狀態各有獨立影像評分。

防漏工具 13 項測試通過：固定 15 頁、整頁與主圖分開、缺手機審查、90 分未達 >90、缺失／過期資產、失效截圖／互動快照、未解缺陷及冒充使用者驗收都會被檢查。AGENTS.md 已列為後續接續入口；指南補入本輪具體反例。工具只驗覆蓋與證據一致，不能自動判定教學品質，也不能保證使用者滿意。

證據：[定向檢查](tests/evidence/mes-004/render-check.json)、[介面回歸](tests/evidence/mes-004/regression/browser-tests.json)、[逐頁 brief](workitems/mes-004/BRIEFS.md)。首次截圖保留於 tests/evidence/mes-004/first-pass/。集中整理 brief 曾晚於部分首稿，已如實記錄；下輪先跑 preflight 再擴展製作。

第一課與三個未列入的既有插畫頁不借用本輪分數。沒有真人理解測試、實廠規則驗證或使用者核准；本機預覽已更新，未公開發布。

'''
log = root / 'TEACHING_REVIEW_LOG.md'
text = log.read_text(encoding='utf-8').replace('**當前狀態：製作中。撤回 MES-003 的整批教學完成結論。**', '**原始開工紀錄；最終狀態見本檔頂端 MES-004 更新。撤回 MES-003 的整批教學完成結論。**')
heading, rest = text.split('\n', 1)
log.write_text(heading + '\n\n' + entry + rest.lstrip('\n'), encoding='utf-8')
print('Updated PLAN and shared learning log with 15 individual score rows.')
