from flask import Blueprint, render_template, request, flash, redirect, url_for
from eggList import db
from eggList.models import ListaProductos, Producto, Usuario
from eggList.productos.forms import AgregarProductoForm, CarritoForm

listas = Blueprint('listas', __name__)





@listas.route("/lista/<int:lista_id>")
def lista(lista_id):
    lista = ListaProductos.query.get_or_404(lista_id)
    form_carrito = CarritoForm()
    productos_en_carrito = []
    productos_fuera_de_carrito = []
    for producto in lista.productos:
        if producto.esta_en_carrito:
            productos_en_carrito.append(producto)
        else:
            productos_fuera_de_carrito.append(producto)


    total = lista.get_total()
    return render_template("listas/lista.html", lista = lista,
                           productos_en_carrito = productos_en_carrito, productos_fuera_de_carrito = productos_fuera_de_carrito,
                           form_carrito = form_carrito, total = total)


@listas.route("/lista/<int:lista_id>/agregar", methods = ["GET","POST"])
def agregar_producto(lista_id):
    lista = ListaProductos.query.get_or_404(lista_id)
    form = AgregarProductoForm()
    if form.validate_on_submit():
        producto = Producto(descripcion = form.descripcion.data,
                            cantidad = form.cantidad.data)
        lista.agregar_producto(producto)
        db.session.commit()
        flash(f'Se agregó correctamente el producto {producto.descripcion} a tu lista!', "success")
        return redirect(url_for('listas.lista', lista_id = lista.id))

    return render_template('productos/agregar_producto_form.html', form = form, lista_id = lista.id)

