# pytive
Mirrativのコメントをpythonで！  
これは人生初のpythonで、コードが汚い可能性？

## 使い方
### ログイン
```python
import mirrativ

client = mirrativ.Mirrativ()
client.login('mr_idをここに', 'fをここに') # クッキーでログイン
```
### メッセージ送信
```python
live_id = '' # ...mirrativ.com/live/'ここ'
client.join_live(live_id)
client.comment(live_id, 1, 'pog')
```
