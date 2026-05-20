from flask_login import LoginManager
from flask import Flask
from .database.models.user import User
from .database.base import Base


def init_app() -> Flask:
    app = Flask(__name__)

    # Configurando o LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        session = db_connection.get_session()  # Obtenha uma sessão de banco de dados
        user = session.query(User).get(int(user_id))  # Busque o usuário pela ID
        session.close()  # Feche a sessão
        return user

    # Setando configurações da aplicação
    from .config import TestingConfig

    app.config.from_object(TestingConfig)

    # Configuração do banco de dados
    from .database.db_connector import DBConnectionHendler

    db_connection = DBConnectionHendler()
    engine = db_connection.get_engine()
    # Criando o contexto da aplicação
    with app.app_context():
        from src.blueprints import (
            kryptacode_bp,
            bot_evo_bp

        )
        # Registrando os blueprints
        app.register_blueprint(kryptacode_bp)
        app.register_blueprint(bot_evo_bp)

        # Criando tabelas no banco de dados
        Base.metadata.create_all(engine)

    return app
