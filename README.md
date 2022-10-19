# pytive
Mirrativのコメントをpythonで！  
これは人生初のpythonで、コードが汚い可能性？

## TODO
- [x] コメント機能
- [ ] フォロー/フォロー解除
- [x] 配信リクエスト

## 使い方
### ログイン
```python
import pytive

client = pytive.Mirrativ() 
# クッキー
client.login('mr_idをここに', 'fをここに')
```
### メッセージ送信
```python
live_id = '' # ...mirrativ.com/live/'ここ'
client.join_live(live_id)
client.comment(live_id, 1, 'pog')
```
### ライブリクエスト
```python
user_id = ''                          # ユーザーのID
client.request_live(user_id, count=1) # countは 1 から 2147483646 までOK
```