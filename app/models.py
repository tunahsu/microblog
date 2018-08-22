from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)

    #在Post類添加一個屬性(author)，並動態執行
    #通常在一對多的"一"這邊定義
    posts = db.relationship('Post', backref='author', lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #Flask-SQLAlchemy會把類名設為小寫來當作對應表的名稱

    def __repr__(self):
        return '<Post {}>'.format(self.body)