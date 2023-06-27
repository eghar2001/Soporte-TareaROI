from datetime import datetime, timedelta
from eggList import db


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=True)
    cantidad = db.Column(db.Integer(), nullable=False, default = 1)
    esta_en_carrito = db.Column(db.Boolean(), default = False)
    id_lista = db.Column(db.Integer(), db.ForeignKey('listas.id'))

    def get_total(self):
        if self.precio:
            return self.precio * self.cantidad
        return self.cantidad


class ListaProductos(db.Model):
    __tablename__ = "listas"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100), nullable = False)
    fecha_creacion = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())

    id_usuario = db.Column(db.Integer(), db.ForeignKey('usuarios.id'), nullable=False)
    autor = db.relationship('Usuario')
    productos = db.relationship('Producto')

    def agregar_producto(self, producto:Producto):
        self.productos.append(producto)

    def get_total(self):
        total = 0
        for producto in self.productos:
            if producto.esta_en_carrito and producto.precio:
                total += producto.get_total()
        return total

    def get_semana(self):
        return self.fecha_creacion - timedelta(days = self.fecha_creacion.weekday())


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    imagen_perfil = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    fecha_creacion = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
