from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# メール設定（Gmailの例）※送信元の情報を設定している
# flaskアプリにconfigで必要な情報を覚えさせる
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  #gmailの場合は'smtp.gmail.com'
app.config['MAIL_PORT'] = 587                 #smtpサーバーのポートは587を使用するのが一般的
app.config['MAIL_USE_TLS'] = True             #通信を暗号化するかどうか（GmailはTLSが基本）
app.config['MAIL_USERNAME'] = 'your@gmail.com'  #ログインするメールアドレス（送信元）
app.config['MAIL_PASSWORD'] = 'your_app_password'   #Gmailログイン用（通常パスワードではなくアプリ用）

# 拡張クラスから拡張インスタンスをつくって操作する
mail = Mail(app)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # 管理者宛のメール
        # subject	メールの件名。ここでは「お問い合わせフォームから届いたよ」の通知
        # sender	メールの差出人。ここでは app.config['MAIL_USERNAME'] → つまりしょうやさん自身のGmailアドレス
        # recipients	宛先リスト（リスト形式）。ここでは ["your@gmail.com"] ＝ 管理者（しょうやさん）自身
        admin_msg = Message(subject="【お問い合わせ】フォームからの通知",
                            sender=app.config['MAIL_USERNAME'],
                            recipients=["your@gmail.com"])
        admin_msg.body = f"お名前: {name}\nメール: {email}\n\nお問い合わせ内容:\n{message}"
        mail.send(admin_msg)

        # ユーザー宛の自動返信メール
        user_msg = Message(subject="【自動返信】お問い合わせありがとうございます",
                           sender=app.config['MAIL_USERNAME'],
                           recipients=[email])
        user_msg.body = f"{name} 様\n\nお問い合わせありがとうございます。\n以下の内容で受け付けました。\n\n---\n{message}\n---\n\n担当者より折り返しご連絡いたします。"
        mail.send(user_msg)

        # Flaskが用意している「一時的な通知メッセージをユーザーに表示するための仕組み」
        flash("お問い合わせを受け付けました。確認メールを送信しました。")
        return redirect("/contact")
    return render_template("contact.html")
