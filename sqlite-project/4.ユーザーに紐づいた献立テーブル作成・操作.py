import sqlite3

conn = sqlite3.connect("user_data.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# FOREIGN KEY(user_id) REFERENCES user(id)
# これは「menus テーブルの user_id フィールドは、user テーブルの id フィールドとつながっています」という意味
cursor.execute("""
CREATE TABLE IF NOT EXISTS menus(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_name TEXT NOT NULL,
    MENU_DATA TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
)
""")

conn.commit()
conn.close()
print("テーブルを作成しました")