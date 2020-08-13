from flask import Flask, redirect, render_template
from flask import request, Markup
import os, time
import sns_user as user, sns_data as data

# Flaskインスタンスと暗号化キーの指定
app = Flask(__name__)
app.secret_key = 'TIIDe5TUMtPUHpoy'

# URLのルーティング
@app.route('/')
@user.login_required
def index():
    me = user.get_id()