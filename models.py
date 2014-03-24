from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:@localhost/shorturls?unix_socket=/tmp/mysql.sock'
db = SQLAlchemy(app)


class Url(db.Model):
	"""A url object. Contains the long and short version of a URL."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(2000), unique=False)
    short_url = db.Column(db.String(10), unique=True)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<Url(%s) %s>' % (self.short_url, self.url)
