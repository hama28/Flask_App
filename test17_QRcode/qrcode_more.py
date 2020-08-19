import qrcode

# QRコードの生成で細かい設定を行う場合
qr = qrcode.QRCode(
    box_size=4,
    border=8,
    version=12,
    error_correction=qrcode.constants.ERROR_CORRECT_Q
)
# 描画するデータを指定する
qr.add_data('https://google.com')
# QRコードの元データを作る
qr.make()
# データをImageオブジェクトとして取得
img = qr.make_image()
# Imageをファイルに保存
img.save('qrcode2.png')
print('ok')