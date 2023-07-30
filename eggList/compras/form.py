import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired


class CompraBusquedaForm(FlaskForm):
    fecha_desde = DateField("Fecha Desde", format='%Y-%m-%d')
    fecha_hasta = DateField("Fecha Hasta", format='%Y-%m-%d')
    supermercado = SelectField("Supermercado")
    submit = SubmitField("Buscar")

    def validate_fecha_desde(self,fecha_desde):
        if datetime.datetime.strptime(fecha_desde.data,"%Y-%m-%d"):
            raise ValidationError("No ingresó una Fecha desde valida")

    def validate_fecha_hasta(self, fecha_hasta):
        if datetime.datetime.strptime(fecha_hasta.data,"%Y-%m-%d") < datetime.datetime.strptime(self.fecha_hasta.data,"%Y-%m-%d"):
            raise ValidationError("No ingresó una Fecha hasta valida")

