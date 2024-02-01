from main import db, app
from flask_login import UserMixin


class Alunos (db.Model, UserMixin):
    __tablename__ = "alunos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(256), unique = True, nullable= False)
    email = db.Column(db.String(50), unique = True, nullable=False)
    telefone = db.Column(db.String(256), unique = True, nullable= True)
    idade = db.Column(db.Integer, unique=False, nullable = False)
    data_nascimento = db.Column(db.String(256), unique=False, nullable = False)

