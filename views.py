from flask import Blueprint, request, render_template, redirect, session
from services import create_user, read_user, delete_user, update_user_password

bp = Blueprint('main', __name__)

@bp.route('/')
def default_page():
    return redirect('/login')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form.get('username_field')
        password = request.form.get('password_field')
        try: 
            user = read_user(username)

            if user.password == password:
                session['username'] = user.username
                return redirect('/main')
            else:
                error_message = "Неправильный пароль!"
        except ValueError:
            error_message = "Пользователь не найден!"
        
    return render_template('login.html', error=error_message)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None
    if request.method == 'POST':
        username = request.form.get('username_field')
        password = request.form.get('password_field')
        try:
            create_user(username, password)
            user = read_user(username)
            session['username'] = user.username
            return redirect('/main')
        except ValueError:
            error_message = "Пользователь уже существует!"
    
    return render_template('register.html', error=error_message)

@bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@bp.route('/main')
def main():
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
    error_message = None

    if 'username' not in session:
        return redirect('/login')
    
    pass1 = request.form.get('new_pass1')
    pass2 = request.form.get('new_pass2')

    if pass1 != pass2:
        error_message = 'Пароли не совпадают!'
        return render_template('main.html', username=session['username'], error=error_message)
    
    try:
        update_user_password(session['username'], pass1)
    except ValueError:
        error_message = 'Пароль совпадает со старым!'

    return render_template('main.html', username=session['username'], error=error_message)
