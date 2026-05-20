from ...database.base import Base
from ...database.db_connector import db_connector

class ConsultaDados:
    """Classe de consultas para o bot Evo"""

    @classmethod
    @db_connector
    def add_contatos(cls, connection, data):
        """ cadastra os contatos vindo de um csv ou de um formulário """
        from src.blueprints.bot_evo.tabelas import ConTatos

        try:
            novo_contato = ConTatos(
                nome=data.get('nome'),
                telefone=data.get('telefone')
            )

            connection.session.add(novo_contato)
            connection.session.commit()

            return {"status": "ok"}

        except Exception as e:
            connection.session.rollback()
            return {"status": "erro", "tipo": "generico"}
