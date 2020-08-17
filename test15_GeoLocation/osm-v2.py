# geocoder.osm 関数の実行結果をすべて見る
import geocoder
import pprint

# 緯度経度を指定
pos = (35.659025, 139.745025)
# OpenStreetMapを使って逆ジオコーディング
g = geocoder.osm(pos, method='reverse')
# すべての結果を表示
pprint.pprint(g.json)