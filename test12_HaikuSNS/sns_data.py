from tinydb import TinyDB, Query
import time, os

# パスの指定
BASE_DIR = os.path.dirname(__file__)
DATA_FILE = BASE_DIR + '/data/data.json'

# データベースを開く
db = TinyDB(DATA_FILE)

# お気に入り登録用のfavテーブルのオブジェクトを返す
def get_fav_table():
    return db.table('fav'), Query()

# お気に入り登録
def add_fav(id, fav_id):
    table, q = get_fav_table()
    a = table.search((q.id == id) & (q.fav_id == fav_id))
    if len(a) == 0:
        table.insert({'id': id, 'fav_id': fav_id})

# お気に入り登録の確認
def is_fav(id, fav_id):
    table, q = get_fav_table()
    a = table.get((q.id == id) & (q.fav_id == fav_id))
    return a is not None

# お気に入り解除
def remove_fav(id, fav_id):
    table, q = get_fav_table()
    table.remove((q.id == id) & (q.fav_id == fav_id))

# お気に入り一覧
def get_fav_list(id):
    table, q = get_fav_table()
    a = table.search(q.id == id)
    return [row['fav_id'] for row in a]

# 俳句保存用のtextテーブルのオブジェクトを返す
def get_text_table():
    return db.table('text'), Query()

# 俳句をデータベースに追加
def write_text(id, text):
    table, q = get_text_table()
    table.insert({'id': id, 'text': text, 'time': time.time()})

# 俳句の作品一覧
def get_text(id):
    table, q = get_text_table()
    return table.search(q.id == id)

# タイムラインに表示するデータを取得
def get_timelines(id):
    # お気に入りユーザーの一覧を取得
    table, q = get_text_table()
    favs = get_fav_list(id)
    # 自身も検索対象に入れる
    favs.append(id)
    # 期間を指定して作品一覧を取得(30日分)
    tm = time.time() - (24*60*60) * 30
    a = table.search(q.id.one_of(favs) & (q.time > tm))
    return sorted(a, key=lambda v:v['time'], reverse=True)