from flask_sqlalchemy import SQLAlchemy

from ..base import Base

db = SQLAlchemy()

class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    empresa = db.Column(db.String(120), nullable=True)
    numero = db.Column(db.String(20), nullable=True)
    observacao = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'empresa': self.empresa,
            'numero': self.numero,
            'observacao': self.observacao
        }

