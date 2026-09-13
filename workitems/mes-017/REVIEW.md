# MES-017 主詞關聯 ER

## 結果

使用者要求 Multi-agent 先思考畫法，再更新網站。語意 agent 核對來源與完整 Recipe 路徑；布局 agent 提議桌面加寬、手機直向重排，並實看五主詞的桌面／手機圖。已整合至 er-atlas.html，舊 integrated-map.html 入口保持可用。

選 Lot／FOUP／EQP／Flow／Recipe 或任意來源節點，右側重新繪製以它為主詞的關聯 ER。保留矩形、菱形、橢圓及原始標籤。Lot 首頁包含 FOUP 與設備；FOUP 首頁包含 Lot 與設備位置。Recipe 保留 SYSTEMKEY → FRMRCP_EQP → EQP_ID → FREQP。點小圖可再換主詞，搜尋及不同 schema 的框選位置亦可切換。現場插圖收合為補充。

圖以關係支線整理，同一實體可能因不同關係重複顯示，已在圖說明示；不宣稱已展示相關端點之間的所有間接關係。桌面每頁四支線、手機兩支線，分頁在圖上方，手機先看關聯圖再看完整 ER。提供獨立放大視窗。

## 本輪發現與修正

- EQP 菱形長表名碰斜邊：依實際行長與菱形幾何增加高度，保留完整文字。
- 手機四支線太長：改兩支線，保留可見分頁，FOUP 優先看 Lot／位置。
- 相同 FOUP、LR 多次出現：加入同一 entity 重複呈現的說明。
- 手機點 ER 後自動捲動產生相容 click，誤觸新出現的小圖節點：小圖點擊要求該節點實際收到 pointerdown，鍵盤仍由 Enter／Space 操作；以真實觸控回歸。
- 舊測試讀收合區 innerText 為空：本轮適配檢查 textContent，插圖操作先展開；不修改歷史測試或證據。

## 驗證與證據

執行 `python -X utf8 workitems/mes-017/check.py` 與 `python -X utf8 workitems/mes-017/regression.py`。最終兩項皆 PASS：1440／390 五主詞各含按鈕與真實滑鼠／觸控；每個尺寸遍歷 121 個根、281 條支線；MES-014 的來源完整性、17 路徑與五題，以及 MES-015／016 的框選與真實點擊回歸全部通過。結果見 tests/evidence/mes-017/verification.json 及 regression-* 下 verification.json。回歸包重用原 014／015／016 assertions，將新證據輸出到本輪目錄，避免覆寫歷史證據。

來源審查實際遍歷全部 121 個根節點，所有支線中的邊均對應原 model；詳 AGENT_SEMANTIC.md。前端語法通過 node --check。原七張 SVG、完整整合 SVG 與 model 未修改。

工具限制：內建 Browser runtime 未發現可用瀏覽器，經 discovery 確認為空；採專案既有 Playwright 測試本機 HTTP。工具 tools/validate_teaching_preflight.py 硬編碼 MES-004 的十五頁，不可用其 PASS 替 MES-017 背書；本輪 preflight 寫於 PLAN.md。

## 審閱狀態

已對桌面／手機實際成图檢視並修正上述缺口。未重新評分整套教學、舊現場插圖或所有次級分頁；不引用歷史高分宣稱本輪達標。使用者驗收 pending。

限制：來源沒有 Wafer entity，頁面已說明，未捏造 Wafer 表與連線。一般支線遇到下一個非菱形節點停止，可點該節點繼續；Recipe 是有明確來源路徑的多段特例。手機仍需向下閱讀兩條支線，完整 ER 的小字仍需放大。

補充最終檢查：final_checks.py 在 390／360／950 寬度通過小圖鍵盤、觸控與不同來源位置切換。主 agent 實看 390-equipment-page2.png：預派長表名完整位於菱形內，窄版換行但未裁切；另複查 Flow、Recipe 的手機鏈及桌面圖。
