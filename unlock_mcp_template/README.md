# UNLOCK Morning Program — MCP Server (ノーコード寄りテンプレート)

このテンプレートは **FastAPI + fastapi_mcp** を使った最小構成の **MCPサーバ** です。
ChatGPTの **Apps in ChatGPT** からこのサーバを接続すると、
「UNLOCK朝プログラム」をツールとして呼び出せます。

---

## 1. ファイル構成
```
unlock_mcp_template/
├─ api/
│  └─ index.py           # FastAPI + MCP 本体（Vercel用のエントリ）
├─ .well-known/
│  └─ mcp.json           # MCPサーバの定義（Appsに登録しやすくするため）
├─ requirements.txt      # 必要ライブラリ
├─ vercel.json           # Vercel用の設定
└─ README.md             # この説明書
```

---

## 2. デプロイ手順（Vercel推奨・無料枠OK）

1. **Vercelアカウント作成**（無料）  
   https://vercel.com/ にアクセスし、GitHub連携でアカウント作成。

2. **GitHubにこのフォルダを新規リポジトリとしてアップ**  
   リポジトリ名例：`unlock-mcp`

3. **Vercelで「New Project」→ GitHubの `unlock-mcp` を選択 → Deploy**  
   - 設定はデフォルトのままでOK
   - デプロイが終わると、`https://<your-project>.vercel.app/` のURLが発行されます

4. **動作確認**  
   - ブラウザで `https://<your-project>.vercel.app/health` を開いて `{"status":"ok"}` が出れば成功
   - `https://<your-project>.vercel.app/.well-known/mcp.json` でMCPのメタ情報が表示されます

---

## 3. ChatGPT側の設定（Apps in ChatGPT）

1. ChatGPTのメニューから **Apps** を開く  
2. **Add an app via MCP**（または「外部サーバを追加」）を選択  
3. 以下の情報を入力：
   - **Server URL**: `https://<your-project>.vercel.app/`
   - 自動で `.well-known/mcp.json` が読まれ、ツール `run_morning_program` が認識されます

> 🔐 認証は今回オフ（PUBLIC）です。必要になればBearer Token等の設定を追加します。

---

## 4. 使い方（ChatGPT内）
アプリが追加されると、会話中にモデルがツール **run_morning_program** を呼べます。  
引数に `difficulty`（"easy"|"standard"|"hard"）を指定可能です。未指定は "standard"。

### 例）モデルの内部的な呼び出し（イメージ）
```json
{
  "tool": "run_morning_program",
  "arguments": {"difficulty": "standard"}
}
```

戻り値（JSON）には、
- 日付、セクション（ZEN/ライフキネティック/プレゼンティズム/リフレクション）
- 各セクションの手順、タイムキュー
- 受取確認の文言
が含まれます。モデルはこのJSONを元に、人に優しい文章で整形して提示します。

---

## 5. よくある質問

### Q. 料金はかかりますか？
- Vercel無料枠で十分に動かせます（トラフィック増で上限に達したら有料検討）。
- ChatGPTはPlus/Team/Enterpriseプランに依存します。

### Q. LINEやNotionに記録したい
- `api/index.py` の `run_morning_program` 内で、
  LINE Messaging API / Notion API / Google Sheets API を呼ぶコードを追加すればOKです。

### Q. 認証をかけたい
- `fastapi_mcp` のAuth機能（Bearer Tokenなど）を追加可能です。
  業務利用や有料提供では必須化を推奨。

---

## 6. トラブルシューティング
- **/health が 200 にならない**：requirementsの未インストールや階層ミス。VercelのBuild Logsを確認。
- **Appsがツールを認識しない**：`.well-known/mcp.json` のURLが正しいか、`name` が重複していないか確認。
- **CORS/HTTPS**：VercelはデフォルトでHTTPS提供。追加設定不要です。

---

© UNLOCK
