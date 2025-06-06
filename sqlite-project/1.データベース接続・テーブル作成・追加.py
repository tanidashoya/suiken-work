import sqlite3

#データベースと接続する。(無ければ自動作成)
conn = sqlite3.connect("user_data.db")
#接続したデータベースを操作可能にするためのカーソルオブジェクトを作成
cursor = conn.cursor()
#cursor.execute(...) は、**「このSQL文をデータベースに送って、実行してください」**という命令
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    )
""")

username = str(input("ユーザーネームを設定してください："))
password = str(input("パスワードを入力してください："))

cursor.execute("INSERT INTO users(username,password) VALUES (?,?) " ,(username,password))

conn.commit()
conn.close()
