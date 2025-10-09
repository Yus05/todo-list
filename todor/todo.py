from flask import Blueprint, render_template

bp = Blueprint('todo', __name__, url_prefix='/todo')


@bp.route('/list')
def index():
    return render_template('todo/index.html')


@bp.route('/create')
def create():
    return "Crear una Tarea"






