from flask import Blueprint, render_template, request, redirect, flash, url_for
from utils import db
from models.categorias import Categoria  # Ajuste o caminho conforme necessário
from flask_login import login_required
import os

bp_categoria = Blueprint("categoria", __name__, template_folder='templates')
@login_required
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
@login_required
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

@bp_categoria.route('/categoria/recovery', methods=['GET'])
@login_required
def recovery_categoria():
    categorias = Categoria.query.all()  # Recupera todas as categorias
    return render_template('categoria_recovery.html', categorias=categorias)  # Crie esse template

@bp_categoria.route('/categoria/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Deletar todos os produtos associados à categoria
            for produto in categoria.produtos:
                db.session.delete(produto)
                
            # Agora, deletar a categoria
            db.session.delete(categoria)
            db.session.commit()
            flash('Categoria e produtos associados deletados com sucesso!', 'success')
            return redirect(url_for('categoria.recovery_categoria'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao deletar a categoria: {str(e)}', 'danger')
            return redirect(url_for('categoria.recovery_categoria'))
    
    return render_template('categoria_delete.html', categoria=categoria)