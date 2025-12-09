from flask import Flask
from config import Config
from app.extensions import db, login_manager
from .views import auth_bp, deck_bp, study_bp, quiz_bp, typing_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'auth.login' 
    login_manager.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."
    login_manager.login_message_category = "warning"

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(deck_bp)
    app.register_blueprint(study_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(typing_bp)

    with app.app_context():
        db.create_all()
    
    return app
