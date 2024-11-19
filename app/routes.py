from flask import Blueprint, jsonify, request, session, redirect, url_for, render_template, flash
from functools import wraps
from .models import Guarderia, Cuidador, Perro, usuarios
from . import db

main_bp = Blueprint('main', __name__)

# Definir la función auxiliar para buscar usuarios
def find_user_by_username(username):
    return next((user for user in usuarios if user.username == username), None)

# Decorador para verificar si el usuario ha iniciado sesión
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Debes iniciar sesión para acceder a esta página.")
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para verificar si el usuario es administrador
def admin_required(f):
    @wraps(f)
    @login_required  # Requiere que el usuario esté autenticado
    def decorated_function(*args, **kwargs):
        user = find_user_by_username(session['username'])
        if not user or not user.es_admin:
            flash("No tienes permiso para acceder a esta página.")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    if 'username' in session:
        user = find_user_by_username(session['username'])
        if user:
            return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = find_user_by_username(username)
        if user and user.check_password(password):
            session['username'] = user.username
            return redirect(url_for('main.dashboard'))
        return "Usuario o contraseña incorrectos", 401
    return render_template('login.html')

@main_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.index'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    user = find_user_by_username(session['username'])
    if user.es_admin:
        return render_template('admin_dashboard.html')
    return render_template('user_dashboard.html', user=user)

@main_bp.route('/populate')
@admin_required  # Asegurarse de que solo los administradores puedan ejecutar esto
def populate():
    try:
        # Crear datos iniciales
        guarderia = Guarderia(nombre="La favorita", direccion="Calle 123", telefono="123456789")
        db.session.add(guarderia)
        db.session.commit()

        cuidador = Cuidador(nombre="Mario", telefono="987654321", id_guarderia=guarderia.id)
        db.session.add(cuidador)
        db.session.commit()

        perro = Perro(nombre="Lassie", raza="Collie", edad=5, peso=15.0, id_guarderia=guarderia.id, id_cuidador=cuidador.id)
        db.session.add(perro)
        db.session.commit()

        # Mostrar mensaje de éxito
        flash("Base de datos poblada exitosamente con datos iniciales.", "success")
    except Exception as e:
        # Si hay algún error, mostrar un mensaje de error
        flash(f"Hubo un error al poblar la base de datos: {e}", "danger")

    # Redirigir al panel de administrador
    return redirect(url_for('main.dashboard'))

# CRUD para Perros
@main_bp.route('/perros', methods=['GET'])
@admin_required
def listar_perros():
    perros = Perro.query.all()
    return render_template('listar_perros.html', perros=perros)

@main_bp.route('/perros/nuevo', methods=['GET', 'POST'])
@admin_required
def agregar_perro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        raza = request.form['raza']
        edad = int(request.form['edad'])
        peso = float(request.form['peso'])
        id_guarderia = int(request.form['id_guarderia'])
        id_cuidador = int(request.form['id_cuidador'])

        nuevo_perro = Perro(
            nombre=nombre, raza=raza, edad=edad, peso=peso,
            id_guarderia=id_guarderia, id_cuidador=id_cuidador
        )
        db.session.add(nuevo_perro)
        db.session.commit()
        return redirect(url_for('main.listar_perros'))

    guarderias = Guarderia.query.all()
    cuidadores = Cuidador.query.all()
    return render_template('agregar_perro.html', guarderias=guarderias, cuidadores=cuidadores)

@main_bp.route('/perros/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar_perro(id):
    perro = Perro.query.get_or_404(id)

    if request.method == 'POST':
        perro.nombre = request.form['nombre']
        perro.raza = request.form['raza']
        perro.edad = int(request.form['edad'])
        perro.peso = float(request.form['peso'])
        perro.id_guarderia = int(request.form['id_guarderia'])
        perro.id_cuidador = int(request.form['id_cuidador'])

        db.session.commit()
        return redirect(url_for('main.listar_perros'))

    guarderias = Guarderia.query.all()
    cuidadores = Cuidador.query.all()
    return render_template('editar_perro.html', perro=perro, guarderias=guarderias, cuidadores=cuidadores)

@main_bp.route('/perros/eliminar/<int:id>', methods=['POST'])
@admin_required
def eliminar_perro(id):
    perro = Perro.query.get_or_404(id)
    db.session.delete(perro)
    db.session.commit()
    return redirect(url_for('main.listar_perros'))

# CRUD para Guarderias
@main_bp.route('/guarderias', methods=['GET'])
@admin_required
def listar_guarderias():
    guarderias = Guarderia.query.all()
    return render_template('listar_guarderias.html', guarderias=guarderias)

@main_bp.route('/guarderias/nuevo', methods=['GET', 'POST'])
@admin_required
def agregar_guarderia():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        nueva_guarderia = Guarderia(nombre=nombre, direccion=direccion, telefono=telefono)
        db.session.add(nueva_guarderia)
        db.session.commit()
        return redirect(url_for('main.listar_guarderias'))

    return render_template('agregar_guarderia.html')

@main_bp.route('/guarderias/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar_guarderia(id):
    guarderia = Guarderia.query.get_or_404(id)

    if request.method == 'POST':
        guarderia.nombre = request.form['nombre']
        guarderia.direccion = request.form['direccion']
        guarderia.telefono = request.form['telefono']

        db.session.commit()
        return redirect(url_for('main.listar_guarderias'))

    return render_template('editar_guarderia.html', guarderia=guarderia)

@main_bp.route('/guarderias/eliminar/<int:id>', methods=['POST'])
@admin_required
def eliminar_guarderia(id):
    guarderia = Guarderia.query.get_or_404(id)
    db.session.delete(guarderia)
    db.session.commit()
    return redirect(url_for('main.listar_guarderias'))

# CRUD para Cuidadores
@main_bp.route('/cuidadores', methods=['GET'])
@admin_required
def listar_cuidadores():
    cuidadores = Cuidador.query.all()
    return render_template('listar_cuidadores.html', cuidadores=cuidadores)

@main_bp.route('/cuidadores/nuevo', methods=['GET', 'POST'])
@admin_required
def agregar_cuidador():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        id_guarderia = int(request.form['id_guarderia'])

        nuevo_cuidador = Cuidador(nombre=nombre, telefono=telefono, id_guarderia=id_guarderia)
        db.session.add(nuevo_cuidador)
        db.session.commit()
        return redirect(url_for('main.listar_cuidadores'))

    guarderias = Guarderia.query.all()
    return render_template('agregar_cuidador.html', guarderias=guarderias)

@main_bp.route('/cuidadores/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar_cuidador(id):
    cuidador = Cuidador.query.get_or_404(id)

    if request.method == 'POST':
        cuidador.nombre = request.form['nombre']
        cuidador.telefono = request.form['telefono']
        cuidador.id_guarderia = int(request.form['id_guarderia'])

        db.session.commit()
        return redirect(url_for('main.listar_cuidadores'))

    guarderias = Guarderia.query.all()
    return render_template('editar_cuidador.html', cuidador=cuidador, guarderias=guarderias)

@main_bp.route('/cuidadores/eliminar/<int:id>', methods=['POST'])
@admin_required
def eliminar_cuidador(id):
    cuidador = Cuidador.query.get_or_404(id)
    db.session.delete(cuidador)
    db.session.commit()
    return redirect(url_for('main.listar_cuidadores'))
