# MES-054 全站課程架構已實作

入口learning.html；index無錨點轉總覽，旧教材錨點相容。共用catalog十單元/三路線、五現場任務、獨立topic與ER共用定義、統一site-shell導航/來源返回/前後教材/進度。讀workitems/mes-054/REVIEW.md及TEST-REPORT.md。檢查workitems/mes-054/check.py、check_lab.py、check_journeys.py、check_topics.py、check_persistence.py。原ER保留，FRPORT_UDATA不回課綱，Stream歷史註記。244頁面操作、132情境狀態、92主題視圖已驗證；真人學習效果與使用者審閱pending。一次性integrate/refine/extract/finish腳本不重跑。

# MES-053 全站架構四角色審查

使用者要求 Multi-agent 以新手工程師、Data Scientist、現場工程師、導師完整審查網站並寫Markdown。已完成，主文件 workitems/mes-053/DESIGN-RECOMMENDATIONS.md，逐項映射 CONTENT-MAP.md，四份ROLE報告及REVIEW.md。十入口雙尺寸載入，代表首屏實看；課末循環與ER返回往返實測見 tests/evidence/mes-053。建議循序/任務/ER三入口共用內容，先做Lot未進機原型。本輪只審查與文件，網站未重構，真人學習效果未驗證。設計審閱pending，不把建議當實作完成；一次性finish_docs.py不重跑。

# MES-052 四主題八張教學圖

BMIR、Port UP／LOST、Lot RQHBE、KER_WIP_Y_BTH 每日07:20快照，已補專屬桌機／手機圖。每日快照路徑與執行時圖面標籤已修正，原始ER保留。FRPORT_UDATA維持撤下教學。讀 workitems/mes-052/REVIEW.md；驗證 python workitems/mes-052/check.py，KER回歸 python workitems/mes-050/check.py。證據 tests/evidence/mes-052；使用者審閱 pending。一次性 integrate.py、fix_snapshot.py、finish_docs.py 不重跑。

# MES-051 廠內定義補充

BMIR：OHB 空時呼叫 RTD 計算下一批上架貨。Port UP有貨/LOST無貨。Lot R加工中/Q等待/H待確認/B長期暫置/E已出貨。KER_WIP_Y_BTH每天07:20機群與KPI快照（取代每週一）。FRPORT_UDATA撤下教學文字，原ER保留。文字已更新，尚未新增這些主題插圖。

# MES-050 KER 圖文已更新

依已確認定義製作分群/SQL/目前與歷史總覽，三主題十二引用同步。讀 workitems/mes-050/REVIEW.md；驗證 python workitems/mes-050/check.py。公式暫不處理，使用者審閱 pending。

# MES-050 KER 定義確認

關係問題回答已記錄於 workitems/mes-050/KER-DEFINITIONS.md。尚未製作 KER 新圖文；指標公式與彙總方式依使用者指示暫不處理。

# MES-049 OHB

OHB 為機台鄰近 FOUP 暫置架，遠端 Stocker 先搬至鄰近暫放以方便後續快速搬運。雙尺寸圖文及設定/狀況四引用已更新，BMIR 分離。讀 workitems/mes-049/REVIEW.md；驗證 python workitems/mes-049/check.py。使用者審閱 pending。

# MES-048 Default Stocker

機台預設 Stocker（FOUP 倉儲）專屬雙尺寸圖文已更新，設定與位置/搬送分清。讀 workitems/mes-048/REVIEW.md；驗證 python workitems/mes-048/check.py。使用者審閱 pending。

# MES-047 機群與課別

MFG_EQP_OWNER_BT 專屬圖文已補：由機台查機群、管理單位及廠商名稱。owner 映射與一般 group 分開。讀 workitems/mes-047/REVIEW.md；驗證 python workitems/mes-047/check.py。使用者審閱 pending。

# MES-046 PART 與 Flow 版本

產品/PART 對應 Flow，進版時同步記錄版本資訊。專屬雙尺寸圖文已更新。讀 workitems/mes-046/REVIEW.md；驗證 python workitems/mes-046/check.py。使用者審閱 pending。

# MES-045 SRTS 抽測規則

使用者確認 SRTS 定義 Flow 站點 Sampling rule 與比例，例如 Part 抽檢30%。專屬雙尺寸圖文已更新，不臆測抽樣單位。讀 workitems/mes-045/REVIEW.md；驗證 python workitems/mes-045/check.py。使用者審閱 pending。

