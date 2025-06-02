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

cursor.execute("INSERT INTO 社員")