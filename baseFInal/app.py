from flask import Flask,request,jsonify,render_template,json
import os
import urllib.parse as up
import psycopg2

#import database

from connection import connect
app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('home.html',name = 'inicio')

@app.route('/asd')
def login():
    return render_template('home.html',prb = 'login')


@app.route('/cliente',methods = ['POST'])
def cliente():
    if request.method == 'POST':
        data = request.form['rut']
        data = "select * from clientes where clientes.rut_cliente ="+"'"+data+"';"
        cur = connect()
        cur.execute(data)
        res = cur.fetchall()
        if res:
            return render_template('home.html',data = res, name='cliente')
        else:
            return render_template('home.html',name='inicio')
    else:
        return "error"

@app.route('/vehiculos',methods = ['POST'])
def vehiculos():
    if request.method == 'POST':
        data = request.form['rut']
        data = "SELECT vehiculo.* from vehiculo, Clientes, Contrato WHERE CLIENTES.RUT_CLIENTE ="+"'"+data+"' AND CLIENTES.rut_CLIENTE = Contrato.rut AND Contrato.patente = Vehiculo.patente;"       
        print(data)
        cur = connect()
        cur.execute(data)
        res = cur.fetchall()
        if res:
            return render_template('home.html',data = res, name='vehiculos')
        else:
            return render_template('home.html',name='inicio')
    else:
        return "error"


@app.route('/pagosc',methods = ['POST'])
def pagos():
    if request.method == 'POST':
        data = request.form['rut']
        data = "SELECT Pagos.fecha_pago, Pagos.monto FROM Clientes, Contrato, Pagos WHERE Clientes.rut_cliente ="+"'"+data+"' AND Clientes.rut_cliente = Contrato.rut AND Contrato.codigo = Pagos.codigo_contrato order by pagos.fecha_pago desc;"       
        print(data)
        cur = connect()
        cur.execute(data)
        res = cur.fetchall()
        if res:
            return render_template('home.html',data = res, name='pagosc')
        else:
            return render_template('home.html',name='inicio')
    else:
        return "error"

@app.route('/morosos',methods = ['GET'])
def morosos():
    if request.method == 'GET':
        data = "SELECT * FROM Clientes WHERE Clientes.estado_cliente = 'MOROSO';"
        cur = connect()
        cur.execute(data)
        res = cur.fetchall()
        if res:
            return render_template('home.html',data = res, name='morosos')
        else:
            return render_template('home.html',name='inicio')
    else:
        return "error"

@app.route('/incidentes',methods = ['POST'])
def incidentes():
    if request.method == 'POST':
        data = request.form['rut']
        data2 = request.form['rut']
        data = "SELECT COUNT(Incidente.codigo_incidente) FROM Incidente, Vehiculo, Clientes, Contrato WHERE Clientes.rut_cliente ="+"'"+data+"' AND Clientes.rut_cliente = Contrato.rut AND Contrato.patente = Vehiculo.patente AND Vehiculo.numero_chasis = Incidente.numero_chasis;"
        cur = connect()
        cur.execute(data)
        res = cur.fetchall()
        data2 = "select incidente.codigo_incidente,incidente.fecha from incidente,vehiculo,contrato,clientes where incidente.numero_chasis = vehiculo.numero_chasis and vehiculo.patente = contrato.patente and contrato.rut = clientes.rut_cliente and clientes.rut_cliente ="+"'"+data2+"';"
        cur2 = connect()
        cur2.execute(data2)
        res2 = cur2.fetchall()
        print(res2)
        if res:
            return render_template('home.html',data = res, name='incidentes',data2 = res2)
        else:
            return render_template('home.html',name='inicio')
    else:
        return "error"        

@app.route('/antecedentes',methods = ['POST'])
def antecedentes():
    if request.method == 'POST':
        data = request.form['rut']
        data = "SELECT Tipo_Ante.codigo, Tipo_Ante.descripcion FROM Tipo_Ante, Clientes, Antecedentes WHERE Clientes.rut_cliente ="+"'"+data+"' AND Clientes.rut_cliente = Antecedentes.rut AND Antecedentes.codigo_tipo = Tipo_Ante.codigo;"       
        print(data)
        cur = connect()
        cur.execute(data)
        res = cur.fetchall()
        if res:
            return render_template('home.html',data = res, name='antecedentes')
        else:
            return render_template('home.html',name='planerror')
    else:
        return "error"    

@app.route('/planes',methods = ['GET'])
def planes():
    if request.method == 'GET':
        data = "SELECT * FROM Plan;"       
        cur = connect()
        cur.execute(data)
        res = cur.fetchall()
        if res:
            return render_template('home.html',data = res, name='planes')
        else:
            return render_template('home.html',name='inicio')
    else:
        return "error"    

