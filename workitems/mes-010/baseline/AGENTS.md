# 最新接續：MES-009

本輪新增 advanced.html：QTime、Future Hold、Part／RouteId、LR／ER／Physical，以及原版＋三種 Flow 候選。先讀 workitems/mes-009/PLAN.md、CONTENT.md、REVIEW.md。檢查 python tests/check_advanced.py（90項）。使用者選版 pending，Part／LR／ER 的內部字典 pending；頁面已明示教學假設。新圖 assets/mes-009，原 stage-v2.png 保留。MES-008 入口與新鮮度資產未改，root 共用文件新增內容後，其旧 manifest 不再代表當前全部文件。不得重跑舊生成器覆蓋新內容。

# 最新接續：MES-008

先讀 workitems/mes-008/PLAN.md 及 TEACHING_REVIEW_LOG.md 最新段。使用者再次退回資料新鮮度，MES-007 新鮮度的頁面／圖像高分與通過判斷已撤回。MES-007 manifest 是歷史版本快照；本輪修改後不要求它與新 freshness 檔相同，不覆寫歷史 hash 掩蓋差異。新證據用 tests/evidence/mes-008。前三課本輪不改。沿用使用者重製授權，必須實際改網頁與圖，不只寫反省。MES-008六節與12張主圖已更新，逐頁評比見 workitems/mes-008/REVIEW.md、review.json。驗證 python tests/check_freshness_v2.py；封存一致性 python tools/verify_mes008_evidence.py。使用者審閱 pending。

# MES 教學製作的接續規則

先讀 CLAUDE.md、IMAGE_STYLE_GUIDE.md、TEACHING_WEBPAGE_GUIDE.md、TEACHING_SCORING_RUBRIC.md、TEACHING_REVIEW_LOG.md 與 WORKITEMS.md 最新段落。

歷史版本 MES-007：使用者授權重製15頁並新增資料新鮮度。先讀 workitems/mes-007/PLAN.md、REVIEW.md 與 evidence-manifest.json。新主插畫在 assets/mes-v3；freshness.html 為第四課。MES-004品質通過已撤回，不作完成依據；MES-006為歷史比較基準。MES-007使用者審閱仍 pending。

使用者第二次指出品質失敗。不得再以部分圖片評分或功能 PASS 宣稱整批教學完成。每個指定 URL 是獨立驗收單位；lab 還須覆蓋全部情境的可見狀態。每頁與每張主圖分開記錄實際桌面／手機證據、分項分數、缺口、修正。未看寫未評估，不能自動填分。

歷史MES-007證據檢查為 `python tools/verify_mes007_evidence.py`，不適用MES-008的新鮮度檔案；它只查範圍、資產與證據一致，不自動評品質，不代表使用者核准。舊 MES-004 validator 不適用新版本。任何共享渲染程式改動後，舊截圖須重驗，不能繼續使用過時證據。
