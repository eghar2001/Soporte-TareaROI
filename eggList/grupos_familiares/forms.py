from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Email

from eggList.models import GrupoFamiliar, Usuario


class CrearGrupoFamiliarForm(FlaskForm):
    familia = StringField('Nombre del Grupo Familiar', validators=[DataRequired(), Length(min=3, max=50)])
    submit = SubmitField('Crear')

    def validate_familia(self, familia):
        grupo = GrupoFamiliar.query.filter(GrupoFamiliar.nombre_familia == familia.data).first()
        if grupo:
            raise ValidationError("Esa nombre ya existe")


class AgregarUsuarioForm(FlaskForm):
    email_usuario = StringField('Mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Agregar')

    def validar_email_usuario(self, email_usuario):
        user = Usuario.query.filter_by(email_usuario=email_usuario.data)
        if not user or not user.email_confirmed_at:
            raise ValidationError("Ese mail no pertenece a ningun usuario, intente de nuevo")
