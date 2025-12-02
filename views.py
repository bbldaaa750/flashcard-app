from flask import Blueprint, request, render_template, redirect
from services import create_user, read_user

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
                return render_template('main.html')
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
            return render_template('main.html')
        except ValueError:
            error_message = "Пользователь уже существует!"
    
    return render_template('register.html', error=error_message)
