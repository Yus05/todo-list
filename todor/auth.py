from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session, g
    )


from werkzeug.security import generate_password_hash, check_password_hash


from .models import User
from todor import db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods = ('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User(username, generate_password_hash(password))
        
        error = None
        
        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El usuario {username} ya esta registrado'
            
        flash(error)
        
    return render_template('auth/register.html')


@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        

        
        error = None
        # Validar datos
        user = User.query.filter_by(username = username).first()
        if user == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Contraseña incorrecta'
        
        # Iniciar sesion
        if error is None:
            session.clear()
            session['user_id'] = user.id
            db.session.commit()
            return redirect(url_for('todo.index'))

            
        flash(error)
    
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)




"""
CONTEXTO GENERAL DEL ARCHIVO:

Este archivo maneja el registro e inicio de sesion de usuarios en la aplicacion Flask.
Está organizado como un Blueprint llamado 'auth', lo que significa que separará la lógica de autenticación del resto de la app (por ejemplo, las tareas de 'todo' u otras funciones).

Blueprints permiten mantener la app modular y más limpia.
En este caso, este blueprint manejará las rutas que empiezan con /auth, como:

- /auth/register
- /auth/login



IMPORTACIONES ¿QUÉ HACE CADA UNA?

- Blueprint: permite registrar un conjunto de rutas bajo un prefijo comun.
- renter_template: renderiza plantillas HTML.
- request: accede a los datos enviados por el formulario(request.form).
- url_for: genera URLs dinamicamente.
- redirect: redirige a otra ruta.
- flash: muestra mensajes de error o confirmacion del usuario (usualmente con Bootstrap).
- session: guarda informacion del usuario durante la sesion (por ejemplo, si esta logueado).
- g: se utiliza para guardar datos globales por peticion.

'generate_password_hash' y 'check_password_hash' son funciones de Werkzeug que sirven para:
- Hashear contrasenas (nunca se guardan en texto plano).
- Verificar si una contraseña ingresada coincide con el hash almacenado.

'User' viene del archivo 'models.py' (donde está definida la tabla de usuarios en SQLAlchemy).
db es la intancia de SQLAlchemy que maneja la base de datos.



CREACION DEL BLUEPRINT:
bp = Blueprint('auth', __name__, url_prefix='/auth')
-> Esto define un blueprint llamado 'auth', y Flask sabrá que todas las rutas aquí dentro empezarán con /auth. Por ejemplo, la función 'register()' tendrá una ruta '/auth/register'.


RUTA DE REGISTRO (/auth/register)
@bp.route('/register', methods=('GET', 'POST'))
def register():
-> Esta función tiene dos propósitos:
1. Mostrar el formulario (cuando el método es GET).
2. Procesar el formulario (cuando el método es POST).

Si el método es POST:
if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
-> Obtiene los datos del formulario.

Luego se crea un nuevo objeto User:
user = User(username, generate_password_hash(password))
-> Aquí la contraseña se convierte en un hash antes de guardarla.

Comprobación de usuario duplicado:
user_name = User.query.filter_by(username=username).first()
-> Busca si ya existe un usuario con ese nombre.

- Si no existe, agrega el usuario a la base de datos:
db.session.add(user)
db.session.commit()
return redirect(url_for('auth.login'))
-> Luego redirige al formulario de login.

- Si ya existe, genera un mensaje de error:
error = f'El usuario {username} ya esta registrado'
flash(error)

Si el método es GET:
Si no se envía el formulario (solo se visita la URL), simplemente renderiza la plantilla:
return render_template('auth/register.html')



RUTA DE INICIO DE SESIÓN (/auth/login)
@bp.route('/login', methods=('GET', 'POST'))
def login():
-> Esta ruta tiene un objetivo muy claro:
1. Permitir que un usuario existente se autentique en la aplicación (es decir, comprobar su identidad y crear una sesión activa para él).

En otras palabras, el login es el paso en el que el usuario 'demuestra' quién es, y Flask guarda esa información temporalmente para que el resto de la aplicación sepa quién está usando el sistema. 

Si el método es POST:
1. Se obtienen los datos del formulario:
username = request.form['username']
password = request.form['password']

2. Se busca el usuario en la base de datos:
user = User.query.filter_by(username=username).first()

3. Se valida:

    - Si no existe el usuario:
    error = 'Nombre de usuario incorrecto'

    - Si la contraseña no coincide con el hash almacenado:
    elif not check_password_hash(user.password, password):
    error = 'Contraseña incorrecta'

4. Si no hay error, se inicia sesión:
session.clear()
session['user_id'] = user.id
db.session.commit()
return redirect(url_for('todo.index'))

Aquí sucede algo importante:
- session.clear() limpia cualquier dato previo.
- session['user_id'] = user.id guarda el ID del usuario logueado.
- Eso permitirá reconocer quién está usando la app en las siguientes peticiones.

(Nota: db.session.commit() aquí no es estrictamente necesario, ya que no se modifica la base de datos al hacer login, pero no causa error.)

5. Si hubo un error, lo muestra con flash(error).
Renderiza el formulario:
return render_template('auth/login.html')


"""