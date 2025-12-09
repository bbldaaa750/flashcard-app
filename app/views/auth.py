from flask import Blueprint, render_template, redirect, url_for, flash
from app.services import create_user, delete_user, update_user_password, authenticate_user
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegistrationForm, ChangePasswordForm
from app.models import Card, Deck

bp = Blueprint('auth', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))
    return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            user = authenticate_user(username, password)
            login_user(user)
            return redirect(url_for('auth.profile'))
            
        except ValueError:
            flash('Неверное имя или пароль!', 'danger')
        
    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            user = create_user(username, password)
            login_user(user)
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('auth.profile'))
        except ValueError:
            flash('Пользователь с таким именем уже существует!', 'danger')
    
    return render_template('register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/profile')
@login_required
def profile():
    form = ChangePasswordForm()

    decks_count = len(current_user.decks)

    cards_query = Card.query.join(Deck).filter(Deck.user_id == current_user.id)
    total_cards = cards_query.count()

    box1 = cards_query.filter(Card.box == 1).count()
    box2 = cards_query.filter(Card.box == 2).count()
    box3 = cards_query.filter(Card.box == 3).count()

    stats = {
        'total_cards': total_cards,
        'decks_count': decks_count,
        'box1': box1,
        'box2': box2,
        'box3': box3
    }

    return render_template('profile.html', form=form, stats=stats)

@bp.route('/delete', methods=['POST'])
@login_required
def delete_account():   
    delete_user(current_user.username)
    return redirect(url_for('auth.register'))

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
            flash('Новый пароль не должен совпадать со старым!', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка: {error}', 'danger')

    return redirect(url_for('auth.profile'))
