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