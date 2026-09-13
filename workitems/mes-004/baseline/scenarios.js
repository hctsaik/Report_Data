'use strict';
// Finite teaching scenarios. Every node is a complete snapshot relative to its
// scenario baseline; rejected actions append an event without changing snapshot.
const choice=(label,next,message)=>({label,next,message});
const reject=(label,message)=>choice(label,null,message);
const node=(prompt,state,actions=[],lesson='')=>({prompt,state,actions,lesson});
const baseState={lot:'L023',product:'P-DEMO',flow:'F-DEMO v1',current:'S40',status:'Queued',location:'ETCH03／LP1',recipe:'ETCH-DEMO/v2',waferIds:['W06','W07','W08'],slots:{'06':'W06','07':'W07','08':'W08'},chamber:null,hold:[],done:['S10','S20','S30']};
const SCENARIOS={operations:[],flow:[]};
function add(course,id,title,sub,context,base,nodes){SCENARIOS[course].push({id,title,sub,context,base:{...baseState,...base},nodes});}
add('operations','arrival','01 搬送到錯誤 Port','搬送不等於過站','L023 在 S40 等待；F012 尚在 STK01。只有 ETCH03／LP1 是本次核准目的地。',{location:'STK01'}, {
 start:node('先選這次搬送的目的地。',{},[reject('送到 ETCH03／LP2','LP2 未被指定給這次搬送。F012 仍在 STK01，Lot 仍在 S40。'),choice('派送到 ETCH03／LP1','transit','建立搬送工作；F012 已由 OHT01 接走。')]),
 transit:node('載具搬送中。這時能宣告 S40 完成嗎？',{location:'OHT01',status:'Queued · 搬送中'},[reject('將 S40 標為完成','載具還在搬送，沒有任何 S40 加工證據。'),choice('確認抵達 LP1','arrived','收到到位確認；位置更新為 ETCH03／LP1。')]),
 arrived:node('載具已到位，但尚未加工。',{location:'ETCH03／LP1',status:'Queued · 待開工確認'},[],'搬送只更新載具位置。接著核對載具、槽位、設備與配方；S40 沒有被跳過。')
});
add('operations','reconcile','02 三片卻有錯片','片數與身分分開驗','預期 Slot 06/07/08 分別是 W06/W07/W08；本次讀值在 Slot 07 看見 W99。',{scan:['06=W06','07=W99','08=W08'],status:'Mapping review'}, {
 start:node('總片數相同，是否足以放行？',{},[reject('片數 3／3，直接接受','W99 不等於預期 W07。預期資料不被覆寫；開工仍被阻擋。'),choice('模擬重讀：Slot 07 沒有讀值','missing','新讀值已取代前次讀值；Slot 07 仍需確認。'),choice('核對實物後重讀：W07','matched','本例核對實物後取得 W07，等待最後核對。')]),
 missing:node('現在只讀到兩片；不可把「未讀到」直接當成報廢。',{scan:['06=W06','07=未讀到','08=W08']},[reject('直接刪除預期 W07','讀值缺失不能證明晶圓不存在。保留預期成員與差異。'),choice('確認實物並重新讀取','matched','重讀取得完整三片身分。')]),
 matched:node('新讀值相符，完成本次身分核對。',{scan:['06=W06','07=W07','08=W08']},[choice('確認三個槽位及身分','finish','本次讀取與預期一致。此核對成功，不等於所有開工條件完成。')]),
 finish:node('身分核對完成。',{scan:['06=W06','07=W07','08=W08'],status:'Queued · 身分已核對'},[],'片數與身分都需要核對；新的讀取必須重新判定，不能沿用舊的放行結果。')
});
add('operations','recipe','03 同名舊版 Recipe','版本是作業契約的一部分','S40 要求 ETCH-DEMO/v2；機台目前選到 v1。',{recipe:'ETCH-DEMO/v1'}, {
 start:node('配方名稱相同，版本不一樣。',{},[reject('直接開工','需求是 v2，現有 v1；拒絕，沒有建立加工紀錄。'),choice('載入並核對 v2','verified','配方版本核對成功；設備資格仍需確認。')]),
 verified:node('再選合格的設備。',{recipe:'ETCH-DEMO/v2'},[reject('改用空閒的 CVD02','CVD02 不在本例的 ETCH 合格設備群。閒置不能取代資格。'),choice('使用已核准 ETCH03／CH-A','finish','設備、腔體與配方版本通過本例確認。')]),
 finish:node('現在可以進入開工程序。',{recipe:'ETCH-DEMO/v2',status:'Ready · 資格已確認'},[],'Step 定義本次作業要求，設備資格與配方版本共同決定是否能執行。這裡尚未加工。')
});
const runNodes={};
for(let i=0;i<3;i++){
 const wafer='W0'+(i+6),slot='0'+(i+6),start=i===0?'start':'ready'+i,next=i===2?'data':'ready'+(i+1);
 runNodes[start]=node(`已完成 ${i}／3；下一片是 ${wafer}。`,{status:i?'Processing · 片間交接':'Ready',count:`${i}／3`},[reject('直接宣告整批完成',`只有 ${i}／3 完成，不能完成 S40。`),choice(`取出 ${wafer} 並開始加工`,'run'+i,`${wafer} 由 Slot ${slot} 進入 CH-A；原槽清空。`)]);
 runNodes['run'+i]=node(`${wafer} 在 CH-A；確認本片結果後再返回。`,{status:'Processing',count:`${i}／3`,chamber:wafer,slots:{'06':'W06','07':'W07','08':'W08',[slot]:null}},[reject('現在取下一片','本例單片 CH-A 尚未完成交接；下一片不能同時進入。'),choice(`記錄 ${wafer} 完成並返回`,next,`${wafer} 完成並返回 Slot ${slot}；累計 ${i+1}／3。`)]);
}
runNodes.data=node('三片已返回，但必要的 W08 結果資料尚未收到。',{status:'Completed · 待資料',count:'3／3',missing:'W08 結果資料'},[reject('Track-out 並到 S50','缺少 W08 結果，MES 完成交易被拒絕；Current 仍是 S40。'),choice('接收並驗證 W08 結果','verified','三片必要結果齊全，等待 MES 完成交易。')]);
runNodes.verified=node('完成本例的 Track-out，才推進下一站。',{status:'Completed · 資料齊全',count:'3／3'},[choice('Track-out：完成 S40','finish','S40 Visit #1 = Pass；Current 改為 S50，等待量測。')]);
runNodes.finish=node('S40 已完成；Flow 還有 S50 和 S60。',{current:'S50',done:['S10','S20','S30','S40'],status:'Queued',count:'3／3'},[],'晶圓歸位、機台完成、資料齊全與 MES 過站是可分辨的事件。');
add('operations','run','04 三片逐片加工','看中間狀態與資料交接','本例開工條件已核准。三片依序加工，最後 W08 的資料回報稍晚。',{},runNodes);
add('operations','fault','05 加工中設備故障','先確認在製片的處置','W06 已完成，W07 正在 CH-A，W08 未開始。設備在此刻發生故障。',{status:'Interrupted',chamber:'W07',slots:{'06':'W06','07':null,'08':'W08'},hold:['E02 設備故障'],count:'1／3'}, {
 start:node('故障訊息出現後，先保留現場與未完成結果。',{},[reject('重按完成，讓 Lot 往下走','W07 的結果未知、W08 未做。不能把故障當成完成。'),choice('依核准程序確認位置與安全取回','recovered','本例維護人員確認後取回 W07；原 Run 留下 Interrupted。')]),
 recovered:node('晶圓已歸位，仍缺少合格的製程結果。',{chamber:null,slots:{'06':'W06','07':'W07','08':'W08'},status:'Hold · 待工程處置'},[reject('設備恢復 Ready 就直接過站','設備恢復只說明設備可用；不會補上 W07/W08 的結果。'),choice('記錄工程處置，交重工評估','finish','保存原 Run 未完成結果，建立工程處置需求；尚未批准重工。')]),
 finish:node('保留目前位置，等待工程決定後續路徑。',{chamber:null,slots:{'06':'W06','07':'W07','08':'W08'},status:'Hold · 工程評估',hold:['E03 未完成作業處置']},[],'晶圓回到 FOUP，不代表加工成功。故障恢復與 Lot 處置必須分開。')
});
add('operations','hold','06 同時有兩個 Hold','解除一項不代表全解除','L023 尚未開始 S40。Q01 品質複核與 E02 工程確認同時阻擋開工。',{status:'Hold',hold:['Q01 品質複核','E02 工程確認']}, {
 start:node('先完成品質複核。',{},[reject('機台 Ready，直接開工','Lot 仍有兩個 Hold 原因；機台狀態不能覆蓋限制。'),choice('核准品質複核，解除 Q01','one','只解除 Q01；E02 仍保留。')]),
 one:node('剩下一個工程 Hold。',{hold:['E02 工程確認']},[reject('Q01 已解除，開始加工','E02 尚未解除，不能開工。'),choice('工程確認通過，解除 E02','finish','所有本例 Hold 原因解除；Lot 回到 Queued。')]),
 finish:node('可以重新進行開工確認；位置與 Step 均未改變。',{hold:[],status:'Queued'},[],'Hold 是原因集合；解除原因不會自動做 Track-in 或 Track-out。')
});
add('flow','bind','01 Lot 套用 Flow','產品、版本、起始位置','準備投入 L023，成員是 W06/W07/W08。產品 P-DEMO 核准使用 F-DEMO v1。',{flow:'尚未套用',current:'未建立',done:[],location:'STK01',status:'Created'}, {
 start:node('選擇這批使用的核准流程。',{},[reject('套用另一產品的 F-OTHER v1','產品與核准流程不匹配。沒有建立執行實例。'),reject('套用尚未發布的 F-DEMO v2 草稿','草稿不可投入本例的生產執行。'),choice('套用核准 F-DEMO v1','finish','建立 L023 的 FlowRef、起點 S10 與 Queued 狀態。')]),
 finish:node('L023 已有自己的流程位置。',{flow:'F-DEMO v1',current:'S10',status:'Queued'},[],'共用 Flow 定義；每批各自建立執行位置。換 FOUP 不會重建此流程。')
});
const normalNodes={};
STEPS.forEach((step,i)=>{
 const key=i===0?'start':'ready'+i;
 normalNodes[key]=node(`目前 ${step.id} ${step.name}。${i===4?'Stage B 已完成，還要完成確認階段。':''}`,{current:step.id,done:STEPS.slice(0,i).map(s=>s.id),status:'Queued',recipe:step.recipe},[reject('直接跳到下一個位置','尚無本站的完成證據；不能只改 Current。'),choice(`開始 ${step.id} ${step.name}`,'work'+i,`${step.id} Visit #1 開始；${i===5?'執行資料結案審核，不是機台加工。':'建立本次作業。'}`)]);
 normalNodes['work'+i]=node(`${step.id} 的必要作業與資料已可在本例確認。`,{current:step.id,done:STEPS.slice(0,i).map(s=>s.id),status:i===5?'Reviewing':'Processing',recipe:step.recipe},[choice(`確認 ${step.id} 完成`,i===5?'finish':'ready'+(i+1),`${step.id} Visit #1 = Pass。${i===5?'全部6站完成。':`推進 ${STEPS[i+1].id}。`}`)]);
});
normalNodes.finish=node('L023 的六站旅程完成。',{current:'結束',done:STEPS.map(x=>x.id),status:'Finished',recipe:'不適用'},[],'Flow 定義沒有被改寫；L023 留下6次完成紀錄，最後才標為 Finished。');
add('flow','normal','02 完整六站旅程','從 S10 一路走到結案','此情境省略實體搬送，location 表示教學待命載具位置。每站前置資格均已滿足；觀察流程位置與紀錄。',{current:'S10',done:[],location:'教學待命載具 F012'},normalNodes);
add('flow','branch','03 量測結果分流','缺資料、合格、不合格不同','L023 到 S50；本例先接收量測資料，再依結果決定去向。',{current:'S50',done:['S10','S20','S30','S40'],status:'Awaiting result'}, {
 start:node('請選一組量測結果，觀察後續路徑。',{},[reject('沒有結果，先到 S60','缺資料不能推定合格。Current 保留 S50。'),choice('收到合格結果','pass','S50 結果完整且合格；依正常規則推進 S60。'),choice('收到不合格結果','fail','保留 S50 Fail；套用品質 Hold，等待處置。')]),
 pass:node('下一站是 S60 結案，還沒完成整條 Flow。',{current:'S60',done:['S10','S20','S30','S40','S50'],status:'Queued'},[],'結果符合條件才能走正常出口。S60 尚需結案確認。'),
 fail:node('目前仍在 S50，品質結果沒有被抹掉。',{status:'Hold',hold:['Q01 量測不合格']},[],'不合格先進入處置流程；要重工或其他處置，需另外核准。可重設後比較另一分支。')
});
add('flow','rework','04 重工後回來複測','原失敗與新 visit 並存','起點：S50 Visit #1 = Fail。本例可評估 R10 清洗→S50 複測，最多1次。',{current:'S50',done:['S10','S20','S30','S40'],status:'Hold',hold:['Q01 量測不合格'],visits:'S50 #1 = Fail'}, {
 start:node('還沒有重工批准，不能自行倒退位置。',{},[reject('直接把 Current 改成 S10','S10 不是這次核准的重工 occurrence；原始失敗仍未處置。'),choice('工程核准 RW-001：R10→S50','clean','記錄重工原因、返回點與次數上限；轉入 R10。')]),
 clean:node('現在執行的是重工 R10，不是把 S10 的舊紀錄重用。',{current:'R10',status:'Queued · 重工',hold:[],visits:'S50 #1 = Fail；RW-001 已核准'},[choice('執行並完成 R10 清洗','retest','R10 #1 = Pass；依返回點回到 S50。')]),
 retest:node('請記錄 S50 第2次 visit 的結果。',{current:'S50',status:'Awaiting retest',hold:[],visits:'S50 #1 = Fail；R10 #1 = Pass'},[choice('S50 Visit #2 合格','finish','追加 S50 #2 = Pass，前次 Fail 保留；推進 S60。'),choice('S50 Visit #2 仍不合格','limit','追加 S50 #2 = Fail；已用完本例的1次重工額度。')]),
 limit:node('不能自動無限重工。',{status:'Hold',hold:['Q02 重工次數已達上限'],visits:'S50 #1 = Fail；R10 #1 = Pass；S50 #2 = Fail'},[reject('再走一次相同重工','已達 RW-001 的1次上限。須新的工程處置，不能循環直到變綠。')],'保留兩次失敗，等待新的工程決策。'),
 finish:node('完成重工複測，進入 S60。',{current:'S60',status:'Queued',hold:[],done:['S10','S20','S30','S40','S50'],visits:'S50 #1 = Fail；R10 #1 = Pass；S50 #2 = Pass'},[],'重工追加可追溯的新歷程；成功不會覆寫原始 Fail。')
});
const splitLots=[{id:'L023-A',current:'S50',wafers:['W06','W07']},{id:'L023-B',current:'R10',wafers:['W08']}];
add('flow','split','05 拆批與重新合批','三片保持唯一，進度須對齊','起點 S50；W08 需要已核准的 R10 支線，另兩片留在 S50 等待。',{current:'S50',done:['S10','S20','S30','S40']}, {
 start:node('依成員拆成兩個活躍子批，父批保留譜系。',{},[choice('拆成 A：W06/W07；B：W08','separated','父批 L023 停用為活躍批次；A、B 合計仍是3片，無重複。')]),
 separated:node('A在 S50，B在 R10，目前進度不同。',{lot:'L023（父批）',status:'Split · 非活躍父批',current:'子批各自執行',lots:splitLots},[reject('立刻合批','A與B的 current occurrence 不同。不能把 R10 尚未完成的 W08 當作已到 S50。'),choice('B 完成 R10，回到 S50','aligned','B 的 R10完成記錄保留；兩子批現在都在 S50 等待。')]),
 aligned:node('兩子批的產品、Flow v1、位置與可合批狀態都相同。',{lot:'L023（父批）',status:'Split · 子批待合併',current:'子批同在 S50',lots:splitLots.map(l=>({...l,current:'S50'}))},[choice('驗證條件，合成 L023-M','finish','兩子批結束為活躍批次；建立 L023-M，三片成員與父子來源可反查。')]),
 finish:node('合併後仍在 S50 等待量測。',{lot:'L023-M',current:'S50',status:'Queued',genealogy:'L023 → L023-A／L023-B → L023-M'},[],'合批整合的是符合條件的批次；不會消除 B 走過 R10 的事實。')
});
add('flow','version','06 流程改版與遷移','發布不會靜默修改 WIP','L023 已做完 S40，依 v1 等待 S50。v2 在 S40 與 S50 之間新增 S45 檢查。',{current:'S50',done:['S10','S20','S30','S40'],otherLot:'L024 尚未投入'}, {
 start:node('先發布已核准的新定義。',{},[choice('發布 F-DEMO v2','published','v2 已發布；L023 的 FlowRef 仍是 v1。')]),
 published:node('決定新批套用與既有批遷移。',{otherLot:'L024 新批可套用 v2'},[reject('所有在製批自動換成 v2/S50','發布與遷移是不同交易；還會漏掉新增 S45。'),choice('L024 新投入套用 v2','newlot','L024套用v2，起始S10；L023仍用v1/S50。')]),
 newlot:node('L023 是否遷移，需要明確的批准與位置對照。',{otherLot:'L024：F-DEMO v2／S10'},[choice('核准遷移：v1/S50 → v2/S45','finish','確認 S40 已完成且需補 S45，保存 MIG-001；L023改為v2/S45。')]),
 finish:node('L023 必須先做新增的 S45。',{flow:'F-DEMO v2',current:'S45',status:'Queued',otherLot:'L024：F-DEMO v2／S10',migration:'MIG-001：v1/S50 → v2/S45'},[],'新定義、Lot 套用與在製遷移分開管理；保留原版本的已完成歷程。')
});
add('flow','qtime','07 等待超過 Q-time','時間從指定事件持續計算','教學門檻：S20 完成到 S30 開始最多30分鐘。起點已過20分鐘；沒有暫停時鐘的規則。',{current:'S30',done:['S10','S20'],qtime:20,location:'STK01'}, {
 start:node('可在期限內開工，或模擬延遲。',{},[choice('現在開工 S30','ontime','20 ≤ 30，本例時間條件符合；S30開始。'),choice('再等待25分鐘','expired','累計45分鐘，超過30分鐘；套用QT01限制。')]),
 ontime:node('已於期限內開始本次作業。',{status:'Processing',qtime:20},[],'計時終點是 S30 開始事件。是否符合仍需其他開工條件，本例假設已確認。'),
 expired:node('45分鐘已經發生，畫面重設不能消除歷史。',{status:'Hold',hold:['QT01 等待超時'],qtime:45},[reject('將計時歸零後開工','原 S20 完成時間不可被這個操作改寫。45分鐘仍保留。'),choice('送工程評估，保留45分鐘','finish','建立超時評估紀錄；未批准後續處置，仍維持Hold。')]),
 finish:node('等待工程評估，不自行決定能否繼續。',{status:'Hold · 待處置',hold:['QT01 等待超時'],qtime:45},[],'Q-time 是兩個明確事件間的約束；是否可豁免或補救依核准規則決定。')
});
add('flow','skip','08 想跳過必要量測','做過蝕刻不代表已有品質證據','S40 已完成，L023在 S50。這個 Flow 的 S50 是必要量測，沒有核准的替代證據。',{current:'S50',done:['S10','S20','S30','S40']}, {
 start:node('交期很緊，能直接去 S60 嗎？',{},[reject('用急單理由跳到 S60','優先權不取消必要 Step。沒有 S50 的結果，不允許推進。'),choice('完成 S50 量測並確認合格','finish','新增有效 S50完成記錄；按正常出口推進 S60。')]),
 finish:node('保留必要證據後才到 S60。',{current:'S60',done:['S10','S20','S30','S40','S50'],status:'Queued'},[],'合法跳站必須有明確授權與條件。本例不允許跳 S50；不是所有 Step 都能用急單豁免。')
});
add('flow','revisit','09 同一作業再次出現','Operation 相同，位置不同','S10 CLEAN 已完成；工程批准現在執行 R10 CLEAN。名稱相同但 occurrence 不同。',{current:'R10',done:['S10','S20','S30','S40'],status:'Queued · 重工',visits:'S10 #1 = Pass；R10 尚未執行'}, {
 start:node('R10 能沿用 S10 的完成紀錄嗎？',{},[reject('CLEAN 做過了，沿用 S10 Pass','S10與R10是不同位置，晶圓已經歷其他作業；舊Pass不能證明這次已做。'),choice('建立並完成 R10 Visit #1','finish','追加R10 #1 = Pass；依已核准返回點回S50。')]),
 finish:node('兩個 CLEAN occurrence 各有自己的紀錄。',{current:'S50',status:'Queued',visits:'S10 #1 = Pass；R10 #1 = Pass'},[],'相同 Operation 可出現多次；流程位置、visit 與實際條件共同界定一次作業。')
});
add('flow','dispatch','10 急單與合格候選','排程優先權不能越過限制','L023（一般）與 L024（急單）都在 S40；只有L024有品質Hold。設備目前只能接一批。',{otherLot:'L024：S40／高優先／Hold Q01'}, {
 start:node('從可執行候選中選下一批。',{},[reject('L024比較急，忽略Hold先做','優先權只是排序依據，不能覆蓋品質限制。L024仍Hold。'),choice('選無Hold且資格符合的 L023','finish','L023開始S40；L024仍停在S40且保持Hold。')]),
 finish:node('兩批位置相同，執行狀態仍各自獨立。',{status:'Processing',otherLot:'L024：S40／高優先／Hold Q01'},[],'先篩選可執行資格，再排序。Flow描述路徑；Dispatch決定合格候選中誰先做。')
});

class ScenarioEngine{
 constructor(scenario){this.scenario=scenario;this.reset();}
 reset(){this.nodeId='start';this.events=[{kind:'start',text:this.scenario.context}];this.feedback='先看起始條件，再選擇操作。';this.kind='';}
 get node(){return this.scenario.nodes[this.nodeId];}
 get state(){return structuredClone({...this.scenario.base,...this.node.state});}
 act(index){const a=this.node.actions[index];if(!a) return false;this.kind=a.next?'accept':'reject';this.feedback=a.message;this.events.push({kind:this.kind,text:a.message});if(a.next)this.nodeId=a.next;return Boolean(a.next);}
}
if(typeof module!=='undefined')module.exports={SCENARIOS,ScenarioEngine};
