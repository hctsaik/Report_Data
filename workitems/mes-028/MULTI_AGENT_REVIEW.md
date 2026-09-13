# Multi-agent 閱讀動線審查

## focus_review（只讀）

缺口是閱讀歷程，不是單一 history.back：selectNode 重設主詞及view，ER_FOCUS.show重設關係page；route/entity/overview沒有共同狀態。放大圖只可關閉，不能就地返回主詞。
建議保存 mode/id/page/walkIndex/view/scroll/details；返回附目的名稱、全圖出口、最近瀏覽路徑。frameEntity內部overview不得形成重複歷史。關係分頁稱「組」，不要混同頁面導航。

## nav_review（跨頁審查及實作）

ER直連advanced、data-map，來源主詞丟失；教材只能回generic ER或首頁。
新增er-return.js及七個目的頁引用，使用同源sessionStorage token，提供返回ER主詞與課程首頁，課內切换繼續攜帶來源。
Agent回報node語法檢查及390px七頁測試通過，包含無token直接進入、外站返回URL拒絕、QTime切Future Hold仍保留返回。

## 主agent整合與驗證

新增er-navigation.js，保存檢視歷程並與browser history整合；跨頁返回重建歷程。桌面手機真實操作測試見check.py。導航恢復分頁／縮放；放大圖內返回保持視窗層級。
瀏覽路徑代表讀者走過的檢視，沒有冒充資料父子關係。
