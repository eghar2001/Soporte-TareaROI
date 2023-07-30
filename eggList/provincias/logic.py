from eggList.models import Provincia, Ciudad


def find_all():
    provincias = Provincia.query.order_by(Provincia.nombre.asc()).all()
    return provincias




def get_ciudades(prov_id:int):
    ciudades = Ciudad.query.filter(Ciudad.id_provincia == prov_id).order_by(Ciudad.nombre.asc()).all()
    return ciudades