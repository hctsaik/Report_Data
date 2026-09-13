# MES-018 裝載關係修正

使用者指出 FOUP →「Lot 在 Foup 內／Siview.frcast」→ Step 歷史畫錯，指定正確裝載關係為 LOT（Siview.Frlot）— 放在（Siview.Frcast_lot）— FOUP（Siview.Frcast）。

計畫：從主詞小圖雙向撤下 2672:cast-link 支線；保留 2671:lot／cast-link／cast 的真實裝載關係。核對 FOUP 所有分頁、Lot 與 Step 根的展開，保存桌面／手機證據。

已修改 er-focus.js 的鄰接規則。撤回支線不再由 FOUP、Step 或關係節點展開；未將 Step 歷史改名成 Lot，也未將 FRCAST 改冒充 FRCAST_LOT。原始 SVG／model 保留來源稽核，不把歷史來源視為已獲使用者確認的教學內容。

本次是對 MES-017 語意審查的修正：來源邊存在只能證明可追溯，不能證明教學意義正確。使用者已否定該支線，舊語意通過不適用此判斷。使用者重新審閱 pending。

驗證：python -X utf8 workitems/mes-018/check.py；證據 tests/evidence/mes-018。原有功能回歸另存本輪，不覆寫舊版截圖與 manifest。

最終結果：桌面1440／手機390皆PASS。Lot／FOUP正確裝載鏈存在，所有分頁不再顯示撤回支線；全部121根與277條展開支線檢查通過。五主詞真實mouse／touch及放大、換主詞回歸通過，無JS錯誤。已實看1440-carrier.png、390-lot.png，裝載關係使用Siview.Frcast_lot。
