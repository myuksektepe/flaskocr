import os

import sqlalchemy
from flask import render_template, request, make_response, abort, redirect, url_for, flash
from werkzeug.utils import secure_filename

from models import *

app = Flask(__name__, static_url_path='/static')

#############################################################################################################3
# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'Test+369'
# app.config['MYSQL_DATABASE_DB'] = 'makdospanelDB'
# app.config['MYSQL_DATABASE_HOST'] = '185.122.201.21'
# app.config['MYSQL_DATABASE_PORT'] = 2106
# mysql.init_app(app)
#
#
# @app.route('/db-list', strict_slashes=False)
# def db_veri_oku():
#     conn = mysql.connect()
#     cursor = conn.cursor()
#     sql = "SELECT * FROM django_session"
#     cursor.execute(sql)
#     cevap = cursor.fetchall()
#     return render_template('sqltest.html', cevap=cevap)


#############################################################################################################
#############################################################################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Test+369@185.122.201.21:2106/makdospanelDB'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/sqlachemy-yaz', strict_slashes=False)
def sqlachemy_yaz():
    try:
        db.create_all()
        admin = User(username='admin', email='admin@example.com')
        db.session.add(admin)
        db.session.commit()
        return 'Kayıt girildi!'
    except sqlalchemy.exc.IntegrityError as hata:
        return 'Hata: {}'.format(hata)


@app.route('/sqlachemy-oku', strict_slashes=False)
def sqlachemy_oku():
    admin_bul = User.query.all()
    return render_template('sqlachemytest.html', admin_bul=admin_bul)


#############################################################################################################
#############################################################################################################


@app.route('/')
def ana_sayfa():
    return 'Merhaba!'


@app.route('/giris', methods=['GET', 'POST'], strict_slashes=False)
def giris():
    if request.method == 'POST':
        return '{}'.format("POST")
    else:
        return '{}'.format("GET")


@app.route('/cerezoku', strict_slashes=False)
def cerezoku():
    kullaniciadi = request.cookies.get('kullaniciadi')
    return render_template('cerez.html')


@app.route('/cerezguncelle', strict_slashes=False)
def cerezguncelle():
    resp = make_response(render_template('cerezokunacaksayfa.html'))
    resp.set_cookie('kullaniciadi', 'musluy')
    return resp


@app.route('/login', methods=['POST', 'GET'], strict_slashes=False)
def login():
    if request.method == 'POST':
        kullaniciadi = request.form['kullaniciadi']
        return render_template('login.html', kullaniciadi=kullaniciadi)
    else:
        uyari = 'Lütfen giriş yapınız'
        return render_template('login.html', uyari=uyari)


@app.route('/dosyayuklemeformu', methods=['POST', 'GET'], strict_slashes=False)
def post_dosya():
    if request.method == 'POST':
        f = request.files['dosya']
        f.save('/home/muslu/flask/uploads/{}'.format(secure_filename(f.filename)))
        return render_template('dosyayuklemeformu.html')
    else:
        uyari = 'Lütfen yüklemek için dosya seçiniz!'
        return render_template('dosyayuklemeformu.html', uyari=uyari)


@app.route('/kayit/goster/<int:kayit_id>', strict_slashes=False)
def kayit_goster(kayit_id):
    return '{}'.format(kayit_id)


@app.route('/merhaba/', strict_slashes=False)
@app.route('/merhaba/<isim>')
def merhaba(isim=None):
    return render_template('index.html', isim=isim)


@app.route('/girisgerekensayfa', strict_slashes=False)
def girisgerekensayfa():
    return redirect(url_for('girisyap'))


@app.route('/flash', strict_slashes=False)
def flash_test():
    flash('Flash test')
    return render_template('index.html')


@app.route('/girisyap', strict_slashes=False)
def girisyap():
    abort(401)


@app.route('/headers-bilgi-ekleme', strict_slashes=False)
def headers_bilgiekleme():
    resp = make_response(render_template('index.html'))
    resp.headers['X-Served-By'] = 'Makdos v2018.4.25'
    return resp


db.init_app(app)
app.secret_key = os.urandom(24)
app.run(host="127.0.0.1", port=8035, debug=True)
#############################################################################################################
#############################################################################################################
