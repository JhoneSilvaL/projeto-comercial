from utils import db
from flask_login import UserMixin
from .categorias import Categoria

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    imagem = db.Column(db.String(100), nullable=True)  # Campo para armazenar o nome da imagem
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, nome, descricao, preco, categoria_id, imagem):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria_id = categoria_id
        self.imagem = imagem

    @staticmethod
    def valida_preco(preco):
        if preco < 0:
            raise ValueError("O preço não pode ser negativo.")