# ユーザー登録用スクリプト
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker
import hashlib

# 引数に渡されたパスワードをハッシュ化
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

engine = create_engine("sqlite:///user_data.db",echo=False)
Base = declarative_base()

# Userテーブルの定義
class User(Base):
    __tablename__="users"
    # フィールドを定義
    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)

# 「engine（接続情報）を使って、データベース操作専用の session（取引窓口）を作成する」
Session = sessionmaker(bind=engine)
session =Session()

username = input("ユーザー名を入力：")
password = input("パスワードを入力：")
hashed_password = hash_password(password)

new_user = User(username=username,password=hashed_password)
session.add(new_user)
session.commit()


"""
① Session = sessionmaker(bind=engine)
意味：セッションを作成する「工場（関数）」を作ってる

engine を使って接続先（SQLiteなど）を教えている

👉 この時点では まだ接続してない
→ 「セッションの雛形（作り方の設計図）」を作っただけ


② session = Session()
意味：その工場から実際の「セッションオブジェクト」を作ってる

このオブジェクトを使って：

データの追加（add）

検索（query）

削除（delete）

更新（commit）

など、あらゆる操作ができるようになる！
"""



