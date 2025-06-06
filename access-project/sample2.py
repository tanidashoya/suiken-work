# | 社員ID（int） | 名前（str） | 年齢（int） |
# | --------- | ------- | ------- |
# | 1         | 田中      | 30      |
# | 2         | 山田      | 25      |

import pyodbc

db_path = db_path = r"D:\Users\tanida\Desktop\分析201kopi-.accdb"
conn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    fr"DBQ={db_path};"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# id = int(input("idを入力してください："))
# age = int(input("年齢を入力してください："))
# name = (input("名前を入力してください："))

# #INSERT（新しいデータを入れる）
# cursor.execute("INSERT INTO 社員(社員ID,名前,年齢) VALUES (?,?,?)",
#                (id,name,age))

# #UPDATE（データを更新する）
# cursor.execute("UPDATE 社員 SET 年齢 = ? WHERE 名前 = ?",(age,name))

# cursor.execute(...) は、**「このSQL文をデータベースに送って、実行してください」**という命令です。
cursor.execute("DELETE FROM 社員 WHERE 社員ID = ?",(3,))

conn.commit()


