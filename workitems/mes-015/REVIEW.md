# MES-015 完整 ER 與現場對照

入口：integrated-map.html?view=original → er-atlas.html?view=original。

完成：初始完整全圖；Lot／FOUP／EQP／Flow／Recipe 框選主要資料位置，全部原連線保留；可另外放大各框選位置；同步既有現場插圖、圖說、教學連結與可關閉的大圖。任意節點僅明確映射時使用專題圖，其餘標示基礎參考。

驗證：tests/check_er_atlas.py 的 128 原節點及原邊映射、121 實際節點、128 實際線、17 路徑及五題於桌面/手機通過。workitems/mes-015/check.py 通過 1440/390 的五種框選、全圖維持、所有節點及邊可見、插圖開關、放大、清除、resize、Recipe 與未知節點回歸。新截圖及結果在 tests/evidence/mes-015。

兩位 agent 審查：語意初審抓出 Recipe 誤用 Stage 圖，以及未知節點誤用 Lot 特定圖說，均已修正並加回歸。後續建議的「基礎參考」提示也已加入。視覺初審87，修正手機第一屏後92（詳 AGENT_VISUAL.md），不是使用者驗收。原 SVG 未修改；未重新宣稱每張既有插圖的獨立品質分數。

限制：完整總覽用於定位，讀表名要放大；手機兩圖上下對照。五類框選是主要物件入口，並非所有相關報表的完整同義詞索引。

基準來源保存在 baseline。update.py/refine.py/fallback.py 為本輪一次性修改紀錄，不可重跑覆蓋後續版本。
