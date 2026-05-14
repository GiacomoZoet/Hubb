from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_mail import Mail
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
socketio = SocketIO(cors_allowed_origins='*', async_mode='eventlet')

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{quote_plus(os.getenv('DB_PASSWORD'))}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_HTTPONLY'] = True
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # ← must be here
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 900
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 2592000

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    with app.app_context():
        from app.sockets import events  # noqa — registers socket handlers
    CORS(app, supports_credentials=True, origins='*')

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.workspaces import workspaces_bp
    from app.routes.channels import channels_bp
    from app.routes.messages import messages_bp
    from app.routes.direct_messages import dm_bp

    app.register_blueprint(auth_bp,       url_prefix='/api/auth')
    app.register_blueprint(users_bp,      url_prefix='/api/users')
    app.register_blueprint(workspaces_bp, url_prefix='/api/workspaces')
    app.register_blueprint(channels_bp,   url_prefix='/api/channels')
    app.register_blueprint(messages_bp,   url_prefix='/api/messages')
    app.register_blueprint(dm_bp,         url_prefix='/api/dm')

    @app.route('/healthz')
    def healthz():
        return jsonify({'status': 'ok'}), 200

    return app
