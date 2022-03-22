from . import urlshort
from flask import Flask, redirect, url_for
import json
import os.path
import random

if os.path.exists('secretkey.json'):
    with open('secretkey.json') as key_file:
        keys = json.load(key_file)


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'jasifulbaiufbiueaubfliubaliub2839028fbaisdubfuioasdbf'

    
    app.register_blueprint(urlshort.bp, url_prefix='/')

    @app.route('/clear')
    def clearCookies():
        newKey = str(random.randint(30000000000000, 90000000000000))
        # app.config["SECRET_KEY"] = rand()
        keys["secretkey"] = newKey
        app.config["SECRET_KEY"] = newKey
        return redirect(url_for('urlshort.home'))
    return app

