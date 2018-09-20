import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #從環境變數中獲取SECRET_KEY，否則使用字串以下字串
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #從環境變數中獲取資料庫URL，否則配置為basedir(根目錄)下的app.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    #資料庫變更後不用通知給本APP
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    '''
    MAIL_SERVER = os.environ.get('MAIL_SERVER') #若mail server沒有在環境中，則禁用
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25) #若mail port沒有在環境中，則使用25
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None #mail server憑證默認為不使用，根據需要可以提供
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    '''

    POSTS_PER_PAGE = 10