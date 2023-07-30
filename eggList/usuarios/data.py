from operator import and_
from typing import List, Optional
from datetime import datetime, timedelta
from flask_login import current_user

from eggList import db
from eggList.models import ListaProductos, Usuario, Compra, Supermercado
from sqlalchemy import func

from eggList.listas import data as data_listas







def get_listas_semanales(user:Usuario = current_user):
    """Retorna las listas de esta semana la cual el user es usuario """
    listas_semanales = data_listas.get_listas_semanales()
    for lista in listas_semanales:
        listas_familiares_semanales = list(filter(lambda lista: user in lista.usuarios, listas_semanales))
        return listas_familiares_semanales


def get_compras_paginate(page:int = 1,user:Usuario = current_user):
    compras = Compra.query.filter(Compra.id_comprador == user.id).order_by(Compra.fecha_compra.desc()).paginate(max_per_page=5, page=page)
    return compras

def get_compras(user:Usuario = current_user):
    compras = Compra.query.filter(Compra.id_comprador == user.id).all()
    return compras

def get_compras_en_fechas(fecha_desde:datetime.date, fecha_hasta: datetime.date, user:Usuario = current_user):
    compras_en_fechas = Compra.query.filter(and_(Compra.id_comprador == user.id,and_( Compra.fecha_compra>fecha_desde, Compra.fecha_compra<fecha_hasta)))\
                        .order_by(Compra.fecha_compra.desc()).all()
    return compras_en_fechas

def get_compras_con_filtros_paginate(supermercado:Supermercado,
                                     fecha_desde:datetime.date,
                                     fecha_hasta: datetime.date,
                                     user:Usuario = current_user,
                                     page:int = 1):
    compras_en_fecha:List[Compra]=[]
    if supermercado:
        compras_en_fechas = Compra.query.filter(
            and_(Compra.id_comprador == user.id,and_( Compra.id_supermercado == supermercado.id,and_(Compra.fecha_compra>=fecha_desde, Compra.fecha_compra<=fecha_hasta))))\
                            .order_by(Compra.fecha_compra.desc()).paginate(per_page=5, page = page)
    else:
        compras_en_fechas = Compra.query.filter(
            and_(Compra.id_comprador == user.id, and_(Compra.fecha_compra >= fecha_desde,
                 Compra.fecha_compra <= fecha_hasta))) \
            .order_by(Compra.fecha_compra.desc()).paginate(per_page=5, page=page)
    return compras_en_fechas


def get_ultima_compra(user:Usuario = current_user):
   compras = get_compras(user)
   ultima_fecha = max([compra.fecha_compra for compra in compras])
   ultima_compra:Compra = None
   for compra in compras:
       if compra.fecha_compra == ultima_fecha:
           ultima_compra = compra
   return ultima_compra



def get_ultimas_n_compras(n:int = 3, user:Usuario = current_user):
    compras= Compra.query.filter(Compra.id_comprador == user.id).order_by(Compra.fecha_compra.desc()).limit(n).all()
    return compras


def get_supermercados(user:Usuario = current_user):
    supermercados = db.session.query(Compra.id_supermercado).filter(Compra.id_comprador == user.id).distinct().all()
    supermercados = [Supermercado.query.get(super[0]) for super in supermercados]
    return supermercados