from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, RadioField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class ReplenishForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    currency = RadioField('Currency', choices=[('uah', 'UAH'), ('usd', 'USD')])
    submit = SubmitField('Replenish')

class ExchangeForm(FlaskForm):
    from_currency = RadioField('From', choices=[('uah', 'UAH'), ('usd', 'USD')])
    to_currency = RadioField('To', choices=[('usd', 'USD'), ('uah', 'UAH')])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Exchange')
