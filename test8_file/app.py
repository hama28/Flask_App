from flask import Flask, request, redirect
from datetime import datetime
import os

# 保存先のディレクトリとURLの設定
IMAGES_DIR = './static/images'
IMAGES_URL = '/static/images'
app = Flask(__name__)


@app.route('/')
def index_page():
    # アップロードのフォーム作成
    return """
    <html><body><h1>アップロード</h1>
    <form action="/upload" method="POST" enctype="multipart/form-data">
    <input type="file" name="upfile">
    <input type="submit" value="アップロード">
    </form>
    </body></html>
    """


@app.route('/upload', methods=['POST'])
def upload():
    # アップされていなければトップへリダイレクト
    if not ('upfile' in request.files):
        return redirect('/')
    # アップしたファイルのオブジェクトを取得
    temp_file = request.files['upfile']
    # ファイル名無しはトップへリダイレクト
    if temp_file.filename == '':
        return redirect('/')
    # JPEGファイル以外は却下する
    if not is_jpegfile(temp_file.stream):
        return '<h1>JPEG以外の形式はアップできません</h1>'
    # 保存先のファイル名を指定
    time_s = datetime.now().strftime('%Y%m%d%H%M%S')
    fname = time_s + '.jpeg'
    # 一時ファイルを保存先ディレクトリに保存
    temp_file.save(IMAGES_DIR + '/' + fname)
    # 画像の表示ページへ
    return redirect('/photo/' + fname)


@app.route('/photo/<fname>')
def photo_page(fname):
    # 画像ファイルの有無チェック
    if fname is None:
        return redirect('/')
    image_path = IMAGES_DIR + '/' + fname
    image_url = IMAGES_URL + '/' + fname
    if not os.path.exists(image_path):
        return '<h1>画像がありません</h1>'
    # 画像を表示するHTML
    return """
    <h1>画像がアップロードされています</h1>
    <p>URL: {0}<br>
    file: {1}</p>
    <img src="{0}" width="400">
    """.format(image_url, image_path)


def is_jpegfile(fp):
    # JPEGファイルかどうかのチェック
    # 今回は、JPEGファイルの先頭2バイトが 0xFFD8 であるという特徴を利用する
    byte = fp.read(2)
    fp.seek(0)
    return byte[:2] == b'\xFF\xD8'


if __name__ == '__main__':
    app.run(debug=True)
