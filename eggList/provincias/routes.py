from flask import Blueprint, jsonify

from eggList.models import Provincia
from eggList.usuarios.logic import user_roles_required

provincias = Blueprint('provincias',__name__)

@provincias.route("/provincia/<int:id_provincia>/ciudades")
def ciudades(id_provincia):
    provincia = Provincia.query.get_or_404(id_provincia)
    ciudades=[]
    for ciudad in provincia.ciudades:
        ciudad_dicc = {"id":ciudad.id, "nombre":ciudad.nombre}
        ciudades.append(ciudad_dicc)
    return jsonify(ciudades)
