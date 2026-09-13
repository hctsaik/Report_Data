# MES-033 原始與presum傳送歷史圖文

使用者確認MFG_Carrier_Te_Ut為presum過的傳送資料，MCS為原始傳送歷史，概念相近。兩者各有說明與圖說，共用本次專門製作的來源/整理比較圖，不再只有文字或互動路線。

新圖assets/mes-033/transfer-history-v1.png及transfer-history-mobile-v1.png。三段：現場FOUP搬運→MCS原始歷史→presum資料；箭頭是概念整理關係，不宣稱已核對SQL流程。未推定presum分組/加總/保留欄位與原始一對一。MCS原有Macro/Micro互動保留。
imagegen提示要求三段具體fab場景、同F012、白底藍框/黃色結語，無自造欄位或時間；手機依桌面重排。兩生成圖已實看，來源exec-779d282e-c257-4704-826e-4de060bdaf40.png與exec-afb93e3e-e1b9-4950-9d62-837adca18966.png。未改舊圖片。

python workitems/mes-033/check.py：1440/390四節點真實搜尋切換、圖文可見、正確手機/桌面放大與MCS互動通過。MES-031回歸通過。手機presum說明截圖已實看。證據tests/evidence/mes-033，未自動評分，使用者審閱pending。一次性integrate.py不重跑。
