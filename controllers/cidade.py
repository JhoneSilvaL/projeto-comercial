from flask import render_template, request, redirect, flash, url_for
from utils import db
from models.cidade import Cidade
from flask import Blueprint
from flask_login import login_required

bp_cidade = Blueprint("cidade", __name__, template_folder='templates')

@bp_cidade.route('/recovery')
@login_required
def recovery():
    dados = Cidade.query.all()
    return render_template('cidade_recovery.html', dados=dados)

@bp_cidade.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method=="GET":
        return render_template('cidade_create.html')

    if request.method=="POST":
        nome = request.form['nome']
        email = request.form['email']
        cidade = request.form['cidade']
        estado = request.form['estado']
        c = Cidade(nome, email, cidade, estado)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('cidade.recovery'))

@bp_cidade.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    c = Cidade.query.get(id)
    
    if request.method=="GET":
        return render_template('cidade_update.html', c=c)

    if request.method=="POST":
        c.nome = request.form['nome']
        c.email = request.form['email']
        c.cidade = request.form['cidade']
        c.estado = request.form['estado']
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('cidade.recovery'))


@bp_cidade.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    c = Cidade.query.get(id)

    if request.method=="GET":
        return render_template('cidade_delete.html', c=c)

    if request.method=="POST":
        db.session.delete(c)
        db.session.commit()
        return redirect(url_for('cidade.recovery'))
        