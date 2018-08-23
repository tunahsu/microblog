from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

#當資料庫錯誤為避免失敗的資料干擾其他資料庫，將session重置為乾淨的狀態
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500