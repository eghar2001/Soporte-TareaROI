from eggList.models import Supermercado


def find_all():
    supermercados = Supermercado.query.all()
    return supermercados