# MES-044 Module／Stage／Step

使用者確認 Module 如黃光，包含多個 Stage，每個 Stage 包含細部 Step。雙尺寸圖文及 Lot 歸屬對照已更新。讀 workitems/mes-044/REVIEW.md；驗證 python workitems/mes-044/check.py。使用者審閱 pending。

# MES-043 Recipe Group

群組包含可做類似加工的機台，依產品/加工條件切換多台或單台加工許可。專屬雙尺寸圖文已更新。讀 workitems/mes-043/REVIEW.md；驗證 python workitems/mes-043/check.py。使用者審閱 pending。

# MES-042 未來的 Flow

Lot forecast 專屬圖文已補：Flow 站序加 IE WPH 耗時估算，逐站預計到站。未套用 Stream 的 LDS 替代標記。讀 workitems/mes-042/REVIEW.md；驗證 python workitems/mes-042/check.py。使用者審閱 pending。

# MES-041 Stream 到站預估

Flow 站序與 IE WPH 耗時估算的專屬圖文已更新，標明舊功能由 LDS 取代。Stream 與一般 forecast 映射分離。讀 workitems/mes-041/REVIEW.md；驗證 python workitems/mes-041/check.py。使用者審閱 pending。

# MES-040 Product Hold

PID 依產品與站點設定管制，同產品 Lot 各自到站暫置以便統一處理。專屬桌面／手機圖文已更新。讀 workitems/mes-040/REVIEW.md；驗證 python workitems/mes-040/check.py。使用者審閱 pending。

# MES-039 Move 圖文

專屬圖文已更新，詳 workitems/mes-039/REVIEW.md。使用者審閱 pending。

# 最新接續：MES-038 批貨歷史圖文

Lot各種動作的專屬桌面/手機圖文已補，詳workitems/mes-038/REVIEW.md。

# 最新接續：MES-037 預派歷史圖文

CSFHPREDISP預知Lot與歷史回查專屬桌面手機圖文已補，驗證見workitems/mes-037/REVIEW.md。

# 最新接續：MES-036 FOUP查Lot圖文

material兩節點改依使用者確認的裝載概念，專屬桌面手機圖已更新，詳workitems/mes-036/REVIEW.md。

# 最新接續：MES-035 Load Port圖文

四角色三時點圖與手機版完成，七Port來源及路徑驗證通過，詳workitems/mes-035/REVIEW.md。

# 最新接續：MES-034 EQP Bay圖文

機台所在走道與管理單位專屬圖文/手機版已補，四來源驗證通過，詳workitems/mes-034/REVIEW.md。

# 最新接續：MES-033 傳送歷史圖文

原始MCS與presum資料的比較插圖、手機版和各節點說明已補，詳workitems/mes-033/REVIEW.md。

# 最新接續：MES-032 Chamber教材入口

專屬圖文與完整課程入口已補，桌面手機教材往返通過，見workitems/mes-032/REVIEW.md。

# 最新接續：MES-031 MCS巨觀/微觀命令

MCS兩節點及閱讀路徑補專屬命令層級、FOUP時間位置追查及互動示例；驗證見workitems/mes-031/REVIEW.md。

# 最新接續：MES-030 Lot與Wafer關係

單Lot25片／多Lot共FOUP互動示例與專屬介紹，桌面手機測試通過，詳workitems/mes-030/REVIEW.md。

# 最新接續：MES-029 PD專屬教材

PD=Process Definition使用者已確認；七節點及路徑補定義、Recipe/Tool關係與桌面手機圖。詳workitems/mes-029/REVIEW.md。

# 最新接續：MES-028 閱讀歷程返回

返回前一檢視/全圖/瀏覽路徑與跨頁返回來源已補。Multi-agent審查及桌面手機歷程驗證見workitems/mes-028/REVIEW.md。

# 最新接續：MES-027 預派目標是機台

預派—FOUP支線撤下，Lot—預派—EQP保留；四方向桌面手機檢查通過。詳workitems/mes-027/REVIEW.md。

# 最新接續：MES-026 主詞教材不可套 FOUP

已修節點與18閱讀路徑的配對，121節點明確映射；Future Hold／QTime各有專屬圖文，其他主題按語意介紹，未配對不得回退FOUP。Future Hold手機直向圖 assets/mes-026。讀 workitems/mes-026/REVIEW.md，驗證 python workitems/mes-026/check.py。品質未自動評分，使用者審閱pending；不是每個主題都有新插畫。一次性integrate.py不重跑。

