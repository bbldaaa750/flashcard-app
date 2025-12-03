from flask import Flask
from views import bp
from extensions import db

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.register_blueprint(bp)

    with app.app_context():
        from models import User
        db.create_all()
    
    app.config['SECRET_KEY'] = 'super_secret_random_string_123' # placeholder
    
    return app
