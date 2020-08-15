from typing import Tuple
from flask import Flask, redirect, render_template
from flask import request, Markup
import os, time
import sns_user as user, sns_data as data

# Flaskインスタンスと暗号化キーの指定
app = Flask(__name__)
app.secret_key = 'TIIDe5TUMtPUHpoy'

# URLのルーティング
@app.route('/')
@user.login_required
def index():
    me = user.get_id()
    return render_template('index.html', id=me,
                users=user.get_allusers(),
                fav_users=data.get_fav_list(me),
                timelines=data.get_timelines(me))

# ログインフォームの表示
@app.route('/login')
def login():
    return render_template('login_form.html')

# ログイン処理
@app.route('/login/try', methods=['POST'])
def login_try():
    ok = user.try_login(request.form)
    if not ok:
        return msg('ログインに失敗しました')
    return redirect('/')

# ログアウト処理
@app.route('/logout')
def logout():
    user.try_logout()
    return msg('ログアウトしました')

# ユーザー個別ページの表示
@app.route('/users/<user_id>')
@user.login_required
def users(user_id):
    if user_id not in user.USER_LOGIN_LIST:
        return msg('ユーザーが存在しません')
    me = user.get_id()
    return render_template('users.html', user_id=user_id, id=me, is_fav=data.is_fav(me, user_id), text_list=data.get_text(user_id))

# お気に入り登録
@app.route('/fav/add/<user_id>')
@user.login_required
def fav_add(user_id):
    data.add_fav(user.get_id(), user_id)
    return redirect('/users/' + user_id)

# お気に入り解除
@app.route('/fav/remove/<user_id>')
@user.login_required
def remove_fav(user_id):
    data.remove_fav(user.get_id(), user_id)
    return redirect('/users/' + user_id)

# 書き込みフォーム
@app.route('/write')
@user.login_required
def write():
    return render_template('write_form.html', id=user.get_id())

# 書き込み処理
@app.route('/write/try', methods=['POST'])
@user.login_required
def try_write():
    text = request.form.get('text', '')
    if text == '':
        return msg('テキストが空です')
    data.write_text(user.get_id(), text)
    return redirect('/')

def msg(msg):
    return render_template('msg.html', msg=msg)

# 拡張機能の指定
@app.context_processor
def add_staticfile():
    return dict(staticfile=staticfile_cp)
def staticfile_cp(fname):
    path = os.path.join(app.root_path, 'static', fname)
    mtime = str(int(os.stat(path).st_mtime))
    return '/static' + fname + '?v=' + str(mtime)

# 改行を有効にするフィルタの追加
@app.template_filter('linebreak')
def linebreak_fiter(s):
    s = s.replace('&', '&amp').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
    return Markup(s)

# 日付をフォーマットするフィルタを追加
@app.template_filter('datestr')
def datestr_fiter(s):
    return time.strftime('%Y年%m月%d日', time.localtime(s))

if __name__ == '__main__':
    app.run(debug=True)