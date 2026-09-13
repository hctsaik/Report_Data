# MES-003｜第二部分重做、第三部分 Flow 深入課

授權：2026-09-12，使用者要求第二部分全部重做，新增深入 Flow／Stage／Step／Lot 套用課程，一次完成更多情境。基線保存在 baseline/。既有視覺被使用者否定，不當作認可母版。

## 計畫

- [x] 依五份 Markdown 寫內容契約、逐圖 brief，實看參考後先產代表圖。
- [x] 重做第二課：設備內外、搬送、配方、加工與完成確認；6 個現場情境。
- [x] 第三課：Flow 定義／版本、Stage 分組、Step occurrence、Lot 綁定與位置、過站歷程、分支／重工／拆合批／改版／Q-time；10 個流程情境。
- [x] 桌面／手機實看、情境狀態與不變量測試、第一課回歸、HTTP 新資產核對。
- [x] 更新 README、WORKITEMS、共用 log 與實際審閱結果，交付兩課。

## 教學契約

本課為簡化 MES 教學模型，不宣称對應未提供的原始 ER schema。Flow/Route 指版本化流程定義；Stage 是本課對有共同目的的 Step 分組；Step occurrence 是某版本流程中的一次作業位置，不等於 Recipe 內部步驟，也不等於某台設備。各 MES 命名、Stage 執行意義、過站交易邊界依實作而異。

同案例：產品 P-DEMO，Flow F-DEMO v1，3 Stage／6 Step：A 準備 S10 清洗→S20 成膜；B 圖形 S30 微影→S40 蝕刻；C 確認 S50 量測→S60 結案。只示範一段教學旅程，非完整晶片配方。Lot L023 含 W06/W07/W08；F012 是位置載具，不決定流程。第二課以 S40 為現場加工背景。

Flow 定義不因一批過站而改變；Lot 的 current occurrence／執行狀態／歷程會變。Track-out 在本例包括必填資料驗證，完成後可推進；若品質待判先停留，不能把機台 Done 當下一站已可開始。例外保留原始失敗歷程；重工是批准的支線加新 visit；拆批保留晶圓集合且不複製，合批須共同 Flow/version/current occurrence/product/可合併狀態。版本升級只改授權實例，v2 發布不靜默改在製 Lot。

來源：Critical Manufacturing semiconductor 頁（路徑追蹤、載具、recipe、Track-in/out、split/merge/rework、PQT）、IBM SiView（物件與執行管理）、Brooks／Daifuku（設備傳送／AMHS）。所有 ID、數值、允許的例外與 Q-time 門檻為教學設定。

## 視覺與評價

適用 CLAUDE.md、IMAGE_STYLE_GUIDE.md（11.11 最新偏好／12 閉環）、TEACHING_WEBPAGE_GUIDE.md、TEACHING_SCORING_RUBRIC.md v1.0、TEACHING_REVIEW_LOG.md。模型選型專屬整頁配分不冒充 Fab 得分；逐圖以 v1.0 第3節核對，工具測試不當品質分數。

已實看母版：visionAI/teaching-images/vision-ai-model-selection/docs/_course_content/generated-concepts/defectfill/wi026-defectfill-c1-r03-desktop.png。沿用可辨識金屬物件、柔和立體、清楚單一路徑、具名局部與淡黃結論；不沿用 DefectFill 內容。舊 tmp/f02-series 圖只作歷史，非本輪母版。

設備插畫用內建 imagegen；可驗證的 Flow／事件／位置用原生圖結合插畫，避免文字卡冒充場景。新頁採大幅主圖、就地說明、可折疊工程細節；手機主線有分段文字與可放大圖。下列每圖皆為 AI 教學示意，非實機照片、比例圖或量產配方。

| 圖 | 核心理解／工作問題 | 輸入與改變／可見證據 | 構圖、關係、下一步 | 字詞／結論／風險 |
|---|---|---|---|---|
| equipment-v2 | 載具停在設備外，單片晶圓經交接才到製程腔體 | 同一 FOUP、水平晶圓、傳送手臂、load lock 與真空 chamber 剖面；主圖+局部路徑 | C，3區 FOUP/大氣側交接/真空製程，箭頭為傳送方向；確認三個角色 | FOUP/Load Port/Transfer/Load lock/Chamber；結論「載具停靠，晶圓進入製程腔體。」；不把FOUP畫進chamber、不同壓力區分清 |
| transport-v2 | 搬送變的是載具位置，未等於加工 | 同一藍色 FOUP 依時刻位於 Stocker、OHT、Load Port；三個時刻分段 | C，左至右3節點；時序箭頭非同時3載具；接著檢查而非開工 | Stocker/OHT/Load Port；「到站只是到位，還要完成開工確認。」；不可在OHT外露晶圓 |
| flow-v2 | 同一定義分成 Stage，Lot 保有自己的流程位置 | 3色stage各2個具象製程，L023指向蝕刻、L024指向清洗，兩個位置不同 | C，3段6站左至右；箭頭=先後、Lot指標=實例位置；看現在站與下一站 | A/B/C、S10/S20/S30/S40/S50/S60；「Flow 定義路徑，Lot 記錄走到哪裡。」；不畫成物理廠房位置，不暗示Stage只有兩站 |

生成前已完成上述人工 preflight；本資料夾無 tools/validate_teaching_preflight.py，不宣稱該工具通過。每圖先原圖實看，再檢查實際頁面尺寸。Prompt、產物路徑與審閱追加本目錄，使用者驗收保持 pending。
