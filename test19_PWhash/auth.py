from flask import Flask, request
import os, json, hashlib, base64

app = Flask(__name__)
APP_DIR = os.path.dirname(__file__)
DATA_FILE = APP_DIR + '/users.json'

# ハッシュ化のためのSALT
HASH_SALT = '(0!ukjc4._AM/Qv4%|bvEH.L$Q,gWrC8'

# パスワードをハッシュ化する
def password_hash(password):
    key = password + HASH_SALT
    # バイナリ化
    key_b = key.encode('utf-8')
    return hashlib.sha256(key_b).hexdigest()

# パスワードが正しいかを検証する
def password_verify(password, hash):
    hash_v = password_hash(password)
    return (hash_v == hash)

# ファイルからログイン情報を読む
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rt') as fp:
            return json.load(fp)
    return {}

# ファイルへログイン情報を保存
def save_users(users):
    with open(DATA_FILE, 'wt', encoding='utf-8') as fp:
        json.dump(users, fp)

# 新規ユーザーを追加
def add_user(id, password):
    users = load_users()
    if id in users:
        return False
    users[id] = password_hash(password)
    save_users(users)
    return True

# ログインできるか確認
def check_login(id, password):
    users = load_users()
    if id not in users:
        return False
    return password_verify(password, users[id])

# ブラウザのメイン画面
@app.route('/')
def index():
    return '''
    <html><meta charset="utf-8"><body>
    <h3>ユーザー登録</h3> {0} <hr>
    <h3>ユーザーログイン</h3> {1}
    </body></html>
    '''.format(get_form('/register', '登録'), get_form('/login', 'ログイン'))

def get_form(action, caption):
    return '''
    <form action="{0}" method="post">
    ID:<br>
    <input type="text" name="id"><br>
    パスワード:<br>
    <input type="password" name="pw"><br>
    <input type="submit" value="{1}">
    </form>
    '''.format(action, caption)

# ユーザー登録
@app.route('/register', methods=['POST'])
def register():
    id = request.form.get('id')
    pw = request.form.get('pw')
    if id == '':
        return '<h1>失敗：IDが空です</h1>'
    # ユーザーを追加
    if add_user(id, pw):
        return '<h1>登録に成功</h1><a href="/">戻る'
    else:
        return '<h1>登録に失敗</h1>'

# ユーザー認証
@app.route('/login', methods=['POST'])
def login():
    id = request.form.get('id')
    pw = request.form.get('pw')
    if id == '':
        return '<h1>失敗：IDが空です</h1>'
    # パスワードを照合
    if check_login(id, pw):
        return '<h1>ログインに成功</h1>'
    else:
        return '<h1>失敗</h1>'

if __name__ == '__main__':
    app.run(debug=True)