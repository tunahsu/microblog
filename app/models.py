from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash #Werkzeug為Flask一個核心依賴項目
from flask_login import UserMixin
from hashlib import md5
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    #在Post類添加一個屬性(author)，並動態執行
    #通常在一對多的"一"這邊定義
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #Gravatar頭貼網址為https://www.gravatar.com/avatar/<用戶郵件地址MD5的hash值>
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    #可以呼叫該function來加載給定ID的用戶
    #Flask-Login將string(id)傳入，需再轉成int
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #Flask-SQLAlchemy會把類名設為小寫來當作對應表的名稱

    def __repr__(self):
        return '<Post {}>'.format(self.body)