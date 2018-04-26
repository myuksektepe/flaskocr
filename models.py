from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

appp = Flask(__name__)
appp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Test+369@185.122.201.21:2106/makdospanelDB'
db = SQLAlchemy(appp)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
