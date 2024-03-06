from flask import Flask, request, render_template, Response, g, redirect, session
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms

from models import db
from models import Empleados, DetalleOrden, Orden

app = Flask(__name__)
app.secret_key = "esta es la clave secreta"
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/index", methods=["GET", "POST"])
def index():
    form = forms.EmpleadoForm(request.form)
    
    if request.method == "POST":
        emp = Empleados(nombre=form.nombre.data,
                        correo=form.correo.data,
                        telefono=form.telefono.data,
                        direccion=form.direccion.data,
                        sueldo=float(form.sueldo.data))
        db.session.add(emp)
        db.session.commit()
        
    return render_template("index.html",form=form)

@app.route("/eliminar",methods=["GET", "POST"])
def eliminar():
    form = forms.EmpleadoForm(request.form)
    if request.method == "GET":
        id=request.args.get('id')
        emp=db.session.query(Empleados).filter(Empleados.id==id).first()
        form.id.data=request.args.get('id')
        form.nombre.data=emp.nombre
        form.correo.data=emp.correo
        form.telefono.data=emp.telefono
        form.direccion.data=emp.direccion
        form.sueldo.data=emp.sueldo
    if request.method == "POST" :
        id=form.id.data
        emp=Empleados.query.get(id)
        db.session.delete(emp)
        db.session.commit()
        return redirect('tabla_empleados')
    
    return render_template('eliminar.html',form=form)

@app.route("/modificar",methods=["GET", "POST"])
def modificar():
    form = forms.EmpleadoForm(request.form)
    
    if request.method == "GET":
        id=request.args.get('id')
        emp=db.session.query(Empleados).filter(Empleados.id==id).first()
        form.id.data=request.args.get('id')
        form.nombre.data=emp.nombre
        form.correo.data=emp.correo
        form.telefono.data=emp.telefono
        form.direccion.data=emp.direccion
        form.sueldo.data=emp.sueldo
    if request.method == "POST" :
        id=form.id.data
        emp=db.session.query(Empleados).filter(Empleados.id==id).first()
        emp.nombre=form.nombre.data
        emp.correo=form.correo.data
        emp.telefono=form.telefono.data
        emp.direccion=form.direccion.data
        emp.sueldo=form.sueldo.data
        db.session.add(emp)
        db.session.commit()
        return redirect('tabla_empleados')
    
    return render_template('modificar.html',form=form)


@app.route("/tabla_empleados", methods=["GET", "POST"])
def ABC_Completo():
    form=forms.EmpleadoForm(request.form)
    empleados=Empleados.query.all()
    return render_template('tabla_empleados.html',empleados=empleados)

@app.route("/pizzas", methods=["GET", "POST"])
def pizzas():
    detalleForm = forms.DetalleOrdenForm(request.form)
    ordenForm = forms.OrdenPizzaForm(request.form)
    
    if request.method == "GET":
        session['detalle'] = [];
        ventasDia = Orden.query.all()
        totalVentasDia=0.0
        for venta in ventasDia:
            totalVentasDia += venta.total
            
        return render_template("pizzas.html",ordenForm=ordenForm, detalleForm=detalleForm, detalle =  session['detalle'], ventasDia = ventasDia,totalVentasDia=totalVentasDia)

    
    if request.method == "POST":
        total = 0
        
        for orden in session['detalle']:
            total += orden['subtotal']
        
        orden = Orden(nombre=ordenForm.nombre.data,
                        direccion=ordenForm.direccion.data,
                        telefono=ordenForm.telefono.data,
                        total=total)
        db.session.add(orden)
        db.session.commit()
        
        ventasDia = Orden.query.all()
        
        totalVentasDia = 0.0
        for venta in ventasDia:
            totalVentasDia +=  venta.total
            

        return render_template("pizzas.html",ordenForm=ordenForm, detalleForm=detalleForm, detalle = session['detalle'], ventasDia = ventasDia, totalVentasDia=totalVentasDia)

@app.route("/quitar-detalle", methods=["POST"])
def quitar():
    detalleForm = forms.DetalleOrdenForm(request.form)
    ordenForm = forms.OrdenPizzaForm(request.form)
    
    if request.method == "POST":
        session['detalle'].pop()
        ventasDia = Orden.query.all()
        totalVentasDia=0.0
        for venta in ventasDia:
            totalVentasDia += venta.total
        return render_template("pizzas.html",ordenForm=ordenForm, detalleForm=detalleForm, detalle =  session['detalle'], ventasDia = ventasDia,totalVentasDia=totalVentasDia)

@app.route("/add-detalle-pizza", methods=["POST"])
def addDetalle():
    
    
    detalleForm = forms.DetalleOrdenForm(request.form)
    ordenForm = forms.OrdenPizzaForm(request.form)
    
    tamano = detalleForm.tamano.data
    numPizzas = int(detalleForm.numPizzas.data)
    
    jamon = detalleForm.jamon.data
    pina = detalleForm.pina.data
    champ = detalleForm.champ.data
    
    subtotal = float(tamano);
    subtotal += 10 if jamon else 0
    subtotal += 10 if pina else 0
    subtotal += 10 if champ else 0
    
    subtotal = subtotal*numPizzas
    
    stringTamano = ""
    
    match (int(tamano)):
        case (40):
            stringTamano = "Chica"
        case (80):
            stringTamano = "Mediana"
        case (120):
            stringTamano = "Grande"
            
    stringIng = ""
    
    stringIng += "jamon," if jamon else ""
    stringIng += "piña," if pina else ""
    stringIng += "champiñones" if champ else ""
    
    # detalle = DetalleOrden(tamano=stringTamano,
    #                 num_pizzas=numPizzas,
    #                 ingredientes = stringIng,
    #                 subtotal = subtotal
    #                 )
    
    listDetalle = session['detalle']
    
    listDetalle.append({
                    'no':len(listDetalle)+1,
                    'tamano':stringTamano,
                    'num_pizzas':numPizzas,
                    'ingredientes': stringIng,
                    'subtotal':subtotal})
    
    session['detalle'] = listDetalle
    
    ventasDia = Orden.query.all()
    totalVentasDia=0.0
    for venta in ventasDia:
            totalVentasDia +=  venta.total
            
    return render_template("pizzas.html",ordenForm=ordenForm, detalleForm=detalleForm, detalle = session['detalle'], ventasDia = ventasDia,totalVentasDia=totalVentasDia)

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
