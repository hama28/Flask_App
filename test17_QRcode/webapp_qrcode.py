from flask import Flask, request, redirect
from tinydb import TinyDB
import qrcode
from tinydb import table

# アクセスをカウントした後にジャンプするURLの
JUMP_URL = 'https://google.com/'
FILE_COUNTER = './counter.json'

# Flaskを生成
app = Flask(__name__)
# TinyDBを開く
db = TinyDB(FILE_COUNTER)

@app.route('/')
def index():
    # 訪問用QRコードを生成
    url = request.host_url + 'jump'
    img = qrcode.make(url)
    img.save('./static/qrcode_jump.png')
    # 画面にQRコードを表示
    counter = get_counter()
    return '''
    <h1>以下のQRコードを名刺に印刷</h1>
    <img src="static/qrcode_jump.png" width=300><br>
    {0}<br>
    現在の訪問者は、{1}人です。
    '''.format(url, counter)

@app.route('/jump')
def jump():
    # アクセスをカウントアップ
    v = get_counter()
    table = db.table('count_visitor')
    table.update({'v': v + 1})
    # 任意のURLにリダイレクト
    return redirect(JUMP_URL)

def get_counter():
    # アクセスを数える
    table = db.table('count_visitor')
    a = table.all()
    if len(a) == 0:
        # もし最初なら値0を挿入する
        table.insert({'v': 0})
        return 0
    return a[0]['v']

if __name__ == '__main__':
    app.run(port=5001)