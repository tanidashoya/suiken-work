import sqlite3
import hashlib



# データベースのデータ更新(既存の生パスワードをハッシュ化されたパスワードに変更)
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# user_name = input("ユーザー名を入力：")
# password = input("パスワードを入力")
# hashed_password = hash_password(password)

# conn = sqlite3.connect("user_data.db")
# cursor = conn.cursor()

# cursor.execute("UPDATE users SET password = ? WHERE username =?",(hashed_password,user_name))

# conn.commit()
# conn.close()



# パスワードハッシュ化ログイン
# ユーザーが入力したパスワードを、そのまま保存せず、ハッシュ（不可逆な変換）をしてから保存・比較するための関数
# password.encode()で文字列をバイト列に変換（hashlib.sha256()）はバイト列でしか計算できない
# hashlib はPythonの標準ライブラリで、SHAやMD5などのハッシュ関数を提供。
# sha256() はその中でも「256ビット（64桁）のハッシュ値」を生成する関数。
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

user_name = input("ユーザー名を入力：")
password = input("パスワードを入力")

hashed_password = hash_password(password)

conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users WHERE username = ? AND password =?",(user_name,hashed_password))
user = cursor.fetchone()

if user:
    print("ログイン完了しました。")
else:
    print("ログイン失敗！")
    
conn.commit()
conn.close()