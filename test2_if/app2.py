from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('card-age.html',
                            username='綾里真宵',
                            age=18,
                            email='mayoi@example.com',
                            like='みそラーメン',
                            job='霊媒師')

if __name__ == '__main__':
    app.debug = True
    app.run()