# 最新工作：MES-025 Qtime包含Lot及專屬教材

來源完整鏈、起訖事件/限值教學、桌面/手機插圖與完整教材入口已更新，1440/390驗證PASS。详workitems/mes-025/REVIEW.md。

# 最新工作：MES-024 Lot Step補Lot上下文

Lot Step及FOUP相關圖已保留中間Lot和原始Summary關係，1440／390驗證PASS，詳workitems/mes-024/REVIEW.md。

# 最新工作：MES-023 Lot預派

右側新增Lot業務關聯，重製桌面／手機派工示意圖，主要對象Lot，FOUP輔助。桌面手機驗證通過，詳workitems/mes-023/REVIEW.md。

# 最新工作：MES-022 FOUP內容物歷史

fhwlths改依使用者定義說明時間、Wafer及Split／Merge進FOUP的更新。桌面／手機檢查PASS，詳workitems/mes-022/REVIEW.md。

# 最新工作：MES-021 帶到校正

帶到／FRLOT_EQP表示Lot在該站點有可用機台；主圖、小圖、相關說明已修正。桌面／手機檢查PASS，詳workitems/mes-021/REVIEW.md。

# 最新工作：MES-020 右側展開

已新增整個右側圖與說明的大視窗，桌面／手機操作驗證通過，詳workitems/mes-020/REVIEW.md。

# 最新工作：MES-019 機群WPH參考圖

依生管為機群定義預期WPH的使用者說明，新增桌面／手機專屬插圖並綁定WPH節點，詳workitems/mes-019/REVIEW.md。使用者審閱pending。

# 最新工作：MES-018 裝載關係修正

依使用者第二張圖撤下FOUP/Step歷史錯誤支線，Lot — FRCAST_LOT — FOUP為裝載關係。詳workitems/mes-018/REVIEW.md。

# 最新工作：MES-017 主詞關聯 ER

依使用者要求完成 Multi-agent 設計與網站整合。選主詞後重排來源關係，桌面左右對照、手機兩支線分頁。實作、驗證與限制見 workitems/mes-017/REVIEW.md；使用者驗收 pending。

# 最新接續：MES-010

已新增 support.html 四節：CW、Sub Route（加量＝追加量測，回原站）、Move（Lot 過站事件，重工計入）、MON／PM／Daily MON／EMS。先讀 workitems/mes-010/CONTENT.md、PLAN.md、REVIEW.md。驗證 python tests/check_support.py：154項通過。使用者驗收 pending；AAA 及 AVL／Eff／Lost／Up 定義未確認。advanced.html 僅新增入口，其餘既有前端以歷史 hash 核對。舊 manifest 不再代表本輪修改後的共用文件，不覆寫歷史證據。

# 目前工作：MES-009

七個名詞已新增於 advanced.html，附七張新插畫、四組原生互動與五個情境問題。Flow 三候選加原版可切換並記錄本機偏好。逐圖評比 workitems/mes-009/REVIEW.md；講解稿 CONTENT.md；使用者選版及內部定義確認 pending。

# 目前工作：MES-008

資料新鮮度六節重新製作；MES-007 新鮮度高分已撤回。基線、學習、brief 與驗證計畫：[workitems/mes-008/PLAN.md](workitems/mes-008/PLAN.md)。狀態：六節／12張主圖已更新，18版面與190操作驗證通過；逐頁評比見 workitems/mes-008/REVIEW.md。使用者未驗收。

# MES 教學網頁工作紀錄

## MES-007｜十五頁插畫重製＋資料新鮮度｜2026-09-12

已依使用者授權實際製作：指定15頁的新主視覺、14張手機直式圖，以及第四部分6節與3個互動案例。使用五份共用Markdown、teaching-review-cycle、planned-code-modifier、imagegen；不是只更新計畫。參考第一課的實物→細節→資料關係，原精確資料練習改為可展開，16情境保留。

逐圖／逐頁分項、手機退回、生成內容錯誤與修正見 [MES-007 REVIEW](workitems/mes-007/REVIEW.md)。本輪紀錄不覆寫MES-004被退回事實；作者自評、工具驗證與使用者認可分開，使用者 pending。實際結果與資產雜湊見 [evidence-manifest](workitems/mes-007/evidence-manifest.json)。

