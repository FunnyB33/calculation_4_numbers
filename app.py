# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, CalculationHistory
from calculation import calculation

app = Flask(__name__)
app.config['SECRET_KEY'] = 990328  # 適切なシークレットキーに置き換えてください
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# データベースを作成
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    expressions = []
    target = ''
    a = b = c = d = ''
    if request.method == 'POST':
        target = request.form.get('target')
        a = request.form.get('a')
        b = request.form.get('b')
        c = request.form.get('c')
        d = request.form.get('d')
        if target and a and b and c and d:
            target_num = int(target)
            nums = [int(a), int(b), int(c), int(d)]
            result, expressions = calculation(*nums, target_num)

            # ユーザーがログインしている場合のみ計算結果をデータベースに保存
            if current_user.is_authenticated:
                calc_history = CalculationHistory(
                    target=target_num,
                    numbers=','.join(map(str, nums)),
                    result=result,
                    expressions='\n'.join(expressions),
                    user_id=current_user.id
                )
                db.session.add(calc_history)
                db.session.commit()
    # ユーザーがログインしている場合のみ計算履歴を取得
    if current_user.is_authenticated:
        histories = current_user.calculations.order_by(CalculationHistory.id.desc()).all()
    else:
        histories = []
    return render_template('index.html', result=result, expressions=expressions, target=target, a=a, b=b, c=c, d=d, histories=histories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            if User.query.filter_by(username=username).first():
                flash('ユーザー名は既に使用されています。')
            else:
                user = User(username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash('登録が完了しました。ログインしてください。')
                return redirect(url_for('login'))
        else:
            flash('ユーザー名とパスワードを入力してください。')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('ユーザー名またはパスワードが間違っています。')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('login'))

@app.route('/delete_history/<int:history_id>', methods=['POST'])
@login_required
def delete_history(history_id):
    history = CalculationHistory.query.get_or_404(history_id)
    # ユーザーの所有権を確認
    if history.user_id != current_user.id:
        abort(403)
    db.session.delete(history)
    db.session.commit()
    flash('計算履歴を削除しました。')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)