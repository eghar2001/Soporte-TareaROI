from datetime import timedelta, datetime

from flask import Blueprint, flash, render_template, redirect, url_for, session, abort, request
from flask_login import login_required, login_user, current_user, logout_user

from eggList import db,bcrypt
from eggList.models import Usuario, ListaProductos, RolUsuario, RolLista, Provincia, Ciudad
from eggList.usuarios.forms import LoginForm, UserForm, ActualizarPerfilForm
from eggList.usuarios import logic as usuario_logic
from eggList.utils import send_email, save_profile_picture
from eggList.provincias import logic as provincia_logic
usuarios = Blueprint('usuarios', __name__)


@usuarios.route("/login",methods = ["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = usuario_logic.get_user_by_email(form.email.data)
        if not user:
            flash("Está mal el email","danger")
            return redirect(url_for('usuarios.login'))
        if not user.email_confirmed_at:
            flash("No verificó el email, por favor intente registrarse denuevo", "danger")
            return redirect(url_for('usuarios.register'))
        if not user.check_password(form.password.data):
            flash("Está mal la contraseña","danger")
            return redirect(url_for('usuarios.login'))

        login_user(user, form.remember.data, duration = timedelta(minutes=30))
        flash("Se ha logueado correctamente","success")
        return redirect(url_for('main.home'))
    return render_template("usuarios/login.html", form = form)


@usuarios.route("/register",methods = ["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = UserForm()

    if form.validate_on_submit():
        user=usuario_logic.create_user(form)
        flash(f"Se ha enviado un correo de verificación a '{user.email}'", "primary")
        return redirect(url_for('main.home'))
    return render_template("/usuarios/register.html", form = form)

@usuarios.route("/confirm_register/<confirm_token>")
def confirm_register(confirm_token):
    user = usuario_logic.verify_id_token(confirm_token)
    if user:
        usuario_logic.confirm_user(user)
        flash("Su usuario se ha registrado correctamente","success")
        return(redirect(url_for("main.home")))
    else:
        flash("Su intento de registro venció, por favor intente de nuevo", "danger")
        return redirect(url_for("usuarios.register"))


@usuarios.route("/perfil/<string:usuario_email>")
@login_required
@usuario_logic.user_roles_required("Usuario")
def perfil(usuario_email):
    usuario= usuario_logic.get_user_by_email(usuario_email)
    if not usuario:
        abort(404)

    return render_template("usuarios/perfil.html", usuario = usuario)


@usuarios.route("/perfil/actualizar/<string:usuario_email>", methods=["GET", "POST"])
@login_required
@usuario_logic.user_roles_required("Usuario")
def actualizar(usuario_email):
    usuario = usuario_logic.get_user_by_email(usuario_email)
    if not usuario:
        abort(404)
    if usuario != current_user:
        abort(403)
    form = ActualizarPerfilForm()

    if request.method == "POST" and form.validate_on_submit():

        usuario.nombre = form.nombre.data
        usuario.apellido = form.apellido.data
        usuario.email = form.email.data
        usuario.telefono = int(form.telefono.data)
        if form.imagen_perfil.data:
            print(type(form.imagen_perfil.data))
            usuario.imagen_perfil = save_profile_picture(form.imagen_perfil.data)



        db.session.commit()
        flash("Se ha actualizado tu usuario correctamente", "success")
        return redirect(url_for("usuarios.perfil",usuario_email = usuario.email))
    form.nombre.data = current_user.nombre
    form.apellido.data = current_user.apellido
    form.email.data = current_user.email
    form.telefono.data = current_user.telefono
    return render_template("usuarios/actualizar_perfil.html", usuario = usuario, form = form)


@usuarios.route("/logout")
@login_required
@usuario_logic.user_roles_required("Usuario")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('main.home'))


@usuarios.route("/set_location/<int:ciudad_id>", methods=["POST"])
@login_required
@usuario_logic.user_roles_required("Usuario")
def set_location(ciudad_id):
    ciudad = Ciudad.query.get_or_404(ciudad_id)
    current_user.id_ciudad= ciudad.id
    db.session.commit()
    return redirect(url_for("main.home"))