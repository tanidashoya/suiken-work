#ユーザー認証
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

engine = create_engine("sqlite:///user_data.db",echo=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    
username = input("ユーザー名を入力：")
password = input("パスワードを入力：")
hashed_password = hash_password(password)

Session = sessionmaker(bind=engine)
session = Session()

user = session.query(User).filter_by(username=username,password=hashed_password).first()

if user:
    print("ログイン成功")
else:
    print("ログイン失敗")