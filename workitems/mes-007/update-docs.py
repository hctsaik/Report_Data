from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'README.md'
s=p.read_text(encoding='utf-8').replace('給 Fab 新手的三部分互動教材','給 Fab 新手的四部分互動教材')
anchor='| http://127.0.0.1:4175/flow.html |'
lines=s.splitlines(); i=next(i for i,line in enumerate(lines) if line.startswith(anchor))
lines.insert(i+1,'| http://127.0.0.1:4175/freshness.html | 第四部分：MMDB／Giga／Native／Mart／TX、選擇原則、三個互動案例、Data Contract；6段 |')
s='\n'.join(lines)+'\n'
start=s.index('## 視覺與維護')
s=s[:start]+'''## 視覺與維護

MES-007 已實際重新製作指定15頁，以第一課 `index.html#fab` 的具體設備、局部放大、資料判讀為參考。15張桌面主插畫、14張獨立直式插畫使用內建 imagegen 製作；分流頁原圖三區直接直向排列。啟用圖片位於 `assets/mes-v3/`；未啟用草稿保留，不能當成完成圖。

`course-illustrated.js/css` 管主視覺、閱讀順序及練習展開；`course-remake.js/css` 保留精確資料對照與判斷題；`scenarios.js` 是16情境的狀態與規則。`freshness.html/js/css` 為第四部分。第一課主內容保留，增加第四課入口。

資料新鮮度依使用者提供的內部架構製作，來源原文在 `workitems/mes-007/source-freshness.txt`。Native通常<3分鐘、Mart約10分鐘是環境條件，不能取代逐表／逐欄契約。TX讀取不等於鎖定後續狀態；控制仍需核准交易執行時重驗。

新增三個案例：

- `freshness.html#ai`：10:01查同A123，切Native／Mart／TX與監看／控制用途。
- `freshness.html#history`：昨天經過DEV，不代表現在仍在DEV；切換事件涵蓋條件。
- `freshness.html#join`：整表刷新至10:01，Hold來源仍可能是09:51。

製作計畫、逐圖brief、prompt、退回理由及分項評比見 [MES-007](workitems/mes-007/PLAN.md)、[REVIEW.md](workitems/mes-007/REVIEW.md)。MES-004品質結論已撤回，保留歷史；本輪作者自評與使用者驗收分開，使用者審閱 pending。

## 驗證

需 Python Playwright、Chromium，並啟動本機4175伺服器。

```powershell
node tests/check_scenarios.cjs
python -X utf8 tests/check_courses.py
python -X utf8 tests/check_illustrated.py
python -X utf8 tests/check_illustrated_states.py
python -X utf8 tools/verify_mes007_evidence.py
```

證據在 `tests/evidence/mes-007/`。`check_illustrated` 覆蓋21頁×桌面／手機、圖片放大、三個新案例及HTTP資產；`check_illustrated_states` 擷取展開練習和全部66狀態的兩個寬度；`check_courses` 以真實操作旅程補足狀態快照。自動工具檢查行為與證據一致，不會替教學品質加分。

`workitems/mes-007/evidence-manifest.json` 綁定本轮程式、啟用圖、截圖與測試結果。修改資產後應重新擷取受影響證據。MES-004的 `check_remake.py` 及其review gate只適用被撤回的舊版本，不能作本輪通過依據。
'''
p.write_text(s,encoding='utf-8')
p=root/'AGENTS.md';s=p.read_text(encoding='utf-8')
a=s.index('目前接續 MES-006：');b=s.index('\n\n',a)
s=s[:a]+'目前版本 MES-007：使用者授權重製15頁並新增資料新鮮度。先讀 workitems/mes-007/PLAN.md、REVIEW.md 與 evidence-manifest.json。新主插畫在 assets/mes-v3；freshness.html 為第四課。MES-004品質通過已撤回，不作完成依據；MES-006為歷史比較基準。MES-007使用者審閱仍 pending。'+s[b:]
s=s.replace('宣稱 MES-004 自評完成前須執行 `python tools/validate_teaching_review.py`；失敗保持未完成。此工具只查覆蓋與證據一致，不取代逐頁閱讀、不代表使用者核准。任何共享渲染程式改動後，舊截圖須重驗，不能繼續使用過時證據。','MES-007證據檢查執行 `python tools/verify_mes007_evidence.py`；它只查範圍、資產與證據一致，不自動評品質，不代表使用者核准。舊 MES-004 validator 不適用新版本。任何共享渲染程式改動後，舊截圖須重驗，不能繼續使用過時證據。')
p.write_text(s,encoding='utf-8')
entry='''## MES-007｜十五頁插畫重製＋資料新鮮度｜2026-09-12

已依使用者授權實際製作：指定15頁的新主視覺、14張手機直式圖，以及第四部分6節與3個互動案例。使用五份共用Markdown、teaching-review-cycle、planned-code-modifier、imagegen；不是只更新計畫。參考第一課的實物→細節→資料關係，原精確資料練習改為可展開，16情境保留。

逐圖／逐頁分項、手機退回、生成內容錯誤與修正見 [MES-007 REVIEW](workitems/mes-007/REVIEW.md)。本輪紀錄不覆寫MES-004被退回事實；作者自評、工具驗證與使用者認可分開，使用者 pending。實際結果與資產雜湊見 [evidence-manifest](workitems/mes-007/evidence-manifest.json)。

學習：跨課題長prompt會污染單圖；直式重排可能改變物件數量與因果，須重新檢查；收合原圖後正文指示也必須同步重讀；功能PASS不能抵銷視覺缺口。後續每頁固定參考與責任，保存拒收稿、修正及實際渲染證據。

'''
for name in ['WORKITEMS.md','TEACHING_REVIEW_LOG.md']:
 p=root/name;s=p.read_text(encoding='utf-8');i=s.index('\n')+1;s=s[:i]+'\n'+entry+s[i:];p.write_text(s,encoding='utf-8')
for name,addition in [
 ('IMAGE_STYLE_GUIDE.md','\n\n## MES-007 製作學習\n\n單圖prompt只放該圖責任與相關識別碼；其他課題的條件列表會污染內容。改版或直式重排後，重新核對物件數量、ID、Current與箭頭因果，不能只看美感。局部文字錯誤優先精確局部修正，避免重排整圖增加新錯。實例、拒收與啟用版本見 workitems/mes-007/REVIEW.md；沿用既有量表，不另加分。\n'),
 ('TEACHING_WEBPAGE_GUIDE.md','\n\n## MES-007 實頁學習\n\n桌面圖轉手機時，完整因果與主標籤優先；跨區裁切不能只因不溢出就通過。收合資料練習後須重新讀正文指向，避免「上方四個時刻」已不存在。資料架構改為直排時，重標每條分支起點；不是只把grid改成單欄。實例與截圖見 workitems/mes-007/REVIEW.md。\n')]:
 p=root/name;p.write_text(p.read_text(encoding='utf-8')+addition,encoding='utf-8')
