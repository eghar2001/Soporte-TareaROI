from flask import Blueprint, render_template, flash
from datetime import datetime
from eggList.usuarios import data as data_usuarios
from flask_login import current_user
from sqlalchemy import func
from eggList.models import ListaProductos
from eggList.grupos_familiares import data as data_grupo_familiar
from eggList.provincias import logic as provincia_logic
main = Blueprint('main',__name__)


@main.route("/home")
@main.route("/")
def home():
    if current_user.is_authenticated:
        listas_semanales = data_usuarios.get_listas_semanales()
        ultimas_3_compras = data_usuarios.get_ultimas_n_compras()
        provincias = provincia_logic.find_all()
        return render_template('main/home.html',listas_semanales = listas_semanales, ultimas_compras = ultimas_3_compras,
                               provincias = provincias)
    else:
        return render_template('main/home.html')
