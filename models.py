from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

"""
コメントアウトないバージョン

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
    numbers = db.Column(db.String(64), nullable=False)
    result = db.Column(db.Integer, nullable=False)
    expressions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
"""

# コメントアウトあるバージョン

# データベースの初期化
db = SQLAlchemy()

# Userモデル（ユーザー情報を管理）
class User(UserMixin, db.Model):
    # データベースのテーブル名を指定
    __tablename__ = 'users'
    
    # ユーザーID（主キーとして一意の整数値）
    id = db.Column(db.Integer, primary_key=True)
    
    # ユーザー名（ユニークである必要があり、null不可）
    username = db.Column(db.String(64), unique=True, nullable=False)
    
    # ハッシュ化されたパスワードを保存
    password_hash = db.Column(db.String(128), nullable=False)
    
    # ユーザーが持つ計算履歴を取得（1対多の関係）
    # backrefで計算履歴側からこのUserオブジェクトにアクセス可能
    calculations = db.relationship('CalculationHistory', backref='user', lazy='dynamic')

    # パスワードをハッシュ化して保存するメソッド
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 入力されたパスワードとハッシュ化されたパスワードを比較して認証するメソッド
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# CalculationHistoryモデル（計算履歴を管理）
class CalculationHistory(db.Model):
    # データベースのテーブル名を指定
    __tablename__ = 'calculation_history'
    
    # 計算履歴のID（主キーとして一意の整数値）
    id = db.Column(db.Integer, primary_key=True)
    
    # 計算のターゲット値（例: 作りたい「10」などの目標）
    target = db.Column(db.Integer, nullable=False)
    
    # 使用された数字（カンマ区切りで保存するための文字列）
    numbers = db.Column(db.String(64), nullable=False)
    
    # 結果として得られた組み合わせの数
    result = db.Column(db.Integer, nullable=False)
    
    # すべての計算式（複数行のテキストとして保存、改行区切り）
    expressions = db.Column(db.Text, nullable=False)
    
    # ユーザーID（外部キーとして、どのユーザーがこの計算を行ったかを示す）
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

