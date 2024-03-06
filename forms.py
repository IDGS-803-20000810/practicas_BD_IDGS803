from wtforms import Form
from wtforms import (
    StringField,
    SelectField,
    RadioField,
    EmailField,
    IntegerField,
    DecimalField,
    BooleanField
)


class EmpleadoForm(Form):
    id = IntegerField("id")
    nombre = StringField("nombre")
    correo = EmailField("correo")
    telefono = StringField("telefono")
    direccion = StringField("direccion")
    sueldo = DecimalField("sueldo")


class OrdenPizzaForm(Form):
    nombre = StringField("nombre")
    direccion = StringField("direccion")
    telefono = StringField("telefono")


class DetalleOrdenForm(Form):
    tamanos = [
        (40, "Chica $40"),
        (80, "Mediana $80"),
        (120, "Grande $120"),
    ]
    
    tamano = RadioField("Tamaño Pizza",choices=tamanos)
    numPizzas = IntegerField("Num. de Pizzas")

    jamon = BooleanField("Jamon $10")
    pina = BooleanField("Piña $10")
    champ = BooleanField("Champiñones $10")
