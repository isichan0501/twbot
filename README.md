"# twbot" 


タスクを書きだす

シークレット情報を.envファイルに書き出す
ディレクトリ構成を決める
各ファイルの関数をブラッシュアップする（必要なのだけ残して後は消去）
↑モジュールとして呼び出せるようにする

keyファイル等の必要なデータはメインディレクトリ/data/**に入れる
READMEファイルにTodoと使用法を書く


undetected_driver用と通常ドライバーでわける
キャプチャ拡張機能をS3にいれる
cookies.jsonをs3で共有するようにする
↑DocumentDB(mongodb互換）にする？

TwitterアカウントのDBをdynamodbでとりあえず作る
↑データベース設計（スキーマを決める）

BOTの処理フローを決める
※seleniumを利用する認証用とAPI用で分ける


1,Twitterにログインしてステータスチェック（BANや番号認証）
2, プロフ設定してなければする
3, フォロワー100人以下の時は相互フォローする
4, 各アカウント用の動きをする
5,アカウントの情報をデータベースに


★裏アカ用のアカウント
1,人気アカウントのプロフやツイートをパクるのでそれ用の@TwitterIDを集めるスクリプト
2, フォローやいいね等をするターゲットユーザーのID一覧を取得
３，DMを送信する



recaptchaのsitekeyを探す


Todo:

1,create DIR (db, img, logs)

2,set account.txt(user:pass:email:emailpw)

3,set proxy.txt(host:port:user:pass)

4,set .env()