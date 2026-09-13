# ER 原圖 SVG 重畫

來源為 `../ORG/2671.jpg` 至 `2677.jpg`；七張 SVG 與原圖同名。這輪是原圖轉繪，不是另編教學投影片，保留矩形／菱形／圓形、藍色核心物件與無向連線，不新增基數或 SQL join 語意。移除照片中的螢幕介面、透視、摩爾紋與浮水印；調整間距、字型與換行以便閱讀。

開啟 [index.html](index.html) 可切换七張圖、縮放及對照原照片。SVG 不嵌入照片，文字可選取、搜尋和編輯；可用瀏覽器或向量編輯器開啟。

**疑義文字已全部確認**：使用者分兩輪確認 13 項疑義，已套用更正並移除橘色標記。詳細位置與校字歷史見 [UNCLEAR_TEXT.md](UNCLEAR_TEXT.md)。明顯但可辨讀的原圖差異沒有自行修正，例如 2676 的 PORT → FRPORT_UDATA 關係仍標 EQP_ID。不能直接把這些圖當可執行 SQL 規格。

維護來源：`redraw.py` 是手工轉錄的節點和連線，`transcription.json` 是同一份轉錄輸出。需修改文字時，先更新 `redraw.py`，再執行 `python ER/NEW/redraw.py` 與 `python ER/NEW/verify.py`。原圖未修改。

本輪驗證記錄在 `verification.json`，瀏覽器預覽截圖在 `preview/`。檢查包括七份 XML、無嵌入點陣圖、節點與文字範圍及原圖 SHA-256；不把格式檢查當作不清楚文字已辨識。
