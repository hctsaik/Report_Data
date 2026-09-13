# MES-025 Qtime包含Lot與專屬教學

使用者要求Qtime關聯圖包含Lot，並介紹Qtime，取代不相關FOUP位置插圖。

來源：advanced.js#qtime、workitems/mes-009/CONTENT.md。Qtime是同一Lot指定起訖事件間的時間限制，不一律等於排隊時間。例子沿用L023：10:00起算、最大30分鐘、10:30截止，明示示例而非廠內通用限制。停止事件與逾時處置依實際規則，不能假定Hold自動重設。

圖的來源路徑：2672:qtime — qtime-link — step — summary — 2671:lot，全部已有原始邊。Qtime及Qtime站點節點皆顯示必要Lot上下文。

參考圖採用已存在assets/mes-009/qtime.png。手機用內建imagegen以原圖重排直向；C解釋型三節點：Lot起算事件、同Lot計時、指定停止事件，沿用原圖白底、具體設備、大字與黄色重點。預設正文補定義、查歷史要核對哪些條件、30分鐘示例及完整教材入口。原圖不重製覆寫。

驗證：桌面／手機Qtime完整鏈、每邊來源、真實點選、專屬图、放大、Lot存在、30分鐘示例及先前修正不回退；保存tests/evidence/mes-025。使用者審閱pending，不重評整套教學。
