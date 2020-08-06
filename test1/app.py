from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    username = '成歩堂龍ノ介'
    age = '20'
    email = 'naruhodo@example.com'
    return render_template('card.html',username=username,age=age,email=email)

if __name__ == '__main__':
    app.debug = True
    app.run()