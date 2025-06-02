# accessに接続してテーブル名を取得するサンプルコード

import pyodbc

# Accessファイルのパス（変更してね）
db_path = r"D:\Users\tanida\Desktop\分析201kopi-.accdb"

# ODBCドライバとDBのパスを指定(これはただの文字列である）
# conn_str = Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ={db_path};　という文字列が格納されているだけ
conn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    fr"DBQ={db_path};"
)

# 接続
conn = pyodbc.connect(conn_str)
# cursorはデータベースにSQL文を送り、結果を受け取るための“操作窓口
cursor = conn.cursor()

# テーブル名を取得してみる
# tables関数で「指定のテーブルの一覧を取得する関数」
# tableType='TABLE'のように引数に指定することで「実データがある通常のテーブルだけに絞って」とお願いしてる。
tables = cursor.tables(tableType='TABLE')
for table in tables:
    print("テーブル名:", table.table_name)

# execute() は、SQL文をAccess（などのデータベース）に送って「実行する」命令
# executeはまだ命令を出しただけの状態
# cursor.execute("SELECT * FROM 受付番号から抽出) ⇒ 受付番号から抽出クエリ（テーブルでも可）の全データをくださいとAccessに命令を出しただけで結果はpythonに来てない
# executeの内部SQLにpythonのf-stringで値を渡せることを確認したがセキュリティ上の懸念あり
# ? プレースホルダ＋引数タプル形式に変更した
start = int(input("始まり"))
end = int(input("終わり"))
cursor.execute("SELECT * FROM 受付番号から抽出 WHERE 証明番号 BETWEEN ? AND ?",(start,end))

# fetchall() は、直前に execute() で送ったSQLの結果を、Pythonに「持ってくる」ための命令
rows = cursor.fetchall()
for row in rows:
    print(row)

# クエリを取得するときも .tables() メソッドを使う。クエリ（保存されたSQL）はtableType="VIEW"
views = cursor.tables(tableType="VIEW")
for view in views:
    print("クエリ名",view.table_name)

cursor.close()
conn.close()

# withを使って安全に自動的にcloseしてくれるwithを使うことも多い
# with pyodbc.connect(conn_str) as conn:
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT * FROM 社員")
#         for row in cursor.fetchall():
#             print(row)
# with を抜けると自動で close() される！
