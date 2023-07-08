from functools import wraps

from flask import render_template
from flask_login import current_user
from sqlalchemy import and_

from eggList import db
from eggList.models import ListaProductos, Producto, UsuarioLista, Usuario, RolLista
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


def buscar_rol(lista: ListaProductos, user: Usuario):
    user_lista = UsuarioLista.query.filter(
        and_(UsuarioLista.usuario_id == user.id, UsuarioLista.lista_id == lista.id)).first()
    return user_lista.role


def actualizar_rol(lista: ListaProductos, user: Usuario, rol_lista_str: str):
    rol_lista = RolLista.query.filter(RolLista.name == rol_lista_str).first()
    user_lista = UsuarioLista.query.filter(
        and_(UsuarioLista.usuario_id == user.id, UsuarioLista.lista_id == lista.id)).first()
    if rol_lista and user_lista:
        user_lista.role = rol_lista
        db.session.commit()


def user_has_list_role(lista: ListaProductos, user: Usuario, rol_lista_str: str):
    user_lista = UsuarioLista.query.filter(
        and_(UsuarioLista.usuario_id == user.id, UsuarioLista.lista_id == lista.id)).first()
    return user_lista.role.name == rol_lista_str