學習：跨課題長prompt會污染單圖；直式重排可能改變物件數量與因果，須重新檢查；收合原圖後正文指示也必須同步重讀；功能PASS不能抵銷視覺缺口。後續每頁固定參考與責任，保存拒收稿、修正及實際渲染證據。


## MES-006｜第一課與十五頁互比；品質結論撤回

使用者再次退回 MES-004，指定 index.html#fab 為較精緻的參考。已完成 [十五頁逐項互比](workitems/mes-006/COMPARISON.md) 與 [可切換互比頁](workitems/mes-006/comparison.html)。下方 MES-004「自評完成」是已撤回的歷史狀態；review.json 已重開、保留原分數並列未解缺口，使用者品質驗收 rejected。功能結果不替代視覺品質。

後續從 Chamber 與 Stage 代表原型重新建立設計；十五頁尚未再重製。新增資料新鮮度（MES-005）的完整要求仍保留於對話，尚未製作，先依最新要求釐清比較基準。

## MES-004｜第二次品質退回；全 15 頁重開｜2026-09-12

目前狀態：15 頁重製、技術驗證與桌面／手機教學自評完成，使用者審閱 pending。MES-003「整批完成」的結論撤回；其功能測試與六張圖的歷史記錄保留，但不能代表使用者指定 15 頁的教學品質。本輪證據見 [MES-004 計畫](workitems/mes-004/PLAN.md) 與 [逐頁評分](workitems/mes-004/review.json)。

已記學習：範圍遺漏、以功能代教學、未映射量表而跳過整頁評分、沒有證據失效檢查。防重犯改為固定 URL 清單＋逐圖／逐頁審查＋可執行覆蓋檢查；13 項防漏測試通過。完成 13 個概念主圖、4 組可切換快照、2 個動態情境主圖及 15 個改條件練習；保留 16 個操作情境。採精確 HTML/CSS 圖解，本輪沒有宣稱產生 15 張 AI 點陣插畫。真人理解與使用者驗收尚未完成。

## MES-003｜第二部分全面重做、第三部分 Flow 深入｜2026-09-12

授權：使用者明確要求重做整個第二部分，第三部分深入 Flow、Stage、Step、Lot如何套用，以及一次製作更多情境。舊版影像品質被否定，本輪從實際DefectFill r03成圖參考重製。

- [x] 保存基線、核對五份Markdown、撰寫OpenSpec與逐圖brief，先做設備原型。
- [x] 第二部分重做8段教材與6個獨立情境。
- [x] 第三部分新增10段教材與10個獨立情境，含完整六站旅程與例外。
- [x] 內建imagegen產出6張啟用圖（桌面／手機各3），失敗版本保存並迭代。
- [x] 狀態不變量、實際UI、桌面／手機、第一課回歸、最終定向HTTP檢查。
- [x] 更新README、共用log、REVIEW、來源／prompt與入口；舊程式及測試移入baseline。

交付：第二部分 http://127.0.0.1:4175/operations.html ，第三部分 http://127.0.0.1:4175/flow.html 。第一課已有兩個新入口。第三部分直接情境為 `#lab?case=normal`、`rework`、`split`、`version` 等，完整16項見README。

內容契約：Flow定義與Lot執行分離；Stage為本課分組，Step occurrence區分可重用Operation與Recipe內步驟；F-DEMO v1三階段六站；例外有批准、成員守恆與歷程。原始完整ER未提供，非特定MES schema或量產配方。

驗證：狀態16情境／66狀態／85邊PASS；兩課54版面／32實際旅程與額外分支PASS；第一課8組／21版面PASS；最終18定向畫面與13份HTTP資產PASS。證據在 `tests/evidence/mes-003/`，詳細適用範圍與扣分理由見 `workitems/mes-003/REVIEW.md`。

視覺修正：Flow手機箭頭改為六站單欄，Lot標記改為非警報色；手機前後比較不再依賴左右捲動；預期槽位與實讀資料分開；v2新增S45真正插入路徑；情境保留標題及可展開完整Flow。已實看啟用原圖與代表最終頁面；未宣稱真人學習效果或使用者驗收。

狀態：本輪實作與驗證完成，使用者審閱 pending。本機預覽，未公開發布；VisionAI來源專案未修改。下一步依使用者對內容深度、圖像與實廠命名的回饋調整。

## MES-002｜其他角色與操作情境｜2026-09-12

