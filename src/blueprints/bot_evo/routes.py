from flask import Blueprint
from  .consultas import ConsultaDados
import csv
from flask import jsonify
from src.database import DBConnectionHendler
from src.blueprints.bot_evo.tabelas import ConTatos

bot_evo_bp = Blueprint('bot_evo', __name__, url_prefix='/don')



def public_endpoint(function):
    """Decorator for public routes"""
    function.is_public = True
    return function


@public_endpoint
@bot_evo_bp.route('/busca_contatos', methods=['GET'])
def busca_contatos():
    """Busca contatos no banco de dados"""

    db_connection = DBConnectionHendler()
    session = db_connection.get_session()

    try:
        contatos = session.query(ConTatos).all()
        return jsonify({
            'success': True,
            'contatos': [contato.to_dict() for contato in contatos]
        })

    except Exception as e:
        print("Erro:", str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        session.close()

@public_endpoint
@bot_evo_bp.route('/contatos', methods=['GET'])
def get_contatos():
    """Lê contatos do CSV e salva no banco"""

    db_connection = DBConnectionHendler()
    session = db_connection.get_session()

    print("Iniciando leitura do CSV e inserção no banco de dados...")

    try:

        arquivo_csv = 'src/blueprints/bot_evo/contatos.csv'

        contatos_adicionados = []
        contatos_existentes = 0
        contatos_invalidos = 0

        # utf-8-sig remove o BOM (\ufeff)
        with open(arquivo_csv, mode='r', encoding='utf-8-sig') as file:

            reader = csv.DictReader(file)

            print("Colunas encontradas:", reader.fieldnames)

            for row in reader:

                nome = row.get('Nome', '').strip()
                telefone = row.get('Numero', '').strip()

                # limpa telefone
                telefone = ''.join(filter(str.isdigit, telefone))

                print(f"Processando contato: {nome} - {telefone}")

                # ignora inválidos
                if not nome or not telefone:
                    contatos_invalidos += 1
                    continue

                # verifica duplicado
                contato_existente = session.query(ConTatos).filter_by(
                    telefone=telefone
                ).first()

                if contato_existente:
                    contatos_existentes += 1
                    continue

                novo_contato = ConTatos(
                    nome=nome,
                    telefone=telefone
                )

                session.add(novo_contato)
                contatos_adicionados.append(novo_contato)

        session.commit()

        return jsonify({
            'success': True,
            'message': 'Importação concluída',
            'adicionados': len(contatos_adicionados),
            'existentes': contatos_existentes,
            'invalidos': contatos_invalidos,
            'contatos': [
                {
                    'nome': contato.nome,
                    'telefone': contato.telefone
                }
                for contato in contatos_adicionados
            ]
        })

    except Exception as e:

        session.rollback()

        print("Erro:", str(e))

        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

    finally:

        session.close()
