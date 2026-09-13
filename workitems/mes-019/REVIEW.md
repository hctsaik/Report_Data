# MES-019 機群 WPH

已依使用者提供的公司定義重畫專屬參考圖：生產管理部門為每個機群定義 WPH（wafer per hour），表示預期每小時晶圓產出量。三段為生管訂標準 → 指定機群 → 每小時預期產出；沒有杜撰具體 WPH 數值或個別機台加總。

內建 imagegen 生成桌面 assets/mes-019/group-wph-v1.png，並從此圖重排手機 group-wph-mobile-v1.png。原 FOUP 位置圖未修改。主 prompt 保存於 prompt.txt；手機 prompt 要求相同內容改為三段垂直構圖，保留大字、機群共同邊界與黃色結論，不補測量結果。

網站明確映射 2673:wph／wph-link，選取時自動打開專屬參考圖；小圖 WPH 名稱改成機群 WPH 定義，原 model／SVG 的標籤保留來源稽核。原資料連線不等於已確認的業務歸屬或 Join，頁面明示不能推成 LR 定義個別機台產出。未自行展開 IE 縮寫。

入口：er-atlas.html?view=original&subject=wph。測試 workitems/mes-019/check.py，證據 tests/evidence/mes-019，涵蓋1440／390的WPH節點、關係節點、專屬圖與放大、Lot原圖保留。語法檢查 node --check er-atlas.js、er-focus.js。

實圖檢視：桌面三段語意、主要字句、機群框及每小時單位一致；手機初版橫圖字太小，改用直向圖。圖內機台與晶圓數量僅為示意，圖說已標明。使用者審閱 pending，未以功能 PASS 宣稱品質評分達標。
