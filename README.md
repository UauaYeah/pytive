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
from pytive import Pytive

client = Pytive()
# クッキー
client.login('mr_idをここに', 'fをここに')
```
### メッセージ送信

```python
# ...mirrativ.com/live/'ここ'
from pytive import CommentType

live_id = ''

client.join_live(live_id)
client.comment(live_id, CommentType.NORMAL, 'pog')
```
### ライブリクエスト
```python
# ユーザーのID
user_id = ''

# countは 1 から 2147483646 までOK
client.request_live(user_id, count=1)
```