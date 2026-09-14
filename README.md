# MES Learning Lab

**線上教學網站：[https://hctsaik.github.io/Report_Data/](https://hctsaik.github.io/Report_Data/)**

點上方網址即可開啟 GitHub Pages 教學網站。

最新：整合 ER 支援選主詞後重新展開關聯小圖（Lot／FOUP／EQP／Flow／Recipe），可點小圖改換主詞。入口 http://127.0.0.1:4175/er-atlas.html?view=original 。[MES-017 紀錄](workitems/mes-017/REVIEW.md)。

本輪新增：[CW](support.html#cw) · [Sub Route／追加量測](support.html#subroute) · [Move](support.html#move) · [MON／PM／EMS](support.html#monitor)。檢查紀錄：[MES-010 REVIEW](workitems/mes-010/REVIEW.md)。

給 Fab 新手的四部分互動教材，加上時間、路徑與配方延伸章。純 HTML/CSS/JavaScript，情境只在瀏覽器內模擬。

## 開啟

可直接開啟 index.html，或在此目錄執行 `python -m http.server 4175 --bind 127.0.0.1`。

| 入口 | 內容 |
|---|---|
| http://127.0.0.1:4175/integrated-map.html | 整合 ER：121 實體／關係節點、128 條線、色彩圖例、沿線閱讀與五個跨圖題目 |
| http://127.0.0.1:4175/data-map.html#2676 | ER 讀圖：七張原圖、14個案例；現場物件、作業與資料意義的對照 |
| http://127.0.0.1:4175/index.html | 第一部分：Fab、Wafer、FOUP、Slot、Lot |
| http://127.0.0.1:4175/operations.html | 第二部分全面重做：設備交接、搬送、身分、配方、逐片加工、Hold、MES完成交易；8段 |
| http://127.0.0.1:4175/flow.html | 第三部分：Flow、Stage、Step、Lot套用、過站、分流、重工、拆合批、改版；10段 |
| http://127.0.0.1:4175/freshness.html | 第四部分：MMDB／Giga／Native／Mart／TX、選擇原則、三個互動案例、Data Contract；6段 |

章節支援 #stage、#step、#lot-flow 等連結。情境支援 `#lab?case=情境ID`；第二部分舊的 #arrival、#run、#hold、#reconcile 連結仍可使用。

## 16個情境

| 課程 | ID | 情境 |
|---|---|---|
| 第二部分 | arrival | 錯誤Port／正確派送／到站 |
| 第二部分 | reconcile | 片數相同但錯片／缺讀值／重讀 |
| 第二部分 | recipe | 同名舊版配方／不合格設備 |
| 第二部分 | run | 三片逐片加工／來源槽清空／資料延遲／MES過站 |
| 第二部分 | fault | W07加工中故障／安全取回／未完成處置 |
| 第二部分 | hold | 兩個Hold原因／分別解除 |
| 第三部分 | bind | 依產品與核准版本套用Flow |
| 第三部分 | normal | S10到S60完整六站旅程 |
| 第三部分 | branch | 缺資料／合格／不合格分流 |
| 第三部分 | rework | 重工／新visit／再次失敗與次數限制 |
| 第三部分 | split | 3片拆成2+1／進度對齊／合批與譜系 |
| 第三部分 | version | 發布v2／新批套用／在製批遷移到S45 |
| 第三部分 | qtime | 20分鐘開工／45分鐘超時／禁止歸零 |
| 第三部分 | skip | 急單不能省略必要量測 |
| 第三部分 | revisit | 同為CLEAN，S10與R10不能共用完成紀錄 |
| 第三部分 | dispatch | 先篩可執行資格，再排優先權 |

每個情境有獨立起始條件、狀態、事件紀錄與重設；切換保留各自進度，重新載入則重新開始。沒有存取真實MES。

## 教學模型

產品P-DEMO、Flow F-DEMO v1、3個Stage與6個Step：A準備（S10清洗、S20成膜）、B圖形（S30微影、S40蝕刻）、C確認（S50量測、S60結案）。不是完整晶片製程。Stage分組、交易邊界、重工、合批、遷移與30分鐘Q-time是明示教學設定，各MES命名與實作不同。

Flow定義可共用，Lot位置／狀態／歷程獨立；FOUP是載具，不決定Flow。原始ER完整schema未提供，工程欄位為概念示例。廠商來源在網頁底部，一般能力不代表本课規則是實廠標準。

## 視覺與維護

MES-008 已重製資料新鮮度六節，啟用12張桌面／手機圖位於 `assets/freshness-v2/`。每節有主圖、互動與換條件自測；契約頁可檢视逐欄時間及下載示例JSON。製作前brief、退回稿與逐頁評比見 [MES-008 PLAN](workitems/mes-008/PLAN.md)、[REVIEW](workitems/mes-008/REVIEW.md)、[實圖比較](workitems/mes-008/review.html)。MES-007新鮮度高分已撤回；新版作者評比與使用者認可分開，使用者審閱仍 pending。


MES-007 已實際重新製作指定15頁，以第一課 `index.html#fab` 的具體設備、局部放大、資料判讀為參考。15張桌面主插畫、14張獨立直式插畫使用內建 imagegen 製作；分流頁原圖三區直接直向排列。啟用圖片位於 `assets/mes-v3/`；未啟用草稿保留，不能當成完成圖。

`course-illustrated.js/css` 管主視覺、閱讀順序及練習展開；`course-remake.js/css` 保留精確資料對照與判斷題；`scenarios.js` 是16情境的狀態與規則。第四部分入口是 `freshness.html`；`freshness-v2.js/css` 管六節內容與互動，`freshness.js` 管導覽與時間狀態。舊 `freshness.css` 不再被頁面引用。第一課主內容保留，增加第四課入口。

資料新鮮度依使用者提供的內部架構製作，來源原文在 `workitems/mes-007/source-freshness.txt`。Native通常<3分鐘、Mart約10分鐘是環境條件，不能取代逐表／逐欄契約。TX讀取不等於鎖定後續狀態；控制仍需核准交易執行時重驗。

新增三個案例：

- `freshness.html#ai`：10:01查同A123，切Native／Mart／TX與監看／控制用途。
- `freshness.html#history`：昨天經過DEV，不代表現在仍在DEV；切換事件涵蓋條件。
- `freshness.html#join`：整表刷新至10:01，Hold來源仍可能是09:51。

製作計畫、逐圖brief、prompt、退回理由及分項評比見 [MES-007](workitems/mes-007/PLAN.md)、[REVIEW.md](workitems/mes-007/REVIEW.md)。MES-004品質結論已撤回，保留歷史；本輪作者自評與使用者驗收分開，使用者審閱 pending。

## 驗證

目前資料新鮮度：`python tests/check_freshness_v2.py`（18版面、190操作），`python tools/verify_mes008_evidence.py`（資產／證據／評分加總一致，無自動品質判斷）。MES-007 manifest為歷史版本，新freshness檔案已由MES-008取代；不要重寫歷史hash讓舊檢查假裝適用。


需 Python Playwright、Chromium，並啟動本機4175伺服器。

```powershell
node tests/check_scenarios.cjs
python -X utf8 tests/check_courses.py
python -X utf8 tests/check_freshness_v2.py
python -X utf8 tools/verify_mes008_evidence.py
```

目前新鮮度證據在 `tests/evidence/mes-008/`。MES-007的 `check_illustrated.py` 與 `verify_mes007_evidence.py` 綁定已取代的新鮮度版面，不作目前驗收，也不要重跑覆寫其歷史證據。`check_illustrated_states.py` 的66狀態證據仍保留在MES-007；這輪以hash確認40份非新鮮度資產未變。自動工具檢查行為與證據一致，不會替教學品質加分。

`workitems/mes-008/evidence-manifest.json` 綁定目前新鮮度程式、啟用圖、截圖與測試結果。MES-007 manifest為歷史版本，舊REVIEW原文另保存在MES-008 baseline。修改資產後應重新擷取受影響證據。MES-004的 `check_remake.py` 及其review gate只適用被撤回的舊版本，不能作本輪通過依據。

## MES-009：新增名詞與 Flow 候選

- [時間、路徑與配方](http://127.0.0.1:4175/advanced.html#qtime)：QTime、Future Hold、Part、RouteId、LR、ER、Physical Recipe。
- [Flow 四種教法比較](http://127.0.0.1:4175/advanced.html#flow-versions)：原版保留；A 層級放大、B 立體走站、C 定義與進度對照。本機記錄偏好不替換正式課程。
- [講解稿](workitems/mes-009/CONTENT.md)、[逐圖評比](workitems/mes-009/REVIEW.md)、[製作與來源](workitems/mes-009/PLAN.md)。
- 驗證：`python tests/check_advanced.py`。Part 及 LR／ER 的內部資料模型仍待確認，頁面明示教學假設。
# 最新入口與版本

目前版本：MES-055。從 [learning.html](learning.html) 進入十個學習單元，也可使用現場任務、主題索引及完整 ER。基礎 FOUP／Slot／Lot、裝載與七個主題圖文已更新，詳見 [MES-055 修改及驗證紀錄](workitems/mes-055/REVIEW.md)。以下保留各階段教材與維護資訊。

請在儲存庫根目錄執行 `python -m http.server 4175 --bind 127.0.0.1`，再開啟 `http://127.0.0.1:4175/learning.html`。網站需透過 HTTP 載入 ER JSON，不建議直接雙擊 HTML。

Git 保留網站資產、測試程式、稽核 JSON 與審查文件；可重產的 `tests/evidence` 截圖及 Python 快取不納入版本控制。重新驗證本輪：`python workitems/mes-055/check.py`（須先啟動上述 HTTP 伺服器並安裝 Playwright）。
