# SmartPlay

## 環境設定指南

### 1. 套件安裝

1. 下載並安裝 [Firefox 瀏覽器](https://www.mozilla.org/firefox/new/)。
2. 在主程式目錄中打開終端，執行以下指令安裝依賴套件：
   ```bash
   pip install -r requirements.txt
   ```

### 2. 前置作業

1. 建立一個 Discord 伺服器，或使用已存在的伺服器。
2. 點擊 [此處](https://discord.com/oauth2/authorize?client_id=1289442925909901344&permissions=8&integration_type=0&scope=bot) 並將機器人加入你的伺服器。
3. 在 Discord 伺服器的文字頻道上，右鍵點擊頻道名稱，然後選擇「複製頻道 ID」。
4. 將複製的頻道 ID 貼入 `config.json` 檔案中的 `discord > id` 欄位。

---

## 使用說明

### 1. 設定 config.json 檔案

- 在 `config.json` 檔案中填寫必要的參數：
  - 帳號、密碼
  - 體育館
  - 時段
  - 設施
  - 信用卡資訊
- 如需多開場次，則添加多組參數。

範例請參考目前 `config.json` 格式

### 2. 執行程式

1. 確認 `config.json` 設置正確。
2. 在終端中執行以下指令啟動程式：
   ```bash
   python main.py
   ```
3. 當系統輸入卡號後，機器人會傳送訊息請求你輸入驗證碼。請在 Discord 頻道中 @smartplay 並輸入驗證碼以完成操作。
---

## 注意事項

1. **預設場地日期**：系統預設會搶最新日期的場地。例如：在 10/10 執行時，會自動搶 10/15 的場地。
2. **手動與排程搶票**：系統啟動後即開始搶票。若需要排程執行，請取消主程式中被註解掉的排程程式碼。

