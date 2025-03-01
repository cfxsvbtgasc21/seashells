from exts import db
from datetime import datetime
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)
    sex=db.Column(db.String(5), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    info=db.Column(db.Text, nullable=True)