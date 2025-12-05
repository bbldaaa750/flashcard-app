from app.extensions import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    
    decks = db.relationship('Deck', backref='owner', lazy=True)

    @property
    def password(self):
        raise AttributeError('Пароль - нечитаемый атрибут.')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Deck(db.Model):
    __tablename__ = 'deck'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    cards = db.relationship('Card', backref='deck', cascade='all, delete', lazy=True)

class Card(db.Model):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    front = Column(Text, nullable=False)
    back = Column(Text, nullable=False)
    
    deck_id = Column(Integer, ForeignKey('deck.id'), nullable=False)
