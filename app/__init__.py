# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
# from config import Config
# from flask_migrate import Migrate

# def create_app():
#     app = Flask(__name__)
#     # Initialize your app and database here
#     db.init_app(app)
#     migrate = Migrate(app, db)
#     return app


# db = SQLAlchemy()
# jwt = JWTManager()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     db.init_app(app)
#     jwt.init_app(app)

#     from app.routes.auth import auth as auth_blueprint
#     from app.routes.user import user as user_blueprint

#     app.register_blueprint(auth_blueprint)
#     app.register_blueprint(user_blueprint)

#     return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with the app
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth as auth_blueprint
    from app.routes.user import user as user_blueprint
    from app.swagger import swagger_ui_blueprint, swagger as swagger_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(swagger_ui_blueprint, url_prefix='/swagger')
    app.register_blueprint(swagger_blueprint)

    return app
