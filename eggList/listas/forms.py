from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length

class CrearListaForm(FlaskForm):
    descripcion = StringField('Descripcion', validators = [DataRequired(),Length(min = 3, max = 100)])
    incluye_grupo_familiar = BooleanField('Incluye grupo familiar')
    submit = SubmitField('Crear Lista')




