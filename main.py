from flask import Flask, request, render_template, Response, g, redirect
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms

from models import db
from models import Empleados

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

@app.route("/tabla_empleados", methods=["GET", "POST"])
def ABC_Completo():
    form=forms.EmpleadoForm(request.form)
    empleados=Empleados.query.all()
    return render_template('tabla_empleados.html',empleados=empleados)

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
