import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Configurar SECRET_KEY y SQLALCHEMY_DATABASE_URI desde .env
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave-secreta-por-defecto')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Asegurarnos de que SQLALCHEMY_DATABASE_URI esté configurado
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise RuntimeError("SQLALCHEMY_DATABASE_URI no está configurado correctamente.")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
