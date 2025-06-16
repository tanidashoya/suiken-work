from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib

"""
アプリとデータベースの設定 
"""
app = Flask(__name__)
app.secret_key = "your_secret_key"
# 使用するデータベースの場所と種類を設定する。
# "sqlite:///user_data.db"はアプリがあるディレクトリ階層のuser_data.dbを設定する（なかったら作る）
# config ⇒Flask クラスのインスタンス app が持っている、**設定情報を格納する辞書型オブジェクト（Config クラスのインスタンス）
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_data.db"
# SQLAlchemyが「オブジェクトの変更を追跡する機能」を無効化する設定。
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# FlaskアプリとSQLAlchemy（ORM）を接続し、Flaskアプリ全体で使える「データベース操作オブジェクト（db）」を作成するコード
# app.config で指定したデータベースに対して接続される
db = SQLAlchemy(app)

# パスワードハッシュ化のための関数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#「テーブルの設計図（モデルクラス）」を定義 （設計図の定義だけでまだ生成されない）
# db.modelとはSQLAlchemyのモデル定義用ベースクラス
# つまり、、、、UserやMealというクラスは、Flask-SQLAlchemyの db.Model を継承して作ったORMモデル（＝テーブルの設計図）
# 基本構造：id = db.Column(データ型, オプション1, オプション2, ...)
# 基本構造：フィールド名 = db.Column(データ型, オプション...)
# Userモデル（__tablename__="○○"を指定していないので自動推測により小文字のuserテーブルとして定義）
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# UserテーブルとつなぐMealテーブル(ユーザーが追加する料理名を追加するテーブル)
# Mealモデル（__tablename__="○○"を指定していないので自動推測により小文字のmealテーブルとして定義）
class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    # "user.id" という文字列は、**「user テーブルの id カラムを参照する」**という意味
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# この下記のコードは開発時のみ実行して、本番環境ではDBがすでに存在することが前提なので、通常はコメントアウトか別スクリプトに分ける
# Flaskアプリのアプリケーションコンテキストを一時的に有効にして、その中で db.create_all() を実行する
# アプリケーションコンテキスト（app context）→ Flaskアプリ自身の設定や拡張（SQLAlchemyなど）を使える状態
# db.create_all()⇒いままでﾍﾞｰｽクラス(db.Model)を継承して定義してきたモデルクラスに基づいてテーブルを作成する
# 初期化（最初だけ）
# app.app_context() ⇒ 「今からこの Flask アプリの設定や拡張（SQLAlchemyなど）を“使える状態”にするよ！」という「文脈（＝コンテキスト）」を生成する**オブジェクト（コンテキストマネージャ）**。
# with app.app_context(): のブロック内では、Flaskアプリが起動中と同じように扱われる。
# この状態で初めて、db.create_all() は 設定情報（接続先DBなど）を参照して正しく動作する
with app.app_context():
    db.create_all()


"""
各ページと機能の定義 
"""

# トップページ
# 【if "user_id" not in session:】によってログイン状態を判定している。ログインしてない場合 ⇒ True（未ログイン状態ではトップページにアクセスできないように制限）
# 【user = User.query.get(session["user_id"])】 sessionに保存されているuser_idを使ってそのユーザーの情報をデータベースから取得する
# 【meals = Meal.query.filter_by(user_id=user.id).all()】Mealテーブルのuser_idフィールドをuser.idの値で検索した結果の全てを取得する
# UserやMealはテーブル名ではなくモデルクラスを指定している。これらのクラスが内部的にuserテーブル、mealテーブルに対応していて、そのクラスの.queryプロパティを使ってクエリ（SELECT）している構造
# .queryは指定したモデルに対応するテーブルに対する検索操作の準備を始める」オブジェクト
# .get：引数に渡された値と「モデルの主キー（primary key）」が一致する行（レコード）を、データベースの中から探して返すメソッド
# .filter_by：「指定したカラムの値と一致するレコード」を探すための条件検索（WHERE句）
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    user = User.query.get(session["user_id"])
    meals = Meal.query.filter_by(user_id=user.id).all()
    return render_template("index.html", user=user, meals=meals)

# 新規登録
# Userモデルのインスタンス（＝1人のユーザー）を作成して、それを user テーブルに追加し、データベースに保存（commit）している処理
# db.sessionのsessionは"/"で使われているsession[user_id]（ブラウザに一時保存するためのsession）とは全く別物
# db.sessionはSQLAlchemyのデータベースセッションでデータベースとの「取引窓口」
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

# ログイン画面
# session[user_id]にuser.idを一時保存
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user_id"] = user.id
            return redirect("/")
        else:
            return "ログイン失敗"
    return render_template("login.html")

# ログアウト
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")

# 新しいメニュー追加
@app.route("/add", methods=["POST"])
def add_meal():
    if "user_id" in session:
        title = request.form["title"]
        meal = Meal(title=title, user_id=session["user_id"])
        db.session.add(meal)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