授權：使用者要求「再產生其它剩下的，也產生幾個情境」，延續本機網頁、Fab 新手程度。原圖的完整 Entity Relationship 清單沒有保存在工作區；已提出範圍確認，先依已知原圖 Tool／Port 與常見入門角色規劃，不宣稱涵蓋未提供的全模型。

預定內容：Tool／Equipment、Load Port、Chamber、Recipe、Route／Step、AMHS／OHT／Stocker、加工／Hold 狀態。4 個互動情境：載具搬送停靠、配方與逐片加工、Hold 與複核、槽位異常核對。每個情境獨立重設到相同初始範例，不把跨情境狀態冒充同一連續交易。

計畫與驗收：
- [x] 核對既有教材與來源，整理擴充範圍。
- [x] 建立第二課與第一課雙向入口，補齊物件、位置、流程與狀態說明。
- [x] 建立四個可操作情境，均有初始狀態、選擇／操作、結果、原因與重設。
- [x] 驗證錯配不推進、搬送狀態、逐片與整批完成差別、Hold 不改位置、異常片數及重設。
- [x] 驗證桌面／手機頁面、導覽、鍵盤、離線與 HTTP；回歸第一課。
- [x] 記錄來源、實際驗證與審閱狀態，交付入口。

實作方式：獨立 `operations.html`、`operations.js` 與 `operations.css`，重用既有基本配色與元件；不把第一課的七段大幅擴成長清單。精確位置與狀態使用 HTML/CSS 原生示意，不產生含虛構實測數字的圖片。

視覺 preflight：代表頁採 C 解釋型，從 FOUP／Load Port 的交接，追到 Tool 內 Chamber，再到資料，3 個具體節點；連線區分物理移動與歸屬。沿用已實看的 Fab 原型與 DefectFill 閱讀方式。單一淡黃結論「載具停靠、晶圓加工、系統紀錄，是相連但不同的事件」。每個情境的變化直接出現在具名物件、位置或狀態上；手機直向重排，互動回饋鄰近控制項。

狀態：第二課本機實作、測試與最終版面修正檢查完成，待使用者審閱。10 段包含 6 段基本介紹、4 個獨立互動情境。入口 http://127.0.0.1:4175/operations.html；`#arrival`、`#run`、`#hold`、`#reconcile` 可直達情境。

驗證：`tests/check_operations.py` PASS，包含桌面／手機四情境的正確與錯誤分支、原地重設／加工中重設、50 個版面狀態（1440／900／768／390／360）、雙向課程入口、HTTP 檔案與互動。`tests/check_lesson.py` 第一課 8 組行為＋21 個版面回歸 PASS。第二課證據 `tests/evidence/operations-v01/results.json`，原生離線與本機 HTTP 均可用。

實看：十段桌面／360 寬主線、W07 加工中／Hold 解除／W99 身分差異的代表狀態。測試找到配方 option 標記錯誤，已修正並重跑通過。視覺審查後把手機搬送／交接箭頭改為上下方向；Ready／Processing 文案改為和情境中開工確認、逐片間隔一致。最後這些小改動以 `tests/check_operations_layout.py` 定向確認，不重跑未變動狀態邏輯。

最終檢查：`tests/check_operations_layout.py` 的 9 組版面、狀態文字、手機箭頭與 HTTP 資產比對 PASS，證據為 `tests/evidence/operations-v01/final-layout.json`；已實看修正後的手機搬送、狀態與加工三頁。

下一步：依使用者閱讀回饋或完整 ER 清單調整。使用者審閱 pending；未給品質分數、未跑真人學習測試、未公開發布。未修改 Vision AI 專案。

## MES-001｜Fab 基礎 Example 第一輪｜2026-09-12

目標：為只有最基本 Fab 知識的讀者介紹 Lot、FOUP、Slot、Wafer；沿用 Vision AI 的章節導覽、大圖、延伸收合與互動閱讀方式。
授權：本機製作與預覽；未要求公開發布。使用者已認可原型方向，新的網頁仍待審閱。

計畫：
- [x] 讀取指南、原型與 Vision AI 原始碼，實看參考網站。
- [x] 完成基本教材、響應式網頁與可放大的實物圖。
- [x] 完成點選晶圓、資料對照、換載具與理解自測。
- [x] 實測桌面／手機、鍵盤、導覽、圖像放大與狀態一致性。
- [x] 更新 README、來源與檢查證據，提供可開啟入口。

