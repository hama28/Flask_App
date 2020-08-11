from flask import Flask, request, session, redirect
app = Flask(__name__)
app.secret_key = 'm9XE4JH5dBOQK4o4'

# ログインに使うユーザー名とパスワードの設定
USERLIST = {
    'yamada': 'yamada',
    'tanaka': 'tanaka',
    'sato': 'sato'
}

@app.route('/')
def index():
    # ログインフォームの表示
    return """
    <html><body><h1>ログインフォーム</h1>
    <form action="/check_login" method="POST">
    ユーザー名：<br/>
    <input type="text" name="user"><br>
    パスワード：<br>
    <input type="password" name="pw"><br>
    <input type="submit" value="ログイン">
    </form>
    <p><a href="/private">会員限定ページ</a></p>
    </body></html>
    """

@app.route('/check_login', methods=['POST'])
def check_login():
    # フォームの値の取得
    user, pw = (None, None)
    if 'user' in request.form:
        user = request.form['user']
    if 'pw' in request.form:
        pw = request.form['pw']
    if (user is None) or (pw is None):
        return redirect('/')
    # ログインチェック
    if try_login(user, pw) == False:
        return """
        <h1>ユーザー名かパスワードが間違っています</h1>
        <p><a href="/">入力フォームに戻る</a></p>
        """
    # 非公開ページにリダイレクト
    return redirect('/private')

@app.route('/private')
def private_page():
    # ログインしていなければトップへリダイレクト
    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/">ログインする</a></p>
        """
    # ログイン後のページの表示
    return """
    <h1>ここは会員限定ページです</h1>
    <p>あなたはログインしています</p>
    <p><a href="/logout">ログアウト</a></p>
    """

@app.route('/logout')
def logout_page():
    # ログアウト処理の実行
    try_logout()
    return """
    <h1>ログアウトしました</h1>
    <p><a href="/">TOPに戻る</a></p>
    """

# ログインに関する処理
# ログインしているかチェック
def is_login():
    if 'login' in session:
        return True
    return False

# ログイン処理を行う
def try_login(user, password):
    # ユーザー名がリストにあるかチェック
    if not user in USERLIST:
        return False
    # パスワードがあっているかチェック
    if USERLIST[user] != password:
        return False
    # ログイン処理を実行
    session['login'] = user
    return True

# ログアウトする
def try_logout():
    session.pop('login', None)
    return True

if __name__ == '__main__':
    app.run(debug=True)