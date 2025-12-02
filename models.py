from extensions import db
from sqlalchemy import Column, Integer, String

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
