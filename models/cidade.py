# É necessário importar a variável DB
from utils import db
from flask_login import UserMixin

class Cidade(db.Model, UserMixin):
  __tablename__= "cidade"
  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(100))
  email = db.Column(db.String(100))
  cidade = db.Column(db.String(100))
  estado = db.Column(db.String(100))
  
  def __init__(self, nome, email, cidade, estado):
    self.nome = nome
    self.email = email
    self.cidade = cidade
    self.estado = estado