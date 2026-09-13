# MES-017 主詞關聯 ER

使用者授權：先起 Multi-agent 思考畫法，再更新網站。選主詞後，在旁邊重新排版其相關 entity；Lot 可包含 FOUP、Tool 等其他物件。

## 設計與 preflight

- 目標：讀者能沿原始關係說明主詞與其他資料實體如何相連。
- C 解釋型：主詞 → 關係／鍵 → 相關實體 → 來源限制。這四個閱讀角色構成主線；依使用者指定保留真正 ER 多節點，不套用投影片三卡限制。
- 參考：現有 er-atlas 完整 ER 的矩形、菱形與來源文字；index.html#fab 的主體與細節對照方式。保留白底、明確焦點、充分圖面空間。
- 黃色重點：連線表示來源資料關係，不代表加工順序或已發生事件。
- 主圖為原生 SVG，按選取重新排版，不生成點陣插圖。原七圖及整合 SVG 不改。
- 語意與布局由獨立 agent 提議，根 agent 整合並驗證。詳 AGENT_SEMANTIC.md、AGENT_LAYOUT.md。
- 來源 packet：ER/INTEGRATED/er-model-v2.json、er-atlas.js routes。
- Wafer 未列於來源，不偽造節點與關係；不同 schema 身分保持分開。

## 實施

1. 新增聚焦子圖模組，依 canonical ID 展開真實關係，保留中介節點、完整標籤與來源邊。
2. 接入主詞按鈕、完整 ER 點擊、搜尋、小圖內改主詞；完整 ER 保留定位用途。
3. 桌面左右對照，手機先顯示主詞小圖；舊現場圖收合為補充。
4. 測真實 mouse/touch、五主詞、換主詞、所有節點、Recipe 完整鏈、桌面手機與原功能回歸。
5. 保存新證據與審查；使用者驗收 pending。

## 環境紀錄

CLAUDE.md 提及的 .ai-product-workflow 及專案 .claude/skills/ai-product-workflow/SKILL.md 在目前工作目錄不存在；未宣稱寫入不存在的 SQLite 工作流。採既有 workitems 與 OpenSpec 留存本輪紀錄。
