from flask import Flask
# Cookieを使うのに必要な宣言
from flask import make_response, request
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    # Cookieの取得
    cnt_s = request.cookies.get('cnt')
    if cnt_s is None:
        cnt = 0
    else:
        cnt = int(cnt_s)
    # 訪問回数カウンタをインクリメント
    cnt += 1
    response = make_response("""
        <h1>訪問回数：{}回</h1>
    """.format(cnt))
    # Cookieに値を設定
    max_age = 60 * 60 * 24 * 90  # 90日
    expires = int(datetime.now().timestamp()) + max_age
    # 値と有効期限を設定
    response.set_cookie('cnt', value=str(cnt),
                        max_age=max_age, expires=expires)
    return response


if __name__ == '__main__':
    app.run(debug=True)
