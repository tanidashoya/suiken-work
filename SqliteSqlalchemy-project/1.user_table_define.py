from sqlalchemy import create_engine,Column,Integer,String
# declarative_base　ORMモデル（テーブル定義）の共通の親クラスを作る関数。
# sessionmaker　データベースとやり取りする「セッションオブジェクト」を生成する工場関数。
from sqlalchemy.orm import declarative_base,sessionmaker

# ORM（Object-Relational Mapping） とは：
# 「Pythonなどのオブジェクト（＝クラス）と、データベースのテーブル（＝リレーショナル構造）を**対応（マッピング）**させる技術」のこと。

# SQLAlchemyのエンジン（DBとの接続管理オブジェクト）を作成
# echo=Trueにすると実行されたSQLがログに出力される（デバッグ用）
engine = create_engine("sqlite:///user_data.db",echo=False)

# declarative_base() によって、全てのORMモデルの基底クラス（親クラス）を作成
# これを継承することでPythonのクラスを「テーブル定義」として使えるする」ためのコード
# ORM用のﾍﾞｰｽクラス（全てのテーブルの土台）を作成
Base = declarative_base()

# Userテーブルの定義
class User(Base):
    __tablename__="users"
    # フィールドを定義
    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)

# Baseに登録された(Baseを継承して定義された)すべてのテーブル定義を、実際のDBファイルに反映
# まだ存在していないテーブルを最初に一度だけ作成するための処理
Base.metadata.create_all(engine)

print("データベース生成完了")


"""
ORM（Object Relational Mapping）とは？
データベースの「テーブル」と「Pythonのクラス」を1対1で対応させる仕組み。

SQLを書かずにPythonのクラスやオブジェクトでDB操作できるようにする。
"""