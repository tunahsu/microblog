from app import app, db
from app.models import User, Post

#當輸入flask shell命令時，會開啟shell並註冊他回傳的項目
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}