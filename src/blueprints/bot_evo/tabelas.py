from sqlalchemy import Column, Integer, String

from src.database.base import Base


class ConTatos(Base):
    """Tabela de contatos para o bot Evo"""
    __tablename__ = 'contatos'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone
        }
