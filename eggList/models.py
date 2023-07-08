from datetime import datetime, timedelta

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import UniqueConstraint

from eggList import db, login_manager
from flask_login import UserMixin


class Producto(db.Model):
    """
    Clase que representa un producto a comprar en un supermercado
    """
    __tablename__ = "productos"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=True)
    cantidad = db.Column(db.Integer(), nullable=False, default=1)
    esta_en_carrito = db.Column(db.Boolean(), default=False)
    id_lista = db.Column(db.Integer(), db.ForeignKey('listas.id'))
    id_compra = db.Column(db.Integer, db.ForeignKey('compras.id'))


    def get_total(self):
        if self.precio:
            return self.precio * self.cantidad
        return self.cantidad


class Compra(db.Model):
    __tablename__="compras"

    id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    fecha_compra = db.Column(db.DateTime(), nullable = False, default = datetime.utcnow())
    productos = db.relationship("Producto")
    id_comprador = db.Column(db.Integer(), db.ForeignKey("usuarios.id"))

class ListaProductos(db.Model):
    """
    Clase que representa un lista de supermercado que contiene productos
    """
    __tablename__ = "listas"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    id_autor = db.Column(db.Integer(), db.ForeignKey('usuarios.id'), nullable=False)
    autor = db.relationship('Usuario')
    usuarios = db.relationship('Usuario',secondary = "usuarios_listas" , back_populates = "listas")
    productos = db.relationship('Producto')

    def agregar_producto(self, producto: Producto):
        self.productos.append(producto)

    def get_total(self):
        total = 0
        for producto in self.productos:
            if producto.esta_en_carrito and producto.precio:
                total += producto.get_total()
        return total

    def get_semana(self):
        return self.fecha_creacion.date() - timedelta(days=self.fecha_creacion.weekday())

    def usuario_valido(self, user):
        es_familiar = False
        return self.autor == user or user in self.usuarios




class GrupoFamiliar(db.Model):
    """
    Clase que representa un grupo familiar dentro del programa
    Es decir, un conjunto de usuarios. Su mayor utilidad es para compartirse las listas
    """
    __tablename__ = "grupos_familiares"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nombre_familia = db.Column(db.String(50), nullable=False, unique=True)
    integrantes = db.relationship('Usuario', back_populates="grupo_familiar")

    def agregar_integrante(self, nuevo_integrante):
        if isinstance(nuevo_integrante, Usuario):
            self.integrantes.append(nuevo_integrante)


class RolLista(db.Model):
    """Clase que representa el rol de un usuario dentro de una lista"""
    __tablename__ = "roles_en_lista"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<RolLista {self.name}>"

    def __eq__(self, other):
        return self.name == other.name

    def es_rol(self, rol: str):
        return self.name == rol


class RolUsuario(db.Model):
    """Clase que representa el rol del usuario en el programa(NO EN UNA LISTA)"""
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

    def es_rol(self, rol: str):
        return self.name == rol

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<RolUsuario {self.name}>"

    def __eq__(self, other):
        return self.name == other.name

#Clase Usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))




class Usuario(db.Model, UserMixin):
    """Clase que representa la entidad usuario en el modelo"""
    __tablename__ = "usuarios"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime(), nullable=True)
    imagen_perfil = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    fecha_creacion = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    roles = db.relationship('RolUsuario', secondary='usuarios_roles')


    id_grupo_familiar = db.Column(db.Integer(), db.ForeignKey('grupos_familiares.id'), nullable=True)
    grupo_familiar = db.relationship('GrupoFamiliar', back_populates="integrantes")

    # Posible mapeo a borrar
    listas = db.relationship('ListaProductos', secondary = "usuarios_listas", back_populates = "usuarios")

    def __eq__(self, other):
        return self.id == other.id

    def has_user_role(self, rol_str: str) -> bool:
        return any([rol_str == rol.name for rol in self.roles])

    def get_id_token(self, expires_sec: int = 1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def add_user_role(self, role: RolUsuario):
        self.roles.append(role)

    def es_familiar_de(self, user):
        if self.grupo_familiar:
            return user in self.grupo_familiar.integrantes
        return False

    def esta_confirmado(self):
        return bool(self.email_confirmed_at)


#TABLAS INTERMEDIAS

class UsuarioLista(db.Model):
    """Clase que representa la tabla intermedia entre un usuario y su listas"""
    __tablename__ = 'usuarios_listas'
    usuario_id = db.Column( db.Integer(), db.ForeignKey('usuarios.id'), primary_key = True)
    lista_id = db.Column( db.Integer(), db.ForeignKey('listas.id'), primary_key=True)
    role_id = db.Column( db.Integer(),db.ForeignKey('roles_en_lista.id'), nullable = False)
    role = db.relationship("RolLista")


usuarios_roles = db.Table('usuarios_roles',
                          db.Column('usuario_id', db.Integer(), db.ForeignKey('usuarios.id')),
                          db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
                          )


