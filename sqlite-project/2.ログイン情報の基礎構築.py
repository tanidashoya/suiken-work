import sqlite3

username = str(input("ユーザーネームを入力："))
password = str(input("パスワードを入力："))

#例のごとくデータベースと接続して操作するためのcursorオブジェクトを作成
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

# データベースの users テーブルから、username と password の両方が変数 username, password と一致するレコードを1件だけ取得し、変数 user に格納する
# cursorはその実行結果（該当するレコード）を内部で保持できる状態になります。
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username,password))
user = cursor.fetchone()

#userはタプルで返されている
if user:
    print(user)
    print("ログイン成功！")
else:
    print("ログイン情報が間違えています!")
    
conn.close()
