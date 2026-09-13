"""Write this round's review and index; does not judge screenshots automatically."""
from pathlib import Path
import json, hashlib, html
ROOT=Path(__file__).resolve().parents[2]
W=ROOT/'workitems/mes-009'
pages=[
('qtime',[19,19,19,18,9,9],['L023 從 10:00 到 10:30 的事件限制，且可改現在時間。','進站／出站停止規則可比較；45 分鐘超時 15 分鐘可反算。','剩餘、邊界、超時、Hold 不重設對應工作處置。','等待／超時與兩種停止事件取捨具體；未展開多重 QTime 規則。','桌面情境圖＋手機原生時間尺；完整投影片在手機不是主讀版。','10:20 進、10:35 出的新情境要求先確認停止事件。']),
('future-hold',[19,19,19,18,9,9],['同一 Lot 在 S20 登記、S50 攔截的工作理由可追蹤。','待觸發與有效 Hold 分列，三次前進到 S50 才生效。','解除此筆不表示其他限制通過；動作與權限邊界明確。','Future 與立即 Hold 的時機比較；未模擬所有廠內觸發模式。','手機路徑直排，狀態與動作仍完整。','解除一筆但仍有其他 Hold 的情境檢查誤用。']),
('part-route',[19,18,19,19,9,9],['P-DEMO／F-DEMO v1／兩批不同位置的共同案例。','定義與引用分開；Part 的內部層級未確認，僅對明示教學模型評比。','查產品、路徑版本、目前位置、歷史各有對應欄位。','同一主檔與不同批次、主檔升版與批次遷移分開。','插畫有工單與晶圓；手機箭頭文字改成正常方向。','新增 v2 不等於 L023 自動遷移。']),
('recipes',[19,18,19,19,9,9],['S40、LR、ER、設備與實體配方維持同一案例。','三層角色與適配解釋明確；內部 ER 界線未確認，不當成正式 schema。','同名舊版可見不一致，分加工前／後處置。','切換設備改變 ER／Physical；核准映射與執行回報分開。','桌面插畫與欄位比對，手機改為直向且連線標籤不旋轉。','用同名舊版本測是否理解實際執行證據。']),
('flow-versions',[19,19,18,19,9,9],['四種教法依新手的層級、進度、資料查詢問題區分。','A 含括放大、B 單批路徑、C 共用定義與兩批進度可見差異。','能選教法、記錄偏好並銜接後續主題；不是完整實務控制演練。','每版都有適用理由與需要補充的地方。','桌面逐圖切換；手機 C 的兩批進度放在同屏；插畫縮圖僅預覽。','兩批位置不同不意味 Flow 不同。'])]
figures=[
('qtime.png',[24,24,19,18,9],[9,9,9,8,9],['起點、等待、終點三情境連同時間可辨識。','時間軸已改成 20:10 比例，剩餘 10 分鐘可反算。','結論指出時限綁事件及 Hold 不重设。','大字與一條閱讀線成立；左工單次要文字較細。','移除擅加批量；實物為示意，不是清洗或載入硬體設計圖。']),
('future.png',[24,24,19,18,9],[9,9,8,9,9],['登記的平板、途中作業、到站攔截具體。','S20 到 S40 明示中間站略；錯誤下一站牌已移除。','待觸發／有效 Hold 及先覆核可直接讀出。','三幕可追蹤同一 Lot；中間圖製程细節較多。','橘色閘門為控制概念示意，不代表實際設備實體門。']),
('part.png',[24,23,19,18,9],[9,9,9,8,9],['規格文件、路徑表、兩批工單與晶圓載具形成具體案例。','兩批共用路徑而目前位置不同；產品與路徑的關係是本例選用。','查詢應分產品、路徑版本、批次進度。','核心 ID 與目前 Step 清楚；主檔說明小字不作手機主線。','圖例教學映射明示；尚非內部資料字典驗證。']),
('recipes.png',[24,23,19,18,9],[9,9,8,8,9],['S40 工單、邏輯要求、設備、實際配方與回報對照。','兩條對應箭頭連 LR／ER／Physical，設備 ID 保持一致。','核准 v7 與回報 v7 可比，結論要求核對執行記錄。','ID 與版本大字；中欄細目仍需放大，不影響三層主線。','移除所有晶圓適用的錯誤敘述；內部定義明示待確認。']),
('flow-a.png',[24,24,18,18,10],[9,9,9,8,9],['全路徑、Stage B 兩站、S40 剖面由小到大。','包含關係用放大區呈現；不把三層當時間順序。','讀者可選定觀看層級；非現場動作教學。','層次清楚；左六站次要標籤較小。','S60 已改為行政清單，氣體配方標籤已移除。']),
('flow-b.png',[24,23,19,19,9],[9,9,9,8,9],['同一 L023 指標位於 S30，兩站完成、三站未到。','路帶依 S10→S60 明示順序；反向箭頭全部移除。','藍色目前與綠色完成分離，提示位置由事件更新。','地圖與站點可追蹤；以形狀對照順序而非寫滿卡片。','Stage B 漏標已補回，移除裝飾人與品牌。']),
('flow-c.png',[24,24,19,19,9],[9,9,9,9,9],['一條定義與兩批不同進度在共同座標上可比。','S50 與 S20 分別對應 L023／L024，六站完全對齊。','直接支持查目前 Step 與路徑定義需分開。','橫向三列比對清楚；手機主線另採兩列精確原生進度。','實物只用於批次對象辨識，沒有把 LotId 印在載具上。'])]
native=[
('qtime',[24,24,19,19,9],['起訖與倒數有共同 Lot 案例。','規則切換改變停止事件且時間不重設。','邊界／超時狀態有處置。','時間尺刻度已對齊；手機核心字可讀。','示例不代表廠規；計時器呈現限制而非真實系統時鐘。']),
('future-hold',[24,24,19,18,9],['Lot 指標逐站前進。','預約／有效兩種狀態在 S50 切換。','觸發後前進停用，覆核解除另有條件。','手機六站較長，但狀態及操作同區可讀。','只有本例單一登記，不表示所有 Hold 類型都受模擬。']),
('part-route',[23,24,19,18,9],['P-DEMO／F-DEMO v1／L023 與 L024 可切換對照。','改 Lot 只改位置，不改路徑定義。','查詢欄位與身分分開。','資料文件本身是圖的物件；較插畫抽象，依賴字面辨識。','手機上下方向明確標示 Lot 引用。']),
('recipes',[24,24,19,18,9],['設備切換改變 ER 與實體配方。','核准與回報同名不同版本可見。','前／後加工不一致處置清楚。','手機大字直向對照，文字不再旋轉。','僅測 ID／版本，不誇大成完整加工許可。'])]
review={'round':'MES-009','rubric':'1.0','user_acceptance':'pending','internal_dictionary_confirmation':'pending (Part, LR/ER mapping)','learner_study':'not performed','scoring_scope':'author review of explicitly illustrative lessons; not factory-specific schema certification','pages':[],'images':[],'native_figures':[]}
for name,score,reasons in pages:
    review['pages'].append({'id':name,'scores':score,'total':sum(score),'evidence':reasons,'screenshots':[f'tests/evidence/mes-009/{name}-{w}.png' for w in [1440,800,360]],'veto':[]})
