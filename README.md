## ctf-server-web-for-python

### 注意
このリポジトリはCTFの問題サーバです。  
そのため意図的に脆弱性を埋め込んでいます。

### Dockerの起動
```
$ docker network create ctf-network
$ docker-compose up -d
```

データベースの確認
```
$ docker container exec -it mysql /bin/sh
$ mysql -u [ユーザー名] -p
```
