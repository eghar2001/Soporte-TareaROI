from datetime import datetime, timedelta

from eggList import db
from eggList.models import ListaProductos


def get_listas_semanales():
    """Retorna todas las listas que se crearon esta semana"""
    este_lunes = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday(),
                                               hours=datetime.utcnow().hour,
                                               minutes=datetime.utcnow().minute,
                                               seconds=datetime.utcnow().second)

    listas_semanales = ListaProductos.query \
        .filter(ListaProductos.fecha_creacion > este_lunes) \
        .order_by(ListaProductos.fecha_creacion.desc()).all()
    return listas_semanales