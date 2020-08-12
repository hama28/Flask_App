from flask import Flask, redirect, url_for, session
from flask import render_template, request
import os, json, datetime
import bbs_login
import bbs_data

app = Flask(__name__)
app.secret_key = 'U1sNMeUkZSuuX2Zn'

# 掲示板のメイン画面
@app.route('/')
def index():
    # ログインが必要
    if not bbs_login.is_login():
        return redirect('/')
    # ログ一覧を表示
    return render_template('index.html',
                    user=bbs_login.get_user(),
                    data=bbs_data.load_data())

# ログイン画面を表示
@app.route('/login')
def login():
    return render_template('login.html')

# ログイン処理
@app.route('try_login', method=['POST'])
def try_login():
    user = request.form.get('user', '')
    pw = request.form.get('pw', '')
    # ログインに成功したらトップページへ
    if bbs_login.try_login(user, pw):
        return redirect('/')
    # ログインに失敗したらメッセージを表示
    return show_msg('ログインに失敗しました')
