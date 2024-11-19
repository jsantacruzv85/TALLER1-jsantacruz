# Taller 1 - Sistema de Autenticación en Flask

Este proyecto implementa un sistema de autenticación básico utilizando **Flask** en Python. Los usuarios pueden iniciar sesión, visualizar y gestionar perros, guarderías y cuidadores. El proyecto utiliza **Flask-SQLAlchemy** para interactuar con una base de datos **MySQL**.

## Tabla de contenidos
- [Descripción](#descripción)
- [Características](#características)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Descripción
Este proyecto es una implementación de un sistema de autenticación y autorización basado en Flask. Los usuarios pueden registrarse e iniciar sesión, mientras que los administradores tienen acceso completo para gestionar las entidades **Perro**, **Guardería**, y **Cuidador**.

### Funcionalidades:
- Creación de usuarios y autenticación mediante nombre de usuario y contraseña.
- Roles de usuario: administradores y usuarios normales.
- CRUD (Crear, Leer, Actualizar, Eliminar) para **Perros**, **Guarderías**, y **Cuidadores**.
- La base de datos se puede poblar automáticamente con datos iniciales.
- Seguridad de autenticación y autorización para restringir el acceso a las vistas de administración.

## Características
- **Autenticación**: Los usuarios pueden iniciar sesión con sus credenciales, y el sistema les da acceso a la vista adecuada según su rol (normal o administrador).
- **Base de datos**: Implementada con **MySQL** y gestionada mediante **Flask-SQLAlchemy**.
- **Interfaz de usuario**: El panel de administración permite gestionar las entidades (Perros, Guarderías, y Cuidadores) de manera fácil y rápida.
- **Datos iniciales**: Se puede poblar la base de datos con datos de ejemplo desde el panel de administrador.

## Tecnologías utilizadas
- **Flask**: Framework de microservicios en Python.
- **Flask-SQLAlchemy**: ORM para manejar la base de datos.
- **MySQL**: Sistema de gestión de base de datos.
- **Bootstrap**: Framework CSS para mejorar el diseño de la interfaz.
- **Python 3.x**: Lenguaje de programación utilizado.

## Instalación

Para instalar y ejecutar el proyecto, sigue estos pasos:

### 1. Clona el repositorio
```bash
git clone https://github.com/jsantacruzv85/TALLER1-jsantacruz.git
cd TALLER1-jsantacruz
