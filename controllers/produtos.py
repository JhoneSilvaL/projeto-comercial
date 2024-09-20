from flask import Flask, render_template, request, redirect, flash, url_for
from utils import db
from models.produtos import Produto
from models.categorias import Categoria
from flask import Blueprint
from flask_login import login_required
import os
from werkzeug.utils import secure_filename

bp_produto = Blueprint("produto", __name__, template_folder='templates')

UPLOAD_FOLDER = 'static/uploads'  
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp_produto.route('/recovery', methods=['GET'])
def recovery():
    search_query = request.args.get('search', '') 

    if search_query:
        produtos = Produto.query.filter(Produto.nome.ilike(f'%{search_query}%')).all()
    else:
        produtos = Produto.query.all()

    return render_template('produto_recovery.html', produtos=produtos)

# Rota para criar um novo produto
@bp_produto.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "GET":
        categorias = Categoria.query.all() 
        return render_template('produto_create.html', categorias=categorias)

    if request.method == "POST":
        try:
            nome = request.form['nome']
            descricao = request.form['descricao']
            preco = request.form['preco']
            categoria_id = request.form.get('categoria_id')

            if 'imagem' not in request.files or request.files['imagem'].filename == '':
                flash('Nenhuma imagem foi enviada ou arquivo não selecionado.', 'danger')
                return redirect(request.url)

            imagem = request.files['imagem']

            if imagem and allowed_file(imagem.filename):
                filename = secure_filename(imagem.filename)
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                imagem.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                flash('Arquivo não permitido.', 'danger')
                return redirect(request.url)
            
            produto = Produto(nome, descricao, preco, categoria_id, filename)
            db.session.add(produto)
            db.session.commit()
            flash('Produto criado com sucesso!', 'success')
            return redirect(url_for('produto.recovery'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro: {str(e)}', 'danger')
            return redirect(request.url)

@bp_produto.route('/categoria/create', methods=['GET', 'POST'])
@login_required
def create_categoria():
    if request.method == "POST":
        nome = request.form['nome']
        if nome:
            categoria = Categoria(nome=nome)
            db.session.add(categoria)
            db.session.commit()
            flash('Categoria criada com sucesso!', 'success')
        else:
            flash('Nome da categoria não pode ser vazio.', 'danger')
        return redirect(url_for('produto.create_categoria')) 
    
    return render_template('categoria_create.html')

@bp_produto.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    produto = Produto.query.get_or_404(id)

    if request.method == "GET":
 
        categorias = Categoria.query.all()
        return render_template('produto_update.html', produto=produto, categorias=categorias)

    if request.method == "POST":
        try:
            produto.nome = request.form['nome']
            produto.descricao = request.form['descricao']
            produto.preco = request.form['preco']
            categoria_id = request.form.get('categoria_id')

            categoria = Categoria.query.get(categoria_id)
            if not categoria:
                flash('Categoria não encontrada.', 'danger')
                return redirect(request.url)

            produto.categoria_id = categoria_id 

            if 'imagem' in request.files and request.files['imagem'].filename != '':
                imagem = request.files['imagem']
                if imagem and allowed_file(imagem.filename):
                    filename = secure_filename(imagem.filename)
                    imagem.save(os.path.join(UPLOAD_FOLDER, filename))
                    produto.imagem = filename  # Atualiza o caminho da imagem no produto

            db.session.commit()
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('produto.recovery'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro: {str(e)}', 'danger')
            return redirect(request.url)

@bp_produto.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    produto = Produto.query.get_or_404(id)

    if request.method == "GET":
        return render_template('produto_delete.html', produto=produto)

    if request.method == "POST":
        try:
            db.session.delete(produto)
            db.session.commit()
            flash('Produto deletado com sucesso!', 'success')
            return redirect(url_for('produto.recovery'))

        except Exception as e:
            db.session.rollback()  # Desfaz a transação em caso de erro
            flash(f'Ocorreu um erro ao deletar o produto: {str(e)}', 'danger')
            return redirect(url_for('produto.recovery'))