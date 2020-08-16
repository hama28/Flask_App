from flask import Flask, redirect, request
from flask import render_template, send_file
import photo_db, sns_user as user

app = Flask(__name__)
app.secret_key = 'dpwvgAxaY2iWHMb1'

# ログイン処理
@app.route('/login')
def login():
    return render_template('login_form.html')

@app.route('/login/try', methods=['POST'])
def login_try():
    ok = user.try_login(request.form)
    if not ok:
        return msg('ログイン失敗')
    return redirect('/')

@app.route('/logout')
def logout():
    user.try_logout()
    return msg('ログアウトしました')


# メイン画面 メンバーの最新写真を全部表示する
@app.route('/')
@user.login_required
def index():
    return render_template('index.html', id=user.get_id(), photos=photo_db.get_files())

# アルバムに入っている画像一覧を表示
@app.route('/album/<album_id>')
@user.login_required
def album_show(album_id):
    album = photo_db.get_album(album_id)
    return render_template('album.html', album=album, photos=photo_db.get_album_files(album_id))

# ユーザーがアップした画像の一覧を表示
@app.route('/user/<user_id>')
@user.login_required
def user_page(user_id):
    return render_template('user.html', id=user_id, photos=photo_db.get_user_files(user_id))


# 画像ファイルのアップロード
@app.route('/upload')
@user.login_required
def upload():
    return render_template('upload_form.html', albums=photo_db.get_albums(user.get_id()))

@app.route('/upload/try', methods=['POST'])
@user.login_required
def upload_try():
    # アップロードされたファイルの確認
    upfile = request.files.get('upfile', None)
    if upfile is None:
        return msg('アップロード失敗')
    if upfile.filename == '':
        return msg('アップロード失敗')
    # どのアルバムに所属させるかをフォームから値を得る
    album_id = int(request.form.get('album', '0'))
    # ファイルの保存とデータベースへの登録
    photo_id = photo_db.save_file(user.get_id(), upfile, album_id)
    if photo_id == 0:
        return msg('データベースのエラー')
    return redirect('/user/' + str(user.get_id()))


# アルバムの作成
@app.route('/album/new')
@user.login_required
def album_new():
    return render_template('album_new_form.html')

@app.route('/album/new/try')
@user.login_required
def album_new_try():
    id = photo_db.album_new(user.get_id(), request.args)
    if id == 0:
        return msg('新規アルバム作成に失敗')
    return redirect('/upload')


# 画像ファイルを送信する
@app.route('/photo/<file_id>')
@user.login_required
def photo(file_id):
    ptype = request.args.get('t', '')
    photo = photo_db.get_file(file_id, ptype)
    if photo is None:
        return msg('ファイルがありません')
    return send_file(photo['path'])


def msg(s):
    return render_template('msg.html', msg=s)

# CSSなどの静的ファイルの後ろにバージョンを自動追記
@app.context_processor
def add_staticfile():
    return dict(staticfile=staticfile_cp)
def staticfile_cp(fname):
    import os
    path = os.path.join(app.root_path, 'static', fname)
    mtime = str(int(os.stat(path).st_mtime))
    return '/static/' + fname + '?v=' + str(mtime)

if __name__ == '__main__':
    app.run(debug=True)