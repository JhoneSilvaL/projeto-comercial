from flask import Flask, render_template, request, url_for, flash, redirect
import os
import locale
from flask_migrate import Migrate
from models import *  # Certifique-se de que todos os modelos estão corretamente definidos em models.py
from utils import db, lm  # Certifique-se de que db e lm são inicializados corretamente
from controllers.produtos import bp_produto
from controllers.usuario import bp_usuario
from controllers.categorias import bp_categoria

# Inicializa a aplicação Flask
app = Flask(__name__)

# Configurações da aplicação
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mydefaultsecretkey')  # Usar uma chave padrão apenas em dev.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração de conexão com o banco de dados
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
mydb = os.getenv('DB_DATABASE')

if not all([username, password, host, mydb]):
    raise ValueError("Todas as variáveis de ambiente de configuração do banco de dados precisam estar definidas.")

conexao = f"mysql+pymysql://{username}:{password}@{host}/{mydb}"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao

# Inicialização do banco de dados e login manager
db.init_app(app)
lm.init_app(app)

# Inicialização da migração de banco de dados
migrate = Migrate(app, db)

# Configuração de locale para formatação de números
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Registro dos blueprints
app.register_blueprint(bp_produto, url_prefix='/produto')
app.register_blueprint(bp_usuario, url_prefix='/usuario')
app.register_blueprint(bp_categoria)

# Filtro de template para formatação de números
@app.template_filter('number_format')
def number_format(value, decimal_places=2, decimal_marker=',', thousands_marker='.'):
    if value is None:
        return ""
    try:
        return f"{value:,.{decimal_places}f}".replace(',', decimal_marker).replace('.', thousands_marker)
    except (ValueError, TypeError):
        return value

# Rota inicial
@app.route('/')
def index():
    return render_template('paginaInicial.html')

# Rota de login
@app.route('/login')
def login():
    return render_template('login.html')

# Rota para a página de criação de usuário
@app.route('/usuario_create.html')
def usuario_create():
    return render_template('usuario_create.html')

# Rota para autenticação de usuário
@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    if usuario != 'admin' or senha != 'senha123':
        flash("Login ou senha incorretos", 'danger')
        return redirect(url_for('login'))
    else:
        return f"Os dados recebidos foram: usuario = {usuario} e senha = {senha}"

# Rota para cadastro de novos usuários
@app.route('/cadastro_usuarios', methods=['GET', 'POST'])
def cadastro_usuarios():
    if request.method == 'GET':
        return render_template('cadastro_usuarios.html')
    else:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        csenha = request.form['csenha']

        # Validações básicas
        if not nome or not email or not senha or senha != csenha:
            if not nome:
                flash('Campo nome não pode ser vazio', 'danger')
            if not email:
                flash('Campo email não pode ser vazio', 'danger')
            if not senha:
                flash('Campo senha não pode ser vazio', 'danger')
            if senha != csenha:
                flash('As senhas não conferem', 'danger')
        else:
            # Aqui você pode adicionar a lógica para salvar os dados no banco
            flash('Dados cadastrados com sucesso!', 'success')

        return redirect(url_for('cadastro_usuarios'))

# Tratamento de erros - Acesso negado
@app.errorhandler(401)
def acesso_negado(e):
    return render_template('acesso_negado.html'), 401

# Tratamento de erros - Página não encontrada
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('not_found.html'), 404

# Executa a aplicação
if __name__ == '__main__':
    app.run(debug=True)