from flask import render_template, request, redirect, flash, url_for
from utils import db, lm
from models.usuario import Usuario
from flask import Blueprint
from flask_login import login_user, logout_user
import hashlib

bp_usuario = Blueprint("usuario", __name__, template_folder='templates')

@bp_usuario.route('/recovery')
def recovery():
    dados = Usuario.query.all()
    return 'Aqui vai aparecer os dados de todos os usuários'

@bp_usuario.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template('usuario_create.html')

    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senhaconf = request.form['senhaconf']

        # Verificar se o e-mail já está cadastrado
        if Usuario.query.filter_by(email=email).first():
            flash('Esse e-mail já está cadastrado. Por favor, escolha outro.', 'danger')
            return redirect(url_for('usuario.create'))

        # Aqui você pode adicionar a lógica de hashing da senha, se necessário
        # md5 = hashlib.md5()
        # md5.update(senha.encode('utf-8'))
        # senha_cripto = md5.hexdigest()

        u = Usuario(nome, email, senha)  # Ajuste aqui se você estiver armazenando a senha de forma criptografada
        db.session.add(u)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('usuario.autenticar'))  # Certifique-se de que o URL está correto
    
@lm.user_loader
def load_user(id):
    usuario = Usuario.query.get(id)
    return usuario

@bp_usuario.route('/autenticar', methods=['POST'])
def autenticar():
    email = request.form['email'] 
    senha = request.form['senha']
    usuario = Usuario.query.filter_by(email=email).first()

    print(usuario)
    if (usuario and usuario.senha == senha):
        login_user(usuario)
        return redirect(url_for('produto.recovery'))
    else:
        flash('Login ou senha incorretos')
        return redirect('/login')

@bp_usuario.route('/logoff')
def logoff():
    logout_user()
    flash('Usuário desconectado do sistema')
    return redirect('/')