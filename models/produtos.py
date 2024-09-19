from utils import db
from flask_login import UserMixin

class Produto(db.Model, UserMixin):
    __tablename__ = 'produtos'  # Nome da tabela no banco
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(100), nullable=False)  # Nome do produto
    descricao = db.Column(db.Text, nullable=True)  # Descrição do produto
    preco = db.Column(db.Float, nullable=False)  # Preço do produto
    cidade = db.Column(db.String(100), nullable=False)  # Cidade do produto
    estado = db.Column(db.String(100), nullable=False)  # Estado do produto
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)  # Chave estrangeira
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())  # Data de criação

    def __init__(self, nome, descricao, cidade, estado, preco, categoria_id):
        self.nome = nome
        self.descricao = descricao
        self.cidade = cidade
        self.estado = estado
        self.preco = preco
        self.categoria_id = categoria_id