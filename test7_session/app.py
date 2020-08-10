from flask import Flask, request, session, redirect
app = Flask(__name__)
app.secret_key = '9KStWezC'


@app.route('/')
def index():
    return """
    <html><body>
    <form action="/setname" method="GET">
    名前：<input type="text" name="username">
    <input type="submit" value="開始">
    </form></body></html>
    """


@app.route('/setname')
def setname():
    name = request.args.get('username')
    if name is None:
        return redirect('/')
    session['name'] = name
    return redirect('morning')


def getLinks():
    return """
    <ul><li><a href="/morning">朝の挨拶</a></li>
    <li><a href="/hello">昼の挨拶</a></li>
    <li><a href="/night">夜の挨拶</a></li></ul>
    """


@app.route('/morning')
def morning():
    if not ('name' in session):
        return redirect('/')
    name = session['name']
    return """
    <h1>{0}さん、おはようございます！</h1>{1}
    """.format(name, getLinks())


@app.route('/hello')
def hello():
    if not ('name' in session):
        return redirect('/')
    return """
    <h1>{0}さん、こんにちは！</h1>{1}
    """.format(session['name'], getLinks())


@app.route('/night')
def night():
    if not ('name' in session):
        return redirect('/')
    return """
    <h1>{0}さん、こんばんは！</h1>{1}
    """.format(session['name'], getLinks())


if __name__ == '__main__':
    app.run(debug=True)
