from flask import render_template, request, redirect, flash, url_for
from utils import db, lm
from models.usuario import Usuario
from flask import Blueprint
from flask_login import login_user, logout_user
from flask_login import current_user
import hashlib
import bcrypt

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

        # Verificar se as senhas coincidem
        if senha != senhaconf:
            flash('As senhas não coincidem. Por favor, tente novamente.', 'danger')
            return redirect(url_for('usuario.create'))

        db.session.add()
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('usuario.autenticar'))

    return render_template('usuario_create.html')
    
@lm.user_loader
def load_user(id):
    usuario = Usuario.query.get(id)
    return usuario

@bp_usuario.route('/autenticar', methods=['POST'])
def autenticar():
    if current_user.is_authenticated:
        flash('Você já está logado. Por favor, desconecte-se antes de fazer login com outra conta.', 'warning')
        return redirect(url_for('produto.recovery'))

    email = request.form['email'] 
    senha = request.form['senha']
    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and usuario.senha == senha:
        login_user(usuario)
        return redirect(url_for('produto.recovery'))
    else:
        flash('Login ou senha incorretos', 'danger')
        return redirect('/login')

@bp_usuario.route('/logoff')
def logoff():
    logout_user()
    flash('Usuário desconectado do sistema')
    return redirect('/')