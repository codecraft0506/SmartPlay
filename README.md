# SmartPlay

## 環境設定

### 套件安裝

1. 下載 Firefox 瀏覽器
2. 到主程式目錄開啟終端 pip install -r requirement.txt

### Discord Bot

1. 開一個伺服器
2. 點選 [此處](https://discord.com/oauth2/authorize?client_id=1289442925909901344&permissions=8&integration_type=0&scope=bot) 並將機器人加入你的伺服器
3. 在伺服器左欄的任一個文字頻道上點擊右鍵開啟選單，點選最下方「複製頻道 ID」
4. 將 ID 貼入 config.json > discord > id 

## 注意事項

1. 系統預設搶最新日期的場地，例: 10/10 執行會搶 10/15 的場地
2. 目前是手動開啟即開始搶票，若要排程定時請把下面主執行函式被註解掉的程式碼取消就好
3. 系統輸入卡號後，bot會傳送訊息要求你輸入驗證碼，請 @smartplay 並輸入驗證碼
