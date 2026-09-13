/* MES055: bespoke explanations shared by standalone topics and ER. */
(() => {
 const topics=window.ER_TEACHING;
 const lessons={
 flowkey:['這批 Lot 使用哪一條 Flow？','先讀 Lot 的產品歸屬，再找產品所對應的流程與版本。',[
 ['從批次找到路徑','示例：Lot L023 屬於 Part P100，P100 對應 Flow F-A v2。沿 Part／mainpd_id 找到流程後，才能讀取這個版本的站點順序。'],
 ['流程版本也要一致','產品的 Flow 進版時，PART 會記錄對應進版資訊。查資料時要核對適用版本，不能把不同版本的站點混成一條路徑。'],
 ['路徑與足跡分開查','Flow 定義「應該怎麼走」。要回答 L023 已經走過 S10 或 S20，請查 Lot Step 或批貨歷史；流程定義本身不能證明已加工。']]],
 available:['本站有哪些可用機台？','以 Lot 與目前站點為主詞，查詢可用的設備關係。',[
 ['先列出候選設備','示例：L023 在 S40 對應可用機台 EQP-A 與 EQP-B。Siview.Frlot_EQP 的關係用來理解本站可用機台，這兩個候選不代表兩台都會加工這批。'],
 ['預派是下一個問題','如果要知道派工系統安排哪一台，應再看預派資料。要確認是否到達或開始加工，則再查位置或實際執行事件。'],
 ['讀圖練習','看到 A、B 都可用，能否回答 L023 已在 A 加工？不能。可用關係、預派安排與加工事實是不同資料。']]],
 eqpstatus:['機台狀態，要一起看時間','用設備身分與資料時間，理解機台在當時的狀況。',[
 ['同一台設備，兩個時間','教學示例：EQP-A 在 09:00 為 UP（加工中），09:30 為 LOST（閒置）。這是兩個時點的狀態，不是同時成立。'],
 ['先確認狀態屬於誰','依廠內定義，機台 UP 表示正在加工、LOST 表示閒置；Port 的 UP／LOST 則是有貨／沒有貨。相同字樣不能跨對象直接解讀。'],
 ['查詢時保留時間與層級','核對來源的更新時間，才能判斷狀態的新鮮度。整台機台狀態也不能代替每一個 Chamber 的狀態；要看腔體，需查 Chamber 資料。']]],
 eqpkey:['EQP_ID：辨認同一台設備','沿著設備識別欄位，對照不同資料中的設備關係。',[
 ['從身分開始對照','示例：設備資料與關係資料都出現 EQP-A。先確認它們指向同一台設備，再閱讀它所屬的機群或 PD／Recipe 配置。'],
 ['同名欄位不等於完整 Join 條件','EQP_ID 提供設備線索。實際串接仍需核對資料來源、廠區、版本或時間範圍，以及一台設備是否對應多筆配置。'],
 ['避免把關係筆數當設備數','同一台機台可以屬於多個機群，也可能有多個 Recipe 關係。展開後有多列，不表示多了幾台實體設備。']]],
 location:['FOUP 在哪裡，與晶圓是否加工','位置資料回答「在何處」，加工事件回答「做了什麼」。',[
 ['讀取當時位置','示例：FOUP F012 在 EQP-A 的 Load Port LP1。先確認載具、設備、Port 與時間，才能描述這一筆位置紀錄。'],
 ['FOUP 與 Chamber 分清楚','FOUP 在 Port 等待交接；晶圓送入機台內的 Chamber 才可能進行加工。插圖的腔體剖面是位置概念補充，不是由 Port 紀錄推導的加工結果。'],
 ['追蹤移動要查歷史','若問題是 F012 幾點由哪裡移到哪裡，應查傳送歷史。若問題是 L023 是否進機，應查對應 Lot 執行事件，並核對相同時間。']]],
 lotstep:['Lot Step：這批貨走過哪些站點？','以 Lot 為主詞，保留站點與時間，閱讀批次的站點歷程。',[
 ['三筆紀錄，兩個不同站點','示例：L023 在 09:00 記錄 S40、10:00 記錄 S50、11:00 再記錄 S40。第二次 S40 是另一筆歷程，不能只因站點相同就刪掉。'],
 ['查詢順序','先選 Lot，再讀站點及時間順序，對照 F12DM.DM_Lot_step_st 的來源定義。重複經過的原因與事件類型，要再核對批貨歷史。'],
 ['FOUP 不是站點歷史的主詞','FOUP 說明裝載位置，Lot 說明生產批次。查 Lot Step 要保留 Lot；若只看 FOUP，可能把內容物變更前後的不同批次混在一起。']]],
 contents:['FOUP 內容物歷史：當時裝了哪些 Wafer？','同一個 FOUP 的內容物會改變，歷史查詢必須指定時間。',[
 ['兩個時間，兩份內容物','教學示例：09:00 的 F012 裝 W06、W07、W08；10:00 更新後裝 W06、W07、W09。W08 與 W09 不同，不能拿後一份名單回答前一個時間。'],
 ['Split／Merge 時更新','Siview.fhwlths 記錄 FOUP 內容物的歷史；每次 Split／Merge 進 FOUP 時會更新。它用來追溯當時有哪些 Wafer，與搬運整個 FOUP 的傳送歷史不同。'],
 ['Slot 與批次歸屬另外核對','圖上的 W06 等是 Wafer ID，不是 Slot 編號。若要回答槽位或 Lot 歸屬，須核對相應來源及時間；本例不假設歷史表具有所有槽位欄位。']]]
 };
 for(const [key,[title,meaning,sections]] of Object.entries(lessons))Object.assign(topics[key],{title,meaning,image:`assets/mes-055/${key}.png`,mobile:`assets/mes-055/${key}.png`,alt:title,caption:'AI 教學示意；設備、ID、站點與時間為假設案例。圖示欄位不代表資料表實際 schema。',details:sections.map(([h,p])=>`<section class="explain-step"><h3>${h}</h3><p>${p}</p></section>`).join('')});
 Object.assign(topics.load,{image:'assets/mes-036/foup-query-lot-v1.png',mobile:'assets/mes-036/foup-query-lot-mobile-v1.png',alt:'FOUP 內多個 Lot 的 Wafer 與槽位對照',caption:'FOUP 可以放一個或多個 Lot；每片晶圓有自己的 Wafer ID。下方互動可切換裝載情境。'});
 topics.load.details=topics.load.details.replace('<div id="lot-wafer-demo"></div>','<details class="refresh-lab"><summary>動手練習：單一 Lot 25 片／多個 Lot 共用 FOUP</summary><div id="lot-wafer-demo"></div></details>');
})();
