from flask import Flask
from .views import auth_bp, deck_bp
from app.extensions import db, login_manager

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'super_secret_random_string_123' # placeholder

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(deck_bp)

    with app.app_context():
        db.create_all()
    
    return app
