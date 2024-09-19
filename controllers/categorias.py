from flask import Blueprint, render_template, request, redirect, flash, url_for
from utils import db
from models.categorias import Categoria  # Ajuste o caminho conforme necessário

bp_categoria = Blueprint("categoria", __name__, template_folder='templates')

@bp_categoria.route('/categoria/create', methods=['GET', 'POST'])
def create_categoria():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome:
            nova_categoria = Categoria(nome)
            db.session.add(nova_categoria)
            db.session.commit()
            flash('Categoria criada com sucesso!', 'success')
            return redirect(url_for('produto.recovery'))  # Redireciona onde desejar
        else:
            flash('Nome da categoria não pode ser vazio!', 'danger')
    return render_template('categoria_create.html')  # Crie esse template

@bp_categoria.route('/categoria/update/<int:id>', methods=['GET', 'POST'])
def update_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    if request.method == 'POST':
        nome = request.form['nome']
        if nome:
            categoria.nome = nome
            db.session.commit()
            flash('Categoria atualizada com sucesso!', 'success')
            return redirect(url_for('produto.recovery'))  # Redireciona onde desejar
        else:
            flash('Nome da categoria não pode ser vazio!', 'danger')

    return render_template('categoria_update.html', categoria=categoria)

@bp_categoria.route('/categoria/delete/<int:id>', methods=['GET', 'POST'])
def delete_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(categoria)
        db.session.commit()
        flash('Categoria deletada com sucesso!', 'success')
        return redirect(url_for('produto.recovery'))  # Redireciona onde desejar

    return render_template('categoria_delete.html', categoria=categoria)  # Crie esse template

@bp_categoria.route('/categoria/recovery', methods=['GET'])
def recovery_categoria():
    categorias = Categoria.query.all()  # Recupera todas as categorias
    return render_template('categoria_recovery.html', categorias=categorias)  # Crie esse template