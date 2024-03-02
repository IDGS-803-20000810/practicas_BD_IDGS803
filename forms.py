from wtforms import Form
from wtforms import StringField, SelectField, RadioField, EmailField, IntegerField, DecimalField

class EmpleadoForm(Form):
    id = IntegerField('id')
    nombre = StringField('nombre')
    correo = EmailField('correo')
    telefono = StringField('telefono')
    direccion = StringField('direccion')
    sueldo = DecimalField('sueldo')
