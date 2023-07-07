from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, RadioField
from wtforms.validators import Email, DataRequired, Length, ValidationError, EqualTo

from eggList.models import Usuario


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators = [DataRequired()])
    remember = BooleanField('Mantener sesion iniciada')
    submit = SubmitField('Ingresar')


class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min = 3, max = 50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    rol_en_compra = RadioField('Rol en las listas', choices = ["Armador", "Comprador"], validators=[DataRequired()])
    password = PasswordField('Contraseña', validators = [DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators = [DataRequired(), EqualTo('password', message="Las contraseñas deben coincidir")])
    submit = SubmitField('Registrarse')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email = email.data).first()
        if user and user.email_confirmed_at:
            raise ValidationError('Ese correo ya está registrado, por favor elija otro')