@app.route('/periodo',methods = ['POST'])
def periodo():
    if request.method == 'POST':
        fi = request.form['fi']
        ff = request.form['ff']
        print(fi,ff)
        data = "SELECT t.x-j.y as Final FROM (SELECT SUM(Pagos.monto) as x FROM Pagos WHERE (Pagos.fecha_pago BETWEEN "+"'"+fi+"' AND '"+ff+"'))t,(SELECT SUM(Incidente.costo_cobertura) as y FROM Incidente WHERE (Incidente.fecha BETWEEN "+"'"+fi+"' AND '"+ff+"'))j ;"      
        cur = connect()
        cur.execute(data)
        res = cur.fetchall()
        print(res)
        if res:
            return render_template('home.html',data = res, name='periodo',fi = fi, ff = ff)
        else:
            return render_template('home.html',name='inicio')
    else:
        return "error"    
@app.route('/periodorut',methods = ['POST'])
def periodorut():
    if request.method == 'POST':
        data = request.form['rut']
        data = "SELECT t.x - j.y as Final FROM (SELECT SUM(Pagos.monto) as x FROM Pagos, Clientes, Contrato WHERE Clientes.rut_cliente ="+"'"+data+"' AND Clientes.rut_cliente = Contrato.rut AND Contrato.codigo = Pagos.codigo_contrato)t ,(SELECT SUM(Incidente.costo_cobertura) as y FROM Clientes, Vehiculo, Incidente, Contrato WHERE Clientes.rut_cliente ="+"'"+data+"' AND Clientes.rut_cliente = Contrato.rut AND Contrato.patente = Vehiculo.patente AND Vehiculo.numero_chasis = Incidente.numero_chasis)j;"
        cur = connect()
        cur.execute(data)
        res = cur.fetchall()

        if res:
            return render_template('home.html',data = res, name='periodorut')
        else:
            return render_template('home.html',name='inicio')
    else:
        return "error"  


@app.route('/taller',methods = ['GET'])
def taller():
    if request.method == 'GET':
        data = "SELECT * FROM Taller WHERE Taller.cantidad_vehiculos = (SELECT MAX(Taller.cantidad_vehiculos) FROM Taller);"
        cur = connect()
        cur.execute(data)
        res = cur.fetchall()
        data2 = "SELECT * FROM Taller WHERE Taller.cantidad_vehiculos = (SELECT MIN(Taller.cantidad_vehiculos) FROM Taller);"
        cur2 = connect()
        cur2.execute(data2)
        res2 = cur2.fetchall()
        print(res)
        if res:
            return render_template('home.html',data = res,data2 = res2, name='taller')
        else:
            return render_template('home.html',name='inicio')
    else:
        return "error"            


@app.route('/ingresarc',methods=['GET','POST'])
def ingresarc():
    if request.method == 'GET':
        return render_template('home.html', name='ingresarc')
    else:
        return render_template('home.html',name='inicio')    


@app.route('/modificar',methods=['GET','POST'])
def modificar():
    if request.method == 'GET':
        return render_template('home.html', name='modificar')
    else:
        return render_template('home.html',name='inicio')         

           
@app.route('/clientes',methods = ['GET'])
def clientes():
    if request.method == 'GET':
        data = "SELECT * FROM clientes;"
        cur = connect()
        cur.execute(data)
        res = cur.fetchall()
        print(res)
        if res:
            return render_template('home.html',data = res, name='clientes')
        else:
            return render_template('home.html',name='inicio')
    else:
        return "error"            
    
@app.route('/incidentesc',methods = ['GET'])
def incidentesc():
    if request.method == 'GET':
        data = "SELECT distinct clientes.rut_cliente, clientes.nombre_cliente,t.cant FROM clientes, contrato, vehiculo, incidente, (SELECT COUNT(incidente.codigo_incidente) as cant, incidente.numero_chasis as nuchas FROM incidente GROUP BY incidente.numero_chasis)t WHERE clientes.rut_cliente = contrato.rut AND contrato.patente = vehiculo.patente AND vehiculo.numero_chasis = incidente.numero_chasis AND incidente.numero_chasis = t.nuchas AND t.cant = (SELECT MAX(cant) FROM (SELECT COUNT(incidente.codigo_incidente) as cant, incidente.numero_chasis as nuchas FROM incidente GROUP BY incidente.numero_chasis)t);"
        cur = connect()
        cur.execute(data)
        res = cur.fetchall()

        print(res)
        if res:
            return render_template('home.html',data = res, name='incidentesc')
        else:
            return render_template('home.html',name='inicio')
    else:
        return "error"  
 