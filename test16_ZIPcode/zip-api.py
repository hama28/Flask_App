from flask import Flask, request
import sqlite3, os, json

# 郵便番号のデータベースのパスを特定
base_path = os.path.dirname(os.path.abspath(__file__))
db_path = base_path + '/zip.sqlite'
form_path = base_path + '/zip-form.html'

# Flaskを取り込む
app = Flask(__name__)

# ルートにアクセスがあったとき
@app.route('/')
def indes():
    with open(form_path, encoding='UTF-8') as f:
        return f.read()

# APIにアクセスがあったとき
@app.route('/api')
def api():
    # パラメータを取得
    q = request.args.get("q", "")
    # データベースから値を取得
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        'SELECT ken,shi,cho FROM zip WHERE code=?',
        [q]
    )
    items = c.fetchall()
    conn.close()
    # 結果をJSONで出力
    res = []
    for i, r in enumerate(items):
        ken,shi,cho = (r[0], r[1], r[2])
        res.append(ken + shi + cho)
        print(q, ":", ken + shi + cho)
    return json.dumps(res)

# Flaskを開始する
if __name__ == '__main__':
    app.run()