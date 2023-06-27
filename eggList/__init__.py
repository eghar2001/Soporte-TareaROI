import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from eggList.config import Config




db = SQLAlchemy()
bcrypt = Bcrypt()
#login_manager = LoginManager()
#login_manager.login_view = "users.login"
#login_manager.login_message_category = "primary"

mail = Mail()



def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    #login_manager.init_app(app)
    mail.init_app(app)

    from eggList.listas.routes import listas
    from eggList.productos.routes import productos
    from eggList.main.routes import main

    app.register_blueprint(listas)
    app.register_blueprint(productos)
    app.register_blueprint(main)

    return app
