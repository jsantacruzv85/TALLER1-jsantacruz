from . import db

class Guarderia(db.Model):
    __tablename__ = 'guarderias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)

    cuidadores = db.relationship('Cuidador', backref='guarderia', lazy=True)
    perros = db.relationship('Perro', backref='guarderia', lazy=True)

class Cuidador(db.Model):
    __tablename__ = 'cuidadores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    id_guarderia = db.Column(db.Integer, db.ForeignKey('guarderias.id'), nullable=False)

    perros = db.relationship('Perro', backref='cuidador', lazy=True)

class Perro(db.Model):
    __tablename__ = 'perros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    raza = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    id_guarderia = db.Column(db.Integer, db.ForeignKey('guarderias.id'), nullable=False)
    id_cuidador = db.Column(db.Integer, db.ForeignKey('cuidadores.id'), nullable=False)


# Clase Usuario
class Usuario:
    def __init__(self, id, username, password, es_admin=False):
        self.id = id
        self.username = username
        self.password = password
        self.es_admin = es_admin

    def check_password(self, password):
        return self.password == password

    def __repr__(self):
        return f"<Usuario {self.username}, Admin: {self.es_admin}>"

# Usuarios de prueba
usuarios = [
    Usuario(1, "admin", "adminpass", es_admin=True),
    Usuario(2, "user1", "password1"),
    Usuario(3, "user2", "password2"),
]
