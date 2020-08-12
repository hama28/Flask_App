from flask import session, redirect

# ログイン用のユーザーリストを定義
USERLIST = {
    'honda': 'honda',
    'toyota': 'toyota',
    'mazda': 'mazda',
}

# ログインしているかチェック
def is_login():
    return 'login' in session

# ログイン処理
def try_login(user, password):
    # 該当ユーザーがいるかチェック
    if user not in USERLIST:
        return False
    # パスワードのチェック
    if USERLIST[user] != password:
        return False
    # ログイン処理
    session['login'] = user
    return True

# ログアウト処理
def try_logout():
    session.pop('login', None)
    return True

# セッションからユーザー名を取得
def get_user():
    if is_login():
        return session['login']
    return 'not login'
