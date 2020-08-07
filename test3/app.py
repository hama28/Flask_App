from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    users = [
        {'name':'コースケ', 'age':22},
        {'name':'ゲンキ', 'age':25},
        {'name':'セイヤ', 'age':18}
    ]
    return render_template(
        'users.html',
        users=users)

if __name__ == '__main__':
    app.debug = True
    app.run()