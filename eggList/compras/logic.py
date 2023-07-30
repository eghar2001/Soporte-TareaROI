from typing import List

from eggList import db
from eggList.models import Compra, Producto
from eggList.listas import logic as lista_logic

def comprar(compra:Compra, productos:List[Producto], commit:bool=False):
    compra.comprar(productos)
    if commit:
        db.session.commit()







