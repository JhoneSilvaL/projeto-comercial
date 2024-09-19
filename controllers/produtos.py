from flask import render_template, request, redirect, flash, url_for
from utils import db
from models.produtos import Produto  # Certifique-se de que o nome esteja correto
from flask import Blueprint
from flask_login import login_required

bp_produto = Blueprint("produto", __name__, template_folder='templates')

@bp_produto.route('/recovery')
#@login_required 
def recovery():
    produtos = Produto.query.all()  # Verifique se o nome da classe está correto
    return render_template('produto_recovery.html', produtos=produtos)

@bp_produto.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "GET":
        return render_template('produto_create.html')

    if request.method == "POST":
        nome = request.form['nome']
        descricao = request.form['descricao']
        cidade = request.form['cidade']
        estado = request.form['estado']
        preco = request.form['preco']
        categoria_id = request.form.get('categoria_id')  # Usando get para evitar erro se não existir
        produto = Produto(nome, descricao, cidade, estado, preco, categoria_id)
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('produto.recovery'))

@bp_produto.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    produto = Produto.query.get_or_404(id)
    
    if request.method == "GET":
        return render_template('produto_update.html', produto=produto)

    if request.method == "POST":
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.cidade = request.form['cidade']
        produto.estado = request.form['estado']
        produto.preco = request.form['preco']
        produto.categoria_id = request.form.get('categoria_id')  # Usando get para evitar erro se não existir
        db.session.commit()
        return redirect(url_for('produto.recovery'))

@bp_produto.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    produto = Produto.query.get_or_404(id)

    if request.method == "GET":
        return render_template('produto_delete.html', produto=produto)

    if request.method == "POST":
        db.session.delete(produto)
        db.session.commit()
        return redirect(url_for('produto.recovery'))