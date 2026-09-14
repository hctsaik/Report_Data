# MES-057 ER 頁面重製

指定入口：er-atlas.html?mesFrom=mu1i1b25a547qm&erNode=t_cfc81de70314（Lot）。
基準：Git 15654c9；實看 tests/evidence/mes-057/before-{1440,390}.png。
問題：桌機圖面起點約869px，手機超過1000px；工具過多。Lot 誤被歸入單元8。

計畫：保留上下兩區與原SVG/JSON。集中主詞和搜尋、縮短頁首；圖例與匯出收在讀圖指南，縮放維持可見；下方保留關聯圖與教學。只有 view=questions 的 ER 入口屬單元8。原生HTML/CSS改版，不生成插畫或改資料關係。

驗證：指定深連結雙尺寸首屏、關聯圖、解說截圖；343項既有行為回歸；首屏可見圖面、指南、課綱歸屬檢查。原圖雜湊不變。完成後提交並更新GitHub Pages、確認公開資產。
使用者審閱 pending；不以功能測試宣稱教學評分。
