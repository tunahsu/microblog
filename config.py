import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #從環境變數中獲取SECRET_KEY，否則使用字串以下字串
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #從環境變數中獲取資料庫URL，否則配置為basedir(根目錄)下的app.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    #資料庫變更後不用通知給本APP
    SQLALCHEMY_TRACK_MODIFICATIONS = False