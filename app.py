from flask import Flask, render_template, request, url_for, flash, redirect
import os
import locale
from flask_migrate import Migrate
from models import *
from utils import db, lm
from controllers.produtos import bp_produto
from controllers.usuario import bp_usuario

app = Flask(__name__)
app.register_blueprint(bp_produto, url_prefix='/produto')
app.register_blueprint(bp_usuario, url_prefix='/usuario')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
mydb = os.getenv('DB_DATABASE')

conexao = f"mysql+pymysql://{username}:{password}@{host}/{mydb}"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
lm.init_app(app)

migrate = Migrate(app, db)

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

@app.template_filter('number_format')
def number_format(value, decimal_places=2, decimal_marker=',', thousands_marker='.'):
    if value is None:
        return ""
    try:
        return f"{value:,.{decimal_places}f}".replace(',', decimal_marker).replace('.', thousands_marker)
    except (ValueError, TypeError):
        return value

@app.route('/')
def index():
    return render_template('paginaInicial.html')

@app.route('/login')
def login ():
    return render_template('login.html')

@app.route('/usuario_create.html')
def usuario_create():
    return render_template('usuario_create.html')

@app.route('/produto_create')
def produto_create():
    return render_template('produto_create.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    if usuario != 'admin' or senha != 'senha123':
       flash("Login ou senha incorretos")
       return redirect("/login")
    else:
       	 return "Os dados recebidos foram: usuario = {} e senha = {}".format(usuario, senha)

@app.route('/cadastro_usuarios', methods=['GET', 'POST'])
def cadastro_usuarios():
    if request.method=='GET':
        return render_template('cadastro_usuarios.html')
    else:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        csenha = request.form['csenha']

        if nome == '' or email == '' or senha == '' or senha != csenha:
            if nome == '':
                flash('Campo nome não pode ser vazio', 'danger')
            if email == '':
                flash('Campo email não pode ser vazio', 'danger')
            if senha == '':
                flash('Campo senha não pode ser vazio', 'danger')
            if senha != csenha:
                flash('As senhas não conferem', 'danger')
        else:
            flash('Dados cadastrados com sucesso!', 'success')

        return redirect(url_for('cadastro_usuarios'))

@app.errorhandler(401)
def acesso_negado(e):
    return render_template('acesso_negado.html')

@app.errorhandler(404)
def acesso_negado(e):
    return render_template('not_found.html')


if __name__ == '__main__':
    app.run(debug=True)