for name,score,visual,reasons in figures:
    review['images'].append({'path':'assets/mes-009/'+name,'scores':score,'total':sum(score),'visual_scores':visual,'evidence':reasons,'review_scope':'original raster and desktop use; phone raster is optional enlarged reference, not scored as a standalone phone lesson','veto':[]})
for name,score,reasons in native:
    review['native_figures'].append({'id':name,'scores':score,'total':sum(score),'evidence':reasons,'screenshots':[f'tests/evidence/mes-009/{name}-visual-{w}.png' for w in [1440,800,360]],'veto':[]})
for group in ['pages','images','native_figures']:
    for row in review[group]:assert row['total']==sum(row['scores']) and row['total']>90
(W/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# MES-009：逐頁與逐圖檢視','', '作者評比，量表 v1.0。使用者選擇／核准 pending；未做真人學習測試。Part 與 LR／ER 的內部定義 pending。這些分數評明示假設的教學品質，不是內部 schema 已認證。','', '量表術語對照：模型意義 → MES 概念與規則；方法比較 → 規則、層級、時機與教法取捨；資料準備 → 查詢／執行證據欄位。權重與門檻不變。','', '## 真正改過的地方','', '- A 首稿把 S60 畫成設備，修成管理清單。','- B 先退回近似原版的三欄，再修反向箭頭、裝飾人物、品牌與遺失的 Stage B。','- QTime 移除擅加批量並修時間比例。','- Future Hold 移除誤導的「下一站 S40」。','- Recipe 移除「所有生產晶圓」適用範圍，改為本例產品。','- 手機原生箭頭不再連文字一起旋轉；C 兩批進度改成同屏比較。','', '原型、來源與構圖責任見 [PLAN](PLAN.md)，講解稿見 [CONTENT](CONTENT.md)，prompt 見 [generation-prompts](generation-prompts.json) 與 [Flow 初始 prompts](prompts.json)。','', '## 頁面評比','']
for r in review['pages']:
    md += [f"### {r['id']}：{r['scores']} = {r['total']}",'']+[f'- {i+1}. {x}' for i,x in enumerate(r['evidence'])]+['',f"證據：[{r['id']}-1440](../../{r['screenshots'][0]})、[800](../../{r['screenshots'][1]})、[360](../../{r['screenshots'][2]})。否決項：無（以已明示教學假設為範圍）。",'']
md+=['## 逐張新插畫','', '圖片按原始圖與桌面嵌入評分；手機投影片縮圖不被宣稱可獨立閱讀。手機主線是重新排版的原生圖與短說明，另有完整圖放大。原版 stage-v2.png 僅保留作使用者指定比較基準，不因本輪提高其歷史分數。','']
for r in review['images']:
    md += [f"### {Path(r['path']).name}：{r['scores']} = {r['total']}",'',f"完成度（美感／完整／專業／密度／層級）：{r['visual_scores']}。"]+[f'- {i+1}. {x}' for i,x in enumerate(r['evidence'])]+['',f"原圖：[檢视](../../{r['path']})。否決項：無；示意圖不是真實現場照片。",'']
md+=['## 原生互動圖','']
for r in review['native_figures']:
    md += [f"### {r['id']}：{r['scores']} = {r['total']}",'']+['- '+x for x in r['evidence']]+['',f"證據：[桌面](../../{r['screenshots'][0]})、[手機](../../{r['screenshots'][2]})。",'']
md+=['## 技術驗證与實務限制','', 'python tests/check_advanced.py：90 項檢查通過，包含 5 節 × 3 尺寸、四種候選、情境回饋、時限邊界、Hold、配方版本、偏好與放大。這些檢查不產生教學分數。','', '尚無真人理解證據，也沒有使用者指定的最終 Flow 版本。LR／ER、Part 的廠內定義仍待確認。保留原課；不操作真實 MES。']
(W/'REVIEW.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
# Scope indices: these are current-round docs; old reviews/manifests remain historical.
updates={
'AGENTS.md':'# 最新接續：MES-009\n\n本輪新增 advanced.html：QTime、Future Hold、Part／RouteId、LR／ER／Physical，以及原版＋三種 Flow 候選。先讀 workitems/mes-009/PLAN.md、CONTENT.md、REVIEW.md。檢查 python tests/check_advanced.py（90項）。使用者選版 pending，Part／LR／ER 的內部字典 pending；頁面已明示教學假設。新圖 assets/mes-009，原 stage-v2.png 保留。MES-008 入口與新鮮度資產未改，root 共用文件新增內容後，其旧 manifest 不再代表當前全部文件。不得重跑舊生成器覆蓋新內容。\n\n',
'WORKITEMS.md':'# 目前工作：MES-009\n\n七個名詞已新增於 advanced.html，附七張新插畫、四組原生互動與五個情境問題。Flow 三候選加原版可切換並記錄本機偏好。逐圖評比 workitems/mes-009/REVIEW.md；講解稿 CONTENT.md；使用者選版及內部定義確認 pending。\n\n',
'TEACHING_REVIEW_LOG.md':'# MES-009｜名詞說明與 Flow 候選教法\n\n新頁 advanced.html，七個名詞分成四節工作情境；另有原版＋三個 Flow 候選。參考使用者貼出的 stage-v2.png，使用 teaching-review-cycle 與內建 imagegen。先 brief／原型，再實圖檢查；S60 性質、反向箭頭、背景下一站牌、配方適用範圍、時間比例均有退回與修正。手機修正整段旋轉標籤與兩批跨屏對照，學習寫回兩份共用指南。90 項技術檢查通過；作者分項見 [REVIEW](workitems/mes-009/REVIEW.md)，不代替使用者認可。Part／LR／ER 內部定義待確認，頁面按明示教學假設交付。原正式 Flow 沒有自動換版；本機偏好僅用於比較。\n\n'}
for name,prefix in updates.items():
    p=ROOT/name
    t=p.read_text(encoding='utf-8')
    if not t.startswith(prefix.splitlines()[0]):p.write_text(prefix+t,encoding='utf-8')
p=ROOT/'README.md'
t=p.read_text(encoding='utf-8').replace('給 Fab 新手的四部分互動教材。','給 Fab 新手的四部分互動教材，加上時間、路徑與配方延伸章。')
if '## MES-009' not in t:t+='\n## MES-009：新增名詞與 Flow 候選\n\n- [時間、路徑與配方](http://127.0.0.1:4175/advanced.html#qtime)：QTime、Future Hold、Part、RouteId、LR、ER、Physical Recipe。\n- [Flow 四種教法比較](http://127.0.0.1:4175/advanced.html#flow-versions)：原版保留；A 層級放大、B 立體走站、C 定義與進度對照。本機記錄偏好不替換正式課程。\n- [講解稿](workitems/mes-009/CONTENT.md)、[逐圖評比](workitems/mes-009/REVIEW.md)、[製作與來源](workitems/mes-009/PLAN.md)。\n- 驗證：`python tests/check_advanced.py`。Part 及 LR／ER 的內部資料模型仍待確認，頁面明示教學假設。\n'
p.write_text(t,encoding='utf-8')
print('MES-009 review and documentation written; user acceptance remains pending.')