設計：先 Fab 情境，再 Wafer → FOUP → Slot → Lot → 動手對照 → 自測。簡化 ID 全課保持 W06/W07/W08、L023、F012。位置是當下快照；批次是管理歸屬。Lot 換載具範例只演示位置欄位改變，不執行生產系統操作。

參考：`C:/code/claude/visionAI/teaching-images/vision-ai-model-selection/interactive-learning.html`、指定 DefectFill 網頁；截圖 `examples/visionai-reference.png`。Vision AI 僅讀取，頁面建於 MES_DATA。

視覺 preflight：
- 代表原型：`examples/fab-physical-data-v01.png`，已實看；既有 AI 生成示意，保留原檔。
- C 解釋型：設備全景 → 同一載具槽位 → 資料對照，3 個節點，連線代表位置對應。
- 核心結論：「位置告訴你晶圓在哪裡；批次告訴你它屬於哪一組生產工作。」淡黃 #FFF4CC。
- 新增網頁原生物件：單片晶圓俯視／側視、載具中的水平晶圓、具名槽位與 Lot 成員清單。藍色表示選取；綠色表示答對。使用 HTML/CSS 以保持文字、選取與資料精確且可重排，不另批量產生投影片。
- 手機主線用 HTML 大字與重排場景；舊圖作整體回顧，可放大，不依賴手機縮圖解釋新名詞。
- 指南：沿用本目錄五份教學文件的可讀性、關係一致與證據原則。既有量表的模型選型項目不適用本次 Fab 名詞入門，不冒稱模型課 >90 達標。

驗收：七段可到達；選取非預設晶圓與空 Slot 時資料一致；整批換 FOUP 後 Wafer/Lot 保持、位置改變；重設可恢復；自測有具體理由；360/390/1440 寬無橫向溢出；圖片載入、放大、Escape 與焦點回復；檔案可離線開啟。

目前：第一轮本機實作與驗證完成，待使用者審閱，未公開發布。入口 `index.html` 或 http://127.0.0.1:4175/；互動直達 `#explore`。伺服器若停止，依 README 重啟。

實際驗證：`python -X utf8 tests/check_lesson.py` PASS（8 組行為檢查、21 個章節／寬度狀態、無 JavaScript 錯誤）。原生檔案可離線使用；HTTP 首頁 200。截圖、結果 JSON 保存在 `tests/evidence/`。已實看全部七段桌面與 360 寬畫面；390 寬另外驗證互動前後狀態。沒有真人學習測試，不宣稱 >90 或使用者核准。

修正：圖像放大按鈕移出影像，避免遮擋結論；手機互動加入鄰近即時資料摘要；窄版標題採平衡換行。沿用既有可讀性與物件連續性原則，沒有另增整套規則。

下一步：依使用者對內容深度、圖像與閱讀方式的回饋，改進 MES-001；目前没有待執行產圖程序。Vision AI 專案未改動。
## MES-011｜ER 圖與教學整合

- 已新增 data-map.html 七節、14案例及原 SVG 聚焦／逐點閱讀。
- 已串接六個既有課程與原圖瀏覽器入口。
- 驗證與限制見 workitems/mes-011/REVIEW.md；使用者審閱 pending。
- 以最新確認定義解說 AVL、Lost、UP；不推定 Eff、Join 條件或逐表 freshness。
## MES-012｜整合大圖與跨圖題目

已新增 integrated-map.html、ER/INTEGRATED/fab-integrated.svg、map.json；20共同主題、128原節點／128原關係索引、五題跨圖解說。入口在首頁、第二／三部分側欄與逐圖頁。驗證tests/check_integrated_map.py，交付紀錄workitems/mes-012/REVIEW.md；使用者審閱pending。
## MES-014｜整合ER v2

已依三位agent畫後審查完成第二輪修正。er-atlas.html為新頁、integrated-map.html保留原入口轉址；SVG121節點128邊。測試tests/check_er_atlas.py與workitems/mes-014/check_entry.py；完整評比workitems/mes-014/REVIEW.md。v2兩位整體評分91，完整專項35/35；使用者審閱pending。
# MES-055｜指定頁面圖文補強

12個指定頁面已調整，material為參考對照。10張新圖、7個主題案例解說、基礎四頁寬單欄、裝載互動可展開。驗證與限制見 workitems/mes-055/REVIEW.md；使用者審閱 pending。
