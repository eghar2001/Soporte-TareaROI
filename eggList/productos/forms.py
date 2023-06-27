import decimal

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange


class AgregarProductoForm(FlaskForm):
    descripcion = StringField('Producto', validators = [DataRequired()])
    cantidad = IntegerField('Cantidad', validators= [ NumberRange(min = 1)])
    submit = SubmitField('Agregar')

class ModificarProductoForm(FlaskForm):
    descripcion = StringField('Producto', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[NumberRange(min=1)])
    precio = DecimalField('Precio', places=2, rounding=decimal.ROUND_UP)
    submit = SubmitField('Modificar')


class CarritoForm(FlaskForm):
    precio = DecimalField('Precio',places = 2, rounding=decimal.ROUND_UP )
    submit = SubmitField("En carrito🛒")