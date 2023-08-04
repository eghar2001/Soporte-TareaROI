import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from eggList.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "usuarios.login"
login_manager.login_message_category = "primary"
login_manager.login_message = "Necesitas loguearte para poder acceder a esta página"

mail = Mail()



def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)



    from eggList.listas.routes import listas
    from eggList.productos.routes import productos
    from eggList.usuarios.routes import usuarios
    from eggList.main.routes import main
    from eggList.grupos_familiares.routes import grupos_familiares
    from eggList.compras.routes import compras
    from eggList.provincias.routes import provincias
    from eggList.errores.routes import errores

    app.register_blueprint(listas)
    app.register_blueprint(productos)
    app.register_blueprint(usuarios)
    app.register_blueprint(main)
    app.register_blueprint(grupos_familiares)
    app.register_blueprint(compras)
    app.register_blueprint(provincias)
    app.register_blueprint(errores)

    return app
