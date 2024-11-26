from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey

db = SQLAlchemy()


class Empresa(db.Model):
    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    endereco = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)

class Avaliador(db.Model):
    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    email = Column(String(255), unique=True)

class Avaliacao(db.Model):
    id = Column(Integer, primary_key=True)
    empresa_id = Column(Integer, ForeignKey('empresa.id'))
    avaliador_id = Column(Integer, ForeignKey('avaliador.id'))
    nota = Column(Integer)
    comentario = Column(Text)