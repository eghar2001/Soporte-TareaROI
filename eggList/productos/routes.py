from flask import Blueprint, flash, redirect, url_for, request, render_template
from eggList import db
from eggList.models import Producto
from eggList.productos.forms import AgregarProductoForm, CarritoForm, ModificarProductoForm
productos = Blueprint('productos',__name__)

@productos.route("/producto/<int:producto_id>/borrar", methods = ["POST"])
def borrar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    lista_id = producto.id_lista
    db.session.delete(producto)
    db.session.commit()
    flash("Su producto ha borrado satisfactoriamente", "primary")
    return redirect(url_for('listas.lista',lista_id = lista_id))


@productos.route("/producto/<int:producto_id>/modificar",methods = ["GET","POST"])
def modificar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    lista_id = producto.id_lista
    form = ModificarProductoForm()
    if request.method == "GET":
        form.descripcion.data = producto.descripcion
        form.cantidad.data = producto.cantidad
        form.precio.data = producto.precio
    if form.validate_on_submit():
        producto.descripcion = form.descripcion.data
        producto.cantidad = form.cantidad.data
        producto.precio = form.precio.data
        db.session.commit()
        flash("Tu producto se ha modificado con exito", "success")
        return redirect(url_for("listas.lista",lista_id = producto.id_lista))
    return render_template("productos/modificar_producto_form.html", form = form, lista_id = producto.id_lista)


@productos.route("/producto/<int:producto_id>/agregar_precio",methods=["POST"])
def confirmar_carrito(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    form_carrito = CarritoForm()
    if form_carrito.validate_on_submit():
        producto.precio = form_carrito.precio.data
        producto.esta_en_carrito = True
        db.session.commit()
        flash(f"{producto.descripcion} esta en carrito ","success")
    return redirect(url_for("listas.lista",lista_id = producto.id_lista))


@productos.route("/producto/<int:producto_id>/sacar_de_carrito")
def sacar_de_carrito(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    producto.esta_en_carrito = False
    db.session.commit()
    flash(f"Tu producto {producto.descripcion} se ha retirado del carrito","success")
    return redirect(url_for("listas.lista", lista_id = producto.id_lista))
