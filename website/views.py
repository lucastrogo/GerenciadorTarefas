'''Arquivo para as outras funções'''

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Usuario, Materia, Topico, Anotacao
from . import db
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@login_required
@views.route('/')
def index():
    materias = Materia.query.filter(id_usuario=current_user.id).all()
    return render_template('index.html', materias=materias)

@login_required
@views.route('/adicionar_materia', methods=['POST'])
def adicionar_materia():
    nome = request.form['nome']
    materia = Materia(nome=nome, id_usuario=current_user.id)
    db.session.add(materia)
    db.session.commit()
    flash('Matéria adicionada com sucesso!', 'success')
    return redirect(url_for('index'))

@login_required
@views.route('/materia/<int:id_materia>')
def materia(id_materia):
    materia = Materia.query.get(id_materia)
    return render_template('subject.html', materia=materia)

@login_required
@views.route('/adicionar_topico/<int:id_materia>', methods=['POST'])
def adicionar_topico(id_materia):
    nome = request.form['nome']
    topico = Topico(nome=nome, id_materia=id_materia)
    db.session.add(topico)
    db.session.commit()
    flash('Tópico adicionado com sucesso!', 'success')
    return redirect(url_for('materia', id_materia=id_materia))

@login_required
@views.route('/marcar_completo/<int:id_topico>', methods=['POST'])
def marcar_completo(id_topico):
    topico = Topico.query.get(id_topico)
    topico.completo = True
    db.session.commit()
    flash('Tópico marcado como concluído!', 'success')
    return redirect(url_for('materia', id_materia=topico.id_materia))

@login_required
@views.route('/adicionar_anotacao/<int:id_topico>', methods=['POST'])
def adicionar_anotacao(id_topico):
    texto = request.form['texto']
    anotacao = Anotacao(texto=texto, id_topico=id_topico)
    db.session.add(anotacao)
    db.session.commit()
    flash('Anotação adicionada com sucesso!', 'success')
    return redirect(url_for('materia', id_materia=Topico.query.get(id_topico).id_materia))