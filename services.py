from models import User
from extensions import db

def create_user(username, password):
    if User.query.filter_by(username=username).first():
        raise ValueError(f"Пользователь с именем '{username}' найден в базе данных.")
    else:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user

def read_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user
    else:
        raise ValueError(f"Пользователь с именем '{username}' не найден в базе данных.")

def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    else:
        raise ValueError(f"Пользователь с именем '{username}' не найден в базе данных.")

def update_user_password(username, new_password):
    user = User.query.filter_by(username=username).first()
    if user.password != new_password:
        user.password = new_password
        db.session.commit()
    else:
        raise ValueError(f"У пользователя с именем '{username}' такой же пароль.")
