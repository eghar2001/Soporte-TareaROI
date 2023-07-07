from eggList import db
from eggList.models import Producto
from eggList.productos.forms import ModificarProductoForm

def poner_en_carrito(producto:Producto, precio = 0):
    producto.precio = precio
    producto.esta_en_carrito = True
    db.session.commit()

def sacar_de_carrito(producto:Producto):
    producto.esta_en_carrito = False
    db.session.commit()


def modificar_producto(producto, modificar_prod_form:ModificarProductoForm):
    producto.descripcion = modificar_prod_form.descripcion.data
    producto.cantidad = modificar_prod_form.cantidad.data
    producto.precio = modificar_prod_form.precio.data
    db.session.commit()

def borrar_producto(producto):
    db.session.delete(producto)
    db.session.commit()