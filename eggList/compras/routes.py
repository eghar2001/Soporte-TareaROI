import datetime
from typing import List

from flask import Blueprint, render_template, request, flash, abort, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import and_

from eggList.compras.form import CompraBusquedaForm
from eggList.models import Compra, Supermercado, Usuario
from eggList.usuarios.logic import user_roles_required
from eggList.usuarios import data as data_usuarios


compras = Blueprint('compras', __name__)

@compras.route("/compras/mis-compras")
@login_required
@user_roles_required("Usuario")
def mis_compras():
    page = request.args.get('page', 1, type=int)
    form = CompraBusquedaForm()
    compras:List[Compra]

    fecha_desde_str = request.args.get('fecha_desde', type=str)
    fecha_hasta_str = request.args.get('fecha_hasta', type=str)
    supermercado_id = request.args.get('supermercado',type=int)
    if fecha_desde_str or fecha_hasta_str or supermercado_id:
        fecha_desde:datetime.datetime = datetime.datetime.strptime(fecha_desde_str, '%Y-%m-%d') if fecha_desde_str else datetime.datetime.strptime("0001-01-01", '%Y-%m-%d')
        fecha_hasta: datetime.datetime=  datetime.datetime.strptime(fecha_hasta_str, '%Y-%m-%d') + datetime.timedelta(days=1) if fecha_hasta_str else datetime.datetime.utcnow() + datetime.timedelta(days = 1)
        supermercado:Supermercado = Supermercado.query.get_or_404(supermercado_id) if supermercado_id != 0 else None
        if fecha_desde > fecha_hasta:
            flash("No ingreso fechas validas", "danger")
            return redirect(url_for("compras.mis_compras"))
        compras = data_usuarios.get_compras_con_filtros_paginate(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,
                                                               page=page, supermercado = supermercado)
    else:
        compras = data_usuarios.get_compras_paginate(page = page)

    supermercados = data_usuarios.get_supermercados()
    form.supermercado.choices = [(0,"Cualquiera")]
    form.supermercado.choices += [(super.id, str(super)) for super in supermercados]
    return render_template("compras/mis-compras.html", compras = compras, form = form)


@compras.route("/compras/compra/<int:compra_id>")
@login_required
@user_roles_required("Usuario")
def compra(compra_id:int):
    compra = Compra.query.get_or_404(compra_id)
    if not compra.id_comprador == current_user.id:
        abort(403)
    return render_template("/compras/compra.html", compra = compra)