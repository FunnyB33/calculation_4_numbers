# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    calculations = db.relationship('CalculationHistory', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class CalculationHistory(db.Model):
    __tablename__ = 'calculation_history'
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.Integer, nullable=False)
    numbers = db.Column(db.String(64), nullable=False)  # カンマ区切りの文字列で保存
    result = db.Column(db.Integer, nullable=False)
    expressions = db.Column(db.Text, nullable=False)  # 改行区切りで保存
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))