from flask import Blueprint, flash, redirect, url_for, request, render_template, abort
from flask_login import login_required, current_user
import eggList.listas.logic as listas_logic
from eggList.models import Producto, ListaProductos
from eggList.productos.forms import CarritoForm, ModificarProductoForm
from eggList.usuarios.logic import user_roles_required
from eggList.productos import logic
productos = Blueprint('productos',__name__)

@productos.route("/producto/<int:producto_id>/borrar", methods = ["POST"])
@login_required
@user_roles_required("Usuario")
def borrar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    lista_id = producto.id_lista
    flash("Su producto ha borrado satisfactoriamente", "primary")
    return redirect(url_for('listas.lista',lista_id = lista_id))


@productos.route("/producto/<int:producto_id>/modificar",methods = ["GET","POST"])
@login_required
@user_roles_required("Usuario")
def modificar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    form = ModificarProductoForm()
    if request.method == "GET":
        form.descripcion.data = producto.descripcion
        form.cantidad.data = producto.cantidad
        form.precio.data = producto.precio
    if form.validate_on_submit():
        logic.modificar_producto(producto,form)
        flash("Tu producto se ha modificado con exito", "success")
        return redirect(url_for("listas.lista",lista_id = producto.id_lista))
    return render_template("productos/modificar_producto_form.html", form = form, lista_id = producto.id_lista)





@productos.route("/producto/<int:producto_id>/agregar_carrito",methods=["POST"])
@login_required
@user_roles_required("Usuario")
def confirmar_carrito(producto_id):

    producto = Producto.query.get_or_404(producto_id)
    lista = ListaProductos.query.get(producto.id_lista)
    if listas_logic.user_has_list_role(lista, current_user, "Comprador"):
        form_carrito = CarritoForm()
        if form_carrito.validate_on_submit():
            logic.poner_en_carrito(producto,form_carrito.precio.data)
            flash(f"{producto.descripcion} esta en carrito ","success")
        return redirect(url_for("listas.lista",lista_id = producto.id_lista))
    else:
        abort(403)


@productos.route("/producto/<int:producto_id>/sacar_de_carrito")
@login_required
@user_roles_required("Usuario")
def sacar_de_carrito(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    lista = ListaProductos.query.get(producto.id_lista)
    if listas_logic.user_has_list_role(lista, current_user, "Comprador"):
        logic.sacar_de_carrito(producto)
        flash(f"Tu producto {producto.descripcion} se ha retirado del carrito","success")
        return redirect(url_for("listas.lista", lista_id = producto.id_lista))
    else:
        abort(403)
