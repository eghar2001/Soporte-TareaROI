from datetime import datetime, timedelta
from typing import List

from flask import current_app, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import UniqueConstraint

from eggList import db, login_manager, bcrypt
from flask_login import UserMixin, current_user



class Provincia(db.Model):
    __tablename__ = "provincias"

    id = db.Column(db.Integer(),primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(100),nullable = False)
    ciudades = db.relationship("Ciudad",back_populates = "provincia")


class Ciudad(db.Model):
    __tablename__ = "ciudades"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    id_provincia = db.Column(db.Integer(),db.ForeignKey("provincias.id"),nullable = False)
    provincia = db.relationship("Provincia", back_populates="ciudades")
    supermercados = db.relationship("Supermercado", back_populates="ciudad")


class Supermercado(db.Model):
    __tablename__ = "supermercados"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(), nullable=False, unique=False)

    id_ciudad = db.Column(db.Integer(),db.ForeignKey("ciudades.id"),nullable = False)
    ciudad = db.Relationship("Ciudad", back_populates = "supermercados")

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.nombre} ({self.ciudad.nombre}, {self.ciudad.provincia.nombre})"

class Producto(db.Model):
    """
    Clase que representa un producto a comprar en un supermercado
    """
    __tablename__ = "productos"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=True)
    cantidad = db.Column(db.Integer())
    esta_en_carrito = db.Column(db.Boolean(), default=False)
    id_lista = db.Column(db.Integer(), db.ForeignKey('listas.id'))
    id_compra = db.Column(db.Integer(), db.ForeignKey('compras.id'))
    id_autor = db.Column(db.Integer(), db.ForeignKey('usuarios.id'), nullable=False)
    autor = db.Relationship('Usuario')

    def get_total(self):
        if self.precio:
            return self.precio * self.cantidad
        return self.cantidad





class Compra(db.Model):
    __tablename__ = "compras"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    fecha_compra = db.Column(db.DateTime(),nullable = True)
    productos = db.relationship("Producto")
    id_comprador = db.Column(db.Integer(), db.ForeignKey("usuarios.id"),nullable = True)
    id_lista = db.Column(db.Integer(), db.ForeignKey("listas.id"), nullable =False)
    id_supermercado = db.Column(db.Integer, db.ForeignKey("supermercados.id"), nullable = False)
    supermercado = db.relationship("Supermercado")


    def comprar(self, productos: List[Producto]):
        self.id_comprador = current_user.id
        self.fecha_compra = datetime.utcnow()
        self.productos = productos

    def fue_comprado(self):
        return bool(self.fecha_compra)

    def get_total(self):
        return sum([prod.precio * prod.cantidad for prod in self.productos])


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
    usuarios = db.relationship('Usuario', secondary="usuarios_listas", back_populates="listas")
    productos = db.relationship('Producto')

    def __str__(self):
        return f"ListaProductos<fecha_creacion: {self.fecha_creacion} -- autor: {self.autor.nombre} {self.autor.apellido}>"


    def agregar_producto(self, producto: Producto):
        self.productos.append(producto)

    def get_total(self):
        total = 0
        for producto in self.productos:
            if producto.esta_en_carrito and producto.precio and not producto.id_compra:
                total += producto.get_total()
        return total

    def get_semana(self):
        return self.fecha_creacion.date() - timedelta(days=self.fecha_creacion.weekday())

    def usuario_valido(self, user):
        es_familiar = False
        return self.autor == user or user in self.usuarios

    def faltan_productos(self):
        return any([bool(prod.id_compra) and not prod.esta_en_carrito for prod in self.productos])

class GrupoFamiliar(db.Model):
    """
    Clase que representa un grupo familiar dentro del programa
    Es decir, un conjunto de usuarios. Su mayor utilidad es para compartirse las listas
    """
    __tablename__ = "grupos_familiares"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nombre_familia = db.Column(db.String(50), nullable=False, unique=True)
    imagen_grupo = db.Column(db.String(20), nullable=  False, default = "default.jpg")
    integrantes = db.relationship('Usuario', back_populates="grupo_familiar")

    def agregar_integrante(self, nuevo_integrante):
        if isinstance(nuevo_integrante, Usuario):
            self.integrantes.append(nuevo_integrante)

    def get_img_url(self):
        return url_for('static',filename = "grupo_familiar_pics/"+self.imagen_grupo)        


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




# Clase Usuario
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
    telefono = db.Column(db.String(12), nullable = False)
    imagen_perfil = db.Column(db.String(20), nullable=False, default="default.webp")
    password = db.Column(db.String(60), nullable=False)
    fecha_creacion = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())

    roles = db.relationship('RolUsuario', secondary='usuarios_roles')

    id_grupo_familiar = db.Column(db.Integer(), db.ForeignKey('grupos_familiares.id'), nullable=True)
    grupo_familiar = db.relationship('GrupoFamiliar', back_populates="integrantes")

    id_ciudad =db.Column(db.Integer(),db.ForeignKey("ciudades.id"), nullable=True)
    ciudad = db.relationship('Ciudad')

    # Posible mapeo a borrar
    listas = db.relationship('ListaProductos', secondary="usuarios_listas", back_populates="usuarios")

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def get_img_url(self):
        return url_for('static',filename = f'profile_pics/{current_user.imagen_perfil}')

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

    def check_password(self, password:str):
        return bcrypt.check_password_hash(self.password, password)


# TABLAS INTERMEDIAS

class UsuarioLista(db.Model):
    """Clase que representa la tabla intermedia entre un usuario y su listas"""
    __tablename__ = 'usuarios_listas'
    usuario_id = db.Column(db.Integer(), db.ForeignKey('usuarios.id'), primary_key=True)
    lista_id = db.Column(db.Integer(), db.ForeignKey('listas.id'), primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles_en_lista.id'), nullable=False)
    role = db.relationship("RolLista")


usuarios_roles = db.Table('usuarios_roles',
                          db.Column('usuario_id', db.Integer(), db.ForeignKey('usuarios.id')),
                          db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
                          )
