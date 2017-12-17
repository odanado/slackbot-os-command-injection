# slackbot-os-command-injection

## 必要なもの
- Docker
- docker-compose

## 前準備
### ビルド
- docker-compose build base
- docker-compose build

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
