from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from services import create_user, read_user, delete_user, update_user_password

bp = Blueprint('main', __name__)

@bp.route('/')
def default_page():
    return redirect('/login')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username_field')
        password = request.form.get('password_field')
        try: 
            user = read_user(username)

            if user.password == password:
                session['username'] = user.username
                return redirect(url_for('main.dashboard'))
            else:
                flash('Неправильный пароль!', 'error')
        except ValueError:
            flash('Пользователь не найден!', 'error')
        
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username_field')
        password = request.form.get('password_field')
        try:
            create_user(username, password)
            user = read_user(username)
            session['username'] = user.username
            return redirect(url_for('main.dashboard'))
        except ValueError:
            flash('Пользователь уже существует!', 'error')
    
    return render_template('register.html')

@bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@bp.route('/main')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    return render_template('main.html', username=session['username'], error=None)

@bp.route('/delete', methods=['POST'])
def delete_account():
    if 'username' not in session:
        return redirect('/login')    
    delete_user(session['username'])
    session.clear()
    return redirect('/register')

@bp.route('/change_password', methods=['POST'])
def change_password():
    if 'username' not in session:
        return redirect('/login')
    
    pass1 = request.form.get('new_pass1')
    pass2 = request.form.get('new_pass2')

    if pass1 != pass2:
        flash('Пароли не совпадают!', 'error')
        return redirect(url_for('main.dashboard'))
    
    try:
        update_user_password(session['username'], pass1)
        flash('Пароль успешно изменен!', 'success')
    except ValueError:
        flash('Пароль совпадает со старым!', 'error')

    return redirect(url_for('main.dashboard'))
