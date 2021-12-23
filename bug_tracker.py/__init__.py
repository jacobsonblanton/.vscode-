# importing and setting up the flask module
from flask import Flask
from flask_sqlalchemy import SQLALchemy
from os import path
from flask_login import LoginManager

db = SQLALchemy
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'erougfoiuhn oisoifjdijvv ji-fnglkdjsfng'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
