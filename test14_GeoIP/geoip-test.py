# ライブラリの取り込み
import geoip2.database

# 確認したいIPアドレスの指定
check_ip = '157.7.44.174'

# データベースを読み込み
render = geoip2.database.Reader('GeoLite2-City.mmdb')
# データベースを検索
rec = render.city(check_ip)
# 検索結果を表示
print('IP:', check_ip)
print('Country', rec.country.name)
print('City', rec.city.name)
print('Latitude', rec.location.latitude)
print('Longitude', rec.location.longitude)