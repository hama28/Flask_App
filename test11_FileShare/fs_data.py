from tinydb import TinyDB, where
import uuid, time, os

# パスの指定
BASE_DIR = os.path.dirname(__file__)
FILES_DIR = BASE_DIR + '/files'
DATA_FILE = BASE_DIR + '/data/data.json'

# アップロードされたファイルとメタ情報の保存
def save_file(upfile, meta):
    # UUIDの生成
    id = 'FS_' + uuid.uuid4().hex
    # アップロードされたファイルを保存
    upfile.save(FILES_DIR + '/' + id)
    # メタデータをデータベースに保存
    db = TinyDB(DATA_FILE)
    meta['id'] = id
    # 期限を計算
    term = meta['limit'] * 60 * 60 * 24
    meta['time_limit'] = time.time() + term
    # 情報をデータベースに挿入
    db.insert(meta)
    return id

# データベースから任意のIDのデータを取り出す
def get_data(id):
    db = TinyDB(DATA_FILE)
    f = db.get(where('id') == id)
    if f is not None:
        f['path'] = FILES_DIR + '/' + id
    return f

# データを更新する
def set_data(id, meta):
    db = TinyDB(DATA_FILE)
    db.update(meta, where('id') == id)

# すべてのデータを取得する
def get_all():
    db = TinyDB(DATA_FILE)
    return db.all()

# アップロードされたファイルとメタ情報の削除
def remove_data(id):
    # ファイルを削除
    path = FILES_DIR + '/' + id
    os.remove(path)
    # メタ情報を削除
    db = TinyDB(DATA_FILE)
    db.remove(where('id') == id)