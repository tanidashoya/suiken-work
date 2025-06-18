from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

# ユーザーモデル
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# LoginManagerの設定
# LoginManager	FlaskとFlask-Loginを接続するためのクラス。ログイン状態の管理の中心になる。
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ユーザー読み込み関数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return 'ログイン失敗'

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



"""
LoginManager	FlaskとFlask-Loginを接続するためのクラス。ログイン状態の管理の中心になる。
login_user	ログイン成功時にそのユーザーをログイン状態にする関数。
logout_user	ログアウト処理を行う関数。セッションを切る役目。
login_required	ログインしていないと見られないページに使うデコレーター（関数の上に書く）
current_user	現在ログインしているユーザーオブジェクトにアクセスする変数。よく .username などで使う。
UserMixin	Flask-Loginに「このクラスはログインできるユーザーですよ」と教えるためのMIXINクラス。Userモデルに継承させて使う。
"""