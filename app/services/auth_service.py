from app.models import User
from app.extensions import db

def create_user(username, password):
    if User.query.filter_by(username=username).first():
        raise ValueError(f'User "{username}" already exists')
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise ValueError(f'User "{username}" not found')
    return user

def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f'User with id {user_id} not found')
    return user

def update_user_password(username, new_password):
    user = get_user(username)
    if user.verify_password(new_password):
        raise ValueError('New password must differ from old')
    user.password = new_password
    db.session.commit()
    return user

def delete_user(username):
    user = get_user(username)
    db.session.delete(user)
    db.session.commit()
    return True

def authenticate_user(username, password):
    user = get_user(username)
    if not user.verify_password(password):
        raise ValueError('Invalid credentials')
    return user
