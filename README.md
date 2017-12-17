# slackbot-os-command-injection

コマンドを投げると実行してその結果を返してくれるbotです
https://qiita.com/odanado/items/fb5a5e996b302d4b4ca4

## 必要なもの
- Docker
- docker-compose

## 前準備
### ビルド
```bash
docker-compose build base
docker-compose build
```

### 環境変数
`.env` ファイルを作って，そこに `SLACK_TOKE` を書いて下さい
```bash
cat .env
SLACK_TOKEN=xoxb-11111111111-xxxxxxxxxxxxxxxxxxxxxxxx
```

## 起動方法
```bash
docker-compose up -d bot
```

# 言語を追加するには
`langs/` 以下に言語名でディレクトリ作って，その中に `Dockerfile` と `config.yml` を書いて下さい
そして `docker-compose.yml` を編集してください
