from app.models import User
from app.extensions import db

def create_user(username, password):
    if User.query.filter_by(username=username).first():
        raise ValueError("Create user failed")
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
        raise ValueError("Read user failed")

def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    else:
        raise ValueError("Delete user failed")

def update_user_password(username, new_password):
    user = User.query.filter_by(username=username).first()
    if user.verify_password(new_password):
        raise ValueError("Update user failed")
    else:
        user.password = new_password
        db.session.commit()

def authenticate_user(username, password):
    try:
        user = read_user(username)
    except ValueError:
        raise ValueError("Auth user failed")

    if not user.verify_password(password):
        raise ValueError("Auth user failed")
        
    return user
