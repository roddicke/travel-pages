# 更新流程（給 Claude 的 session 用）
1. add_repo roddicke/travel-pages（push 權限）並 clone。
2. 用 Artifact read 把各頁最新 HTML 存到本機（artifact 網址與檔名對照見 build.py 的 P 清單；列車頁含 photos/）。
3. `npm i d3@7.8.5 topojson-client@3.1.0 three@0.128.0`（到 /tmp/lib），修改 build.py 頂端的路徑後執行，會內嵌函式庫、改相對連結、產生 index.html。
4. 斷網驗證 → commit → push main。
