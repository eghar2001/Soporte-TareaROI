from functools import wraps
from typing import List

from flask import render_template
from flask_login import current_user
from sqlalchemy import and_

from eggList import db
from eggList.models import ListaProductos, Producto, UsuarioLista, Usuario, RolLista, Compra, Supermercado
from eggList.usuarios import logic as usuario_logic


def agregar_producto(lista: ListaProductos, producto: Producto):
    lista.agregar_producto(producto)
    db.session.commit()


def crear_lista(lista: ListaProductos):
    usuarios = lista.usuarios
    lista.usuarios = []
    db.session.add(lista)
    db.session.commit()
    rol_armador = RolLista.query.filter(RolLista.name == "Armador").first()
    for usuario in usuarios:
        db.session.add(UsuarioLista(usuario_id=usuario.id,
                                    lista_id=lista.id,
                                    role=rol_armador))
    db.session.commit()


def buscar_compra_disponible(lista:ListaProductos) -> Compra:
    compra_disponible:Compra = Compra.query.filter(and_(Compra.id_lista == lista.id, Compra.fecha_compra==None )).first()
    return compra_disponible

def buscar_rol_usuario(lista: ListaProductos) -> RolLista:
    user_lista = buscar_user_lista(lista)
    return user_lista.role


def actualizar_rol(lista: ListaProductos, rol_lista_str: str, commit:bool = False):
    rol_lista = RolLista.query.filter(RolLista.name == rol_lista_str).first()
    user_lista = buscar_user_lista(lista)
    if rol_lista and user_lista:
        user_lista.role = rol_lista
        if commit:
            db.session.commit()


def user_has_list_role(lista: ListaProductos,  rol_lista_str: str = "Armador",user:Usuario = current_user)-> bool:
    user_lista = buscar_user_lista(lista, user)
    return user_lista.role.name == rol_lista_str



def buscar_user_lista(lista:ListaProductos, user:Usuario = current_user) -> UsuarioLista:
    user_lista = UsuarioLista.query.filter(and_(UsuarioLista.usuario_id == user.id, UsuarioLista.lista_id == lista.id)).first()
    return user_lista


def en_supermercado(lista, supermercado:Supermercado):
    actualizar_rol(lista, "Comprador")
    compra_disponible =  buscar_compra_disponible(lista)
    if not compra_disponible:
        compra = Compra(id_lista = lista.id, id_supermercado = supermercado.id)
        db.session.add(compra)
    db.session.commit()


def salir_del_super(lista:ListaProductos):
    for prod in lista.productos:
        if prod.esta_en_carrito and not prod.id_compra:
            prod.esta_en_carrito = False
    compra_disponible = buscar_compra_disponible(lista)
    db.session.delete(compra_disponible)
    db.session.commit()









