from sqlalchemy.exc import IntegrityError
from ...database.db_connector import db_connector



class ConsultaDados:

    @classmethod
    @db_connector
    def cadastrar_contato(cls, connection, data):

        from src.database.models.user import User

        try:
            nova_consulta = User(
                username=data.get('username'),
                email=data.get('email'),
                empresa=data.get('empresa'),
                numero=data.get('numero'),
                observacao=data.get('observacao')
            )

            connection.session.add(nova_consulta)
            connection.session.commit()

            return {"status": "ok"}

        except IntegrityError:
            connection.session.rollback()
            return {"status": "erro", "tipo": "duplicado"}

        except Exception as e:
            connection.session.rollback()
            return {"status": "erro", "tipo": "generico"}
