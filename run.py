from app import create_app, db
from app.models import Guarderia, Cuidador, Perro, Usuario
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text, create_engine

app = create_app()

with app.app_context():
    try:
        # Crear una conexión inicial sin especificar la base de datos
        base_uri = app.config["SQLALCHEMY_DATABASE_URI"]
        server_uri = base_uri.rsplit('/', 1)[0]  # Conectar solo al servidor MySQL
        engine = create_engine(server_uri)

        with engine.connect() as connection:
            # Crear la base de datos si no existe
            connection.execute(text("CREATE DATABASE IF NOT EXISTS tablas"))

        # Volver a conectar a la base de datos especificada
        engine = db.get_engine()

        with engine.connect() as connection:
            connection.execute(text("USE tablas"))

        # Crear las tablas si no existen
        db.create_all()
        print("Base de datos y tablas creadas con éxito.")

    except ProgrammingError as e:
        print(f"Error creando la base de datos o tablas: {e}")

# Crear usuarios de prueba
usuarios = [
    Usuario(1, "admin", "adminpass", es_admin=True),  # Usuario administrador
    Usuario(2, "user1", "password1"),
    Usuario(3, "user2", "password2"),
]

# Auxiliar para buscar usuario por nombre
def find_user_by_username(username):
    return next((user for user in usuarios if user.username == username), None)

# Mostrar los usuarios creados
if __name__ == "__main__":
    print("Usuarios creados para pruebas:")
    for usuario in usuarios:
        print(usuario)
    app.run(debug=True)
