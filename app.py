from flask import Flask, render_template, request, url_for, flash, redirect
import json, os
from flask_migrate import Migrate
from models import *
## from models.cidade import Cidade
from flask import flash, redirect
from utils import db, lm
from controllers.cidade import bp_cidade
from controllers.usuario import bp_usuario


app = Flask(__name__)
app.register_blueprint(bp_cidade, url_prefix='/cidade')
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

@app.route('/')
def index():
    return render_template('paginaInicial.html')

@app.route('/login')
def login ():
    return render_template('login.html')

@app.route('/usuario_create.html')
def usuario_create():
    return render_template('usuario_create.html')

@app.route('/cidade_create')
def cidade_create():
    return render_template('cidade_create.html')

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

# @app.route('/add_diario')
# def add_diario():
#     c = Cidade('LIC0X83', 'Desenvolvimento Web')
#     db.session.add(c)
#     db.session.commit()
#     return 'Dados inseridos com sucesso!'

# @app.route('/select_diario')
# def select_diario():
#     #dados = Diario.query.all() # SELECT * from diario
#     #for d in dados:
#     #    print(d.id, d.titulo, d.disciplina)

#     c = Cidade.query.get(2) # SELECT * from diario WHERE id = 2
#     print(c.id, c.titulo, c.disciplina)

#     return 'Dados obtidos com sucesso'

# @app.route('/update_diario')
# def update_diario():
#     c = Cidade.query.get(2)
#     c.titulo = 'LICX866'
#     c.disciplina = "Segurança da Informação"
#     db.session.add(c)
#     db.session.commit()
#     return 'Dados atualizados com sucesso'

# @app.route('/delete_diario')
# def delete_diario():
#     c = Cidade.query.get(2)
#     db.session.delete(c)
#     db.session.commit()
#     return 'Dados excluídos com sucesso'

@app.errorhandler(401)
def acesso_negado(e):
    return render_template('acesso_negado.html')

@app.errorhandler(404)
def acesso_negado(e):
    return render_template('not_found.html')


if __name__ == '__main__':
    app.run(debug=True)
