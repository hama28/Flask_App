import qrcode

img = qrcode.make('https://google.com')
img.save('qrcode.png')
print('ok')