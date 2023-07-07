from datetime import timedelta, datetime

from flask import Blueprint, flash, render_template, redirect, url_for, session, abort
from flask_login import login_required, login_user, current_user, logout_user

from eggList import db,bcrypt
from eggList.models import Usuario, ListaProductos, RolUsuario, RolLista
from eggList.usuarios.forms import LoginForm, RegisterForm
from eggList.usuarios import logic as usuario_logic
from eggList.utils import send_email

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
        if not bcrypt.check_password_hash(user.password, form.password.data):
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
    form = RegisterForm()
    if form.validate_on_submit():
        user=usuario_logic.create_user(form)
        send_email(users=[user], title="Creacion de cuenta en EggList",
                   body=f"""Usted ha solicitado crear una cuenta en eggList
Por favor, dirijase al siguiente link si quiere confirmar la cuenta:
{url_for('usuarios.confirm_register', confirm_token=user.get_id_token(), _external=True)}

Si no fue usted, por favor, ignore el mensaje
                           """
                   )
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






@usuarios.route("/logout")
@login_required
@usuario_logic.user_roles_required("Usuario")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('main.home'))
