from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from eggList import db
from eggList.grupos_familiares.forms import CrearGrupoFamiliarForm, AgregarUsuarioForm
from eggList.models import GrupoFamiliar, Usuario
from eggList.utils import send_email
from eggList.usuarios.logic import verify_id_token, user_roles_required,get_user_by_email
from eggList.grupos_familiares import logic as grupo_logic

grupos_familiares = Blueprint('grupos_familiares',__name__)

@grupos_familiares.route("/grupo_familiar/crear",methods = ["GET","POST"])
@login_required
@user_roles_required("Usuario")
def crear_grupo_familiar():
    form = CrearGrupoFamiliarForm()
    if form.validate_on_submit():
        grupo = GrupoFamiliar(
            nombre_familia = form.familia.data,
            integrantes = [current_user, ]
        )
        grupo_logic.crear_grupo(grupo)
        flash("Su grupo familiar se a creado correctamente", "success")
        return redirect(url_for('grupos_familiares.grupo_familiar'))

    return render_template('grupos_familiares/crear_grupo_form.html', form=form)

@grupos_familiares.route("/grupo_familiar")
@login_required
@user_roles_required("Usuario")
def grupo_familiar():
    form = AgregarUsuarioForm()
    return render_template("grupos_familiares/grupo_familiar.html",form = form)

@grupos_familiares.route("/grupo_familiar/agregar_usuario",methods=["POST"])
@login_required
@user_roles_required("Usuario")
def agregar_usuario():
    form = AgregarUsuarioForm()
    if form.validate_on_submit():
        usuario_a_agregar = get_user_by_email(form.email_usuario.data)
        if not usuario_a_agregar or not usuario_a_agregar.esta_confirmado():
            flash("No se ha encontrado el usuario, por favor intente denuevo","danger")
            return redirect(url_for('grupos_familiares.grupo_familiar'))
        if current_user.es_familiar_de(usuario_a_agregar):
            flash("El main ingresado ya se encuentra dentro de los integrantes de su grupo familiar", "warning")
            return redirect(url_for('grupos_familiares.grupo_familiar'))
        send_email([usuario_a_agregar],
                   title = f"'{current_user.nombre} {current_user.apellido}' te invitado de su grupo familiar",
                   body=f"""Si desea unirse al grupo familiar '{current_user.grupo_familiar.nombre_familia}', dirijase al siguiente link
{url_for('grupos_familiares.confirmar_usuario',grupo_familiar=current_user.grupo_familiar.nombre_familia, confirm_token = usuario_a_agregar.get_id_token(), _external=True)}                   
                            
Caso contrario, ignore este email
""")
        flash(f"Se ha enviado la invitacion a '{usuario_a_agregar.email}'","primary")
        return redirect(url_for('grupos_familiares.grupo_familiar'))


@grupos_familiares.route("/grupo_familiar/<string:grupo_familiar>/confirmar_usuario/<confirm_token>")
@login_required
@user_roles_required("Usuario")
def confirmar_usuario(grupo_familiar, confirm_token):
    grupo = grupo_logic.get_grupo_by_nombre(grupo_familiar)
    usuario_nuevo = verify_id_token(confirm_token)
    if  not grupo:
        abort(404)
    if not usuario_nuevo:
        flash("Expiró la solicitud entrar al grupo familiar, por favor intente de nuevo","warning")
        return redirect(url_for('main.home'))
    grupo_logic.agregar_integrante(grupo,usuario_nuevo)
    flash(f"'{usuario_nuevo.email}' se ha unido satisfactoriamente al grupo familiar '{grupo.nombre_familia}'", "success")
    return redirect(url_for('usuarios.login'))



