from flask import Blueprint, render_template, flash
from datetime import datetime
from eggList.models import ListaProductos
main = Blueprint('main',__name__)


@main.route("/home")
@main.route("/")
def home():
    listas = ListaProductos.query.order_by(ListaProductos.fecha_creacion.desc()).all()
    if not listas:
        flash("No hay listas disponibles, por favor agregue", "primary")

    semana = listas[0].get_semana()
    listas_por_semana = [(semana,[])]
    index = 0
    for lista in listas:
        if lista.get_semana() == semana:
            listas_por_semana[index][1].append(lista)
        else:
            semana = lista.get_semana()
            listas_por_semana.append((semana,[lista]))
            index += 1


    print(listas_por_semana)

    return render_template('main/home.html', listas_por_semana = listas_por_semana)
