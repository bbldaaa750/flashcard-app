from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.services import create_user, delete_user, update_user_password, authenticate_user
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegistrationForm, ChangePasswordForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            user = authenticate_user(username, password)
            login_user(user)
            return redirect(url_for('main.dashboard'))
            
        except ValueError:
            flash('Неверное имя или пароль!', 'error')
        
    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            user = create_user(username, password)
            login_user(user)
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('main.dashboard'))
        except ValueError:
            flash('Пользователь с таким именем уже существует!', 'error')
    
    return render_template('register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/main')
@login_required
def dashboard():
    form = ChangePasswordForm() 
    return render_template('main.html', form=form) 

@bp.route('/delete', methods=['POST'])
@login_required
def delete_account():   
    delete_user(current_user.username)
    return redirect(url_for('main.register'))

@bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        new_pass = form.password.data
        try:
            update_user_password(current_user.username, new_pass)
            flash('Пароль успешно изменен!', 'success')
        except ValueError:
            flash('Новый пароль не должен совпадать со старым!', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка: {error}', 'error')

    return redirect(url_for('main.dashboard'))
