from flask import Blueprint, request, render_template, redirect, url_for, flash
from services import create_user, delete_user, update_user_password, authenticate_user
from flask_login import login_user, logout_user, login_required, current_user

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
    
    if request.method == 'POST':
        username = request.form.get('username_field')
        password = request.form.get('password_field')

        try:
            user = authenticate_user(username, password)
            login_user(user)
            return redirect(url_for('main.dashboard'))
            
        except ValueError:
            flash('Неверное имя или пароль!', 'error')
        
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username_field')
        password = request.form.get('password_field')
        try:
            user = create_user(username, password)
            login_user(user)
            return redirect(url_for('main.dashboard'))
        except ValueError:
            flash('Пользователь уже существует!', 'error')
    
    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/main')
@login_required
def dashboard():
    return render_template('main.html', username=current_user.username)

@bp.route('/delete', methods=['POST'])
@login_required
def delete_account():   
    delete_user(current_user.username)
    return redirect(url_for('main.register'))

@bp.route('/change_password', methods=['POST'])
@login_required
def change_password():  
    pass1 = request.form.get('new_pass1')
    pass2 = request.form.get('new_pass2')

    if pass1 != pass2:
        flash('Пароли не совпадают!', 'error')
        return redirect(url_for('main.dashboard'))
    
    try:
        update_user_password(current_user.username, pass1)
        flash('Пароль успешно изменен!', 'success')
    except ValueError:
        flash('Пароль совпадает со старым!', 'error')

    return redirect(url_for('main.dashboard'))
