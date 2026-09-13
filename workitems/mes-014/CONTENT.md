# 真正的整合 ER：內容與色彩規則

七張來源的128節點映到121個實際SVG節點；只合併六組完全相同、包含schema的表識別。128條來源邊皆在實際SVG中，原關係菱形、實體矩形與概念／屬性橢圓保留。不同表不因同樣描述Lot或設備就合併。

框線用於辨認：Lot藍、FOUP綠、設備與子資源橙、流程與配方紫、紀錄／統計灰；關係與鍵的菱形為中性灰。Tool與EQP統一設備類別，未另造Tool實體。同色不表示同表、相同狀態或已證明Join。Hold與forecast／stream等紀錄不因名稱含Lot／Flow就套核心實體色。

資料圖本身不增加物理推論線。解釋沿原始關係：LOT—FRCAST_LOT—FOUP說明裝載；FOUP—CSFHDOPHS—EQP說明原圖位置關係；FOUP—CSFRPREDISPATCH—EQP說明預派。三條不能合併為通用關聯。直接點選分支時，說明面板按每條真實邊列兩端，不能用平坦節點清單假裝路徑。

來源未列schema的FREQP、MFG_EQP_BAY_BT等即使名字相同，保留各自來源節點；圖上明示未列schema。SYSTEMKEY、EQP_ID依原上下文保留，不作全域鍵合併。FRMRCP和FRMRCP_EQP仍是配置，不補出Physical Recipe實際執行。

17個可閱讀路徑包含裝載、Slot、位置、預派、預到、交接、Flow、LR、PD、ER、Chamber、Future Hold、Move/WIP、搬送、Qtime、快照、OEE；五個題目使用相同圖座標與既有路徑。

長路徑全貌只能看結構。當fit後低於80%顯示比例，自動以90%沿線閱讀，透過上一點／下一點定位。文字投影約18px，避免以小字完整縮圖冒充可讀圖。片段外相鄰节点可用導覽／平移查看；全圖所有節點仍在SVG內。分支巡覽走DFS真實邊，返回中心再走下一枝，不跨不存在的邊。

原始圖號保留在展開來源面板，畫布不列「原圖2671／…」。獨立小字fhwlths註記也保留於来源說明。
