from flask_sqlalchemy import SQLAlchemy

import datetime

db=SQLAlchemy()

class Empleados(db.Model):
    __tablename__='empleados'
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(100))
    correo=db.Column(db.String(100))
    telefono=db.Column(db.String(25))
    direccion=db.Column(db.String(50))
    sueldo=db.Column(db.Float)
    create_date=db.Column(db.DateTime,default=datetime.datetime.now)
    
class Orden(db.Model):
    __tablename__='orden'
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(100))
    direccion=db.Column(db.String(100))
    telefono=db.Column(db.String(100))
    total=db.Column(db.Float)
    fecha_orden=db.Column(db.String(100),default="{}-{}-{}".format(str(datetime.datetime.now().day),str(datetime.datetime.now().month),str(datetime.datetime.now().year)))
    create_date=db.Column(db.DateTime,default=datetime.datetime.now)
    
class DetalleOrden(db.Model):
    __tablename__='detalle_orden'
    id=db.Column(db.Integer,primary_key=True)
    tamano=db.Column(db.String(100))
    num_pizzas=db.Column(db.String(10))
    ingredientes=db.Column(db.String(255))
    subtotal=db.Column(db.Float)
    create_date=db.Column(db.DateTime,default=datetime.datetime.now)
