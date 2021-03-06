from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash #Werkzeug為Flask一個核心依賴項目
from flask_login import UserMixin
from hashlib import md5
from app import db, login

#因為這是一個只有外鍵的輔助表，所以不用model類別
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    #在Post類添加一個屬性(author)，並動態執行
    #通常在一對多的"一"這邊定義
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    #傳回產生實例的類別名稱則定義__repr__()
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

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    #follower.c.followed_id的意思是follower裡面的followed_id這個欄位 c應該是指column
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #Flask-SQLAlchemy會把類名設為小寫來當作對應表的名稱
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
