from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('card-age.html',
                            username='成歩堂龍一',
                            age=25,
                            email='naruhodo@example.com',
                            like='リンゴとウインナー',
                            job='弁護士')

if __name__ == '__main__':
    app.debug = True
    app.run()