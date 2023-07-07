from eggList import db
from eggList.models import GrupoFamiliar, Usuario


def crear_grupo(grupo:GrupoFamiliar):
    db.session.add(grupo)
    db.session.commit()


def get_grupo_by_nombre(nombre: str):
    return GrupoFamiliar.query.filter(GrupoFamiliar.nombre_familia == nombre).first()


def agregar_integrante(grupo:GrupoFamiliar, usuario:Usuario):

    usuario.grupo_familiar = None
    grupo.agregar_integrante(usuario)
    db.session.commit()