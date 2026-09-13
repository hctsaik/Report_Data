# MES-020 右側展開

右側頂部新增「展開右側 ↗」。點擊後整個圖與說明區進入大視窗，主詞說明自動打開，關聯圖依可用寬度重排，參考圖最多1100px寬。頂部「收回右側 ↙」固定可見，Escape也能返回。

使用原始 inspector DOM，不複製圖片或互動，保留當前主詞、關係分頁與既有放大功能；關閉後恢復原說明收合狀態、位置與按鈕焦點。原圖與教學內容不變。

驗證 python workitems/mes-020/check.py：1440／390 展開與返回、Escape、WPH說明、巢狀插圖放大、主詞與分頁保留、無水平溢出及JS錯誤均通過。實看 tests/evidence/mes-020/1440-explanation.png、390-expanded.png；沒有宣稱教學品質分數。使用者審閱pending。
