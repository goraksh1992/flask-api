from main_project import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(30))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)