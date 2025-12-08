from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class DeckForm(FlaskForm):
    title = StringField('Название колоды', validators=[
        DataRequired(message="Введите название колоды"),
        Length(max=100, message="Название не может быть длиннее 100 символов")
    ])
    submit = SubmitField('Создать')

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(message="Введите имя пользователя")
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Введите пароль")
    ])
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(message="Введите имя"),
        Length(min=2, max=20, message="Имя должно быть от 2 до 20 символов")
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Введите пароль"),
        Length(min=6, message="Пароль должен быть не короче 6 символов")
    ])
    confirm_password = PasswordField('Повторите пароль', validators=[
        DataRequired(message="Повторите пароль"),
        EqualTo('password', message="Пароли должны совпадать")
    ])
    submit = SubmitField('Зарегистрироваться')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[
        DataRequired(message="Введите новый пароль"), 
        Length(min=6, message="Пароль должен быть не короче 6 символов")
    ])
    confirm_password = PasswordField('Повторите пароль', validators=[
        DataRequired(message="Повторите пароль"),
        EqualTo('password', message="Пароли должны совпадать")
    ])
    submit = SubmitField('Сохранить новый пароль')

class CardForm(FlaskForm):
    front = StringField('Вопрос', validators=[DataRequired(message="Введите вопрос")])
    back = StringField('Ответ', validators=[DataRequired(message="Введите ответ")])
    submit = SubmitField('Добавить')
