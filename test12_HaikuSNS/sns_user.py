from flask import Flask, session, redirect
from functools import wraps

# ユーザー名とパスワードの一覧
USER_LOGIN_LIST = {
    'ichiro': '111',
    'niro': '222',
    'sanro': '333',
    'yonro': '444',
    'goro': '555' }

# ログインしているかのチェック
def is_login():
    return 'login' in session

# ログインを試行する
def try_login(form):
    user = form.get('user', '')
    password = form.get('pw', '')
    # パスワードのチェック
    if user not in USER_LOGIN_LIST:
        return False
    if USER_LOGIN_LIST[user] != password:
        return False
    session['login'] = user
    return True

# ユーザー名の取得
def get_id():
    return session['login'] if is_login() else '未ログイン'

# 全ユーザーの情報を取得
def get_allusers():
    return [u for u in USER_LOGIN_LIST]

# ログアウトする
def try_logout():
    session.pop('login', None)

# ログイン必須を処理するデコレーターを定義
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_login():
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper