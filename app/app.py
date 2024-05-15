from app import app
from flask import Flask, render_template, request, redirect, url_for, session, flash
from app.models import db, User
from app.forms import LoginForm, RegisterForm, ReplenishForm, ExchangeForm
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def index():
    user_id = session.get('user_id')
    user_username = None
    if user_id:
        user = User.query.get(user_id)
        user_username = user.username
    return render_template('index.html', user_id=user_id, user_username=user_username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return '<p>Invalid username or password</p>'
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)

@app.route('/replenish', methods=['GET', 'POST'])
def replenish():
    form = ReplenishForm()
    if form.validate_on_submit():
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        if form.currency.data == 'uah':
            user.uah_balance += form.amount.data
        else:
            user.usd_balance += form.amount.data
        db.session.commit()
        return redirect(url_for('user_profile', user_id=user_id))
    return render_template('replenish.html', form=form)

@app.route('/exchange', methods=['GET', 'POST'])
def exchange():
    form = ExchangeForm()
    if form.validate_on_submit():
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        rate = 40

        if form.from_currency.data == 'uah' and form.to_currency.data == 'usd':
            if user.uah_balance >= form.amount.data:
                user.uah_balance -= form.amount.data
                user.usd_balance += form.amount.data / rate
                db.session.commit()
                return redirect(url_for('user_profile', user_id=user_id))
            else:
                flash('Insufficient funds in UAH balance', 'error')
        elif form.from_currency.data == 'usd' and form.to_currency.data == 'uah':
            if user.usd_balance >= form.amount.data:
                user.usd_balance -= form.amount.data
                user.uah_balance += form.amount.data * rate
                db.session.commit()
                return redirect(url_for('user_profile', user_id=user_id))
            else:
                flash('Insufficient funds in USD balance', 'error')
    return render_template('exchange.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
