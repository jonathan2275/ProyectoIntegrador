from flask import Flask, render_template,request,redirect,url_for,send_file,session
import controlador
from conexion import baseDatos as bd
from prediccion import predic
import json
app = Flask(__name__)
app.secret_key ="1234"

###########################################################
@app.route('/')
def _():
  if(validator(session)):
    base = bd()
    produ = base.consulta("SELECT * FROM producto ORDER by stock_producto ASC LIMIT 5")
    v1 = [base.consulta("SELECT sum(total_factura) FROM factura")[0][0],base.consulta("SELECT sum(stock_producto) FROM producto")[0][0],base.consulta("SELECT COUNT(id_factura) FROM factura")[0][0]]
    base.cerrar()
    return render_template('index.html', nombre = session['nombre'],producto = produ,v = v1)
  else:
    return redirect(url_for('_login'))

@app.route('/login')
def _login(): 
  return render_template('login.html',message = request.values.get('msg'), alert = request.values.get('alert'))

@app.route('/producto')
def _producto(): 
    if(validator(session)):
      base = bd()
      producto = base.consulta("select * from producto")
      base.cerrar()
      return render_template('producto.html',producto = producto, nombre = session['nombre'],message = request.values.get('msg'), alert = request.values.get('alert'))
    else:
      return redirect(url_for('_login'))

@app.route('/facturacion')
def _facturacion():
  if(validator(session)):
    base = bd()
    factura = base.consulta("select * from factura")
    base.cerrar() 
    return render_template('facturacion.html',factura = factura, nombre = session['nombre'],message = request.values.get('msg'), alert = request.values.get('alert'))
  else:
      return redirect(url_for('_login'))

@app.route('/perfil')
def _p(): 
  if(validator(session)):
    base = bd()
    resp = base.consulta("select * from usuario where email = '{}'".format(session['email']))
    base.cerrar()
    return render_template('profile.html',nombre = session['nombre'], message=request.values.get('msg'),alert=request.values.get('alert'), infor = resp[0])
  else:
      return redirect(url_for('_login'))

@app.route('/registro')
def _R(): 
  return render_template('register.html')

@app.route('/logout')
def _lg(): 
  session.pop('email')
  return redirect(url_for('_login'))

#######################################################
def validator(session):
  if 'email' in session:
    return True
  else:
    return False

#######################################################
@app.route('/searchPhoto')
def _sP(): 
  return controlador.searchPhoto(request.values.get('word')),200,{'Content-Type': 'application/json'}

@app.route('/registrarse',methods=['GET','POST'])
def _rr():
  resp, msg = controlador.registrarse(request.form['name'],request.form['uname'],request.form['email'],request.form['password'])
  if resp:
    return redirect(url_for('_login')+'?msg='+msg+'&alert=alert-success')
  else:
    return render_template('register.html',message=msg)

@app.route('/iniciar',methods=['GET','POST'])
def _ic():
  resp, msg, vec = controlador.login(request.form['email'],request.form['password']) 
  if resp:
    session['nombre'] = vec[0] +" "+ vec[1]
    session['email'] = request.form['email']
    return redirect(url_for('_'))
  return redirect(url_for('_login')+'?msg='+msg+'&alert=alert-danger')
 
@app.route('/updateI',methods=['GET','POST'])
def _upI():
  resp, msg = controlador.updatePerson(request.form['edad'],request.form['email'],request.form['name'],request.form['uname'],request.form['direccion'],request.form['ciudad'],request.form['pais'],request.form['acerca'])
  return redirect(url_for('_p')+'?msg='+msg+'&alert=alert-success')

@app.route('/saveProduct')
def _sPro(): 
  return controlador.registrarProducto(request.values.get('nombrep'),request.values.get('preciop'),request.values.get('stockp'),request.values.get('estadop'),request.values.get('imgs')),200,{'Content-Type': 'application/json'}

@app.route('/detailsProduct')
def _dP(): 
  base = bd()
  details = base.consulta("select * from producto where id_producto = {}".format(request.values.get('id')))
  img = base.consulta("select * from producto_img where id_producto = {} limit 1".format(request.values.get('id')))
  base.cerrar()
  return json.dumps({'producto':details[0],'img':img}),200,{'Content-Type': 'application/json'}

@app.route('/updateProduct')
def _uP(): 
  return controlador.actualizarProducto(request.values.get('id'),request.values.get('nombrep'),request.values.get('preciop'),request.values.get('stockp'),request.values.get('estadop')),200,{'Content-Type': 'application/json'}

@app.route('/saveFactura')
def _sF(): 
  return controlador.registrarFactura(request.values.get('nombref'),request.values.get('cedulaf'),request.values.get('telefonof'),request.values.get('direccionf'),request.values.get('totalf'),request.values.get('estadof'),request.values.get('produ')),200,{'Content-Type': 'application/json'}

@app.route('/detailsFactura')
def _dF(): 
  base = bd()
  details = base.consulta("select * from factura where id_factura = {}".format(request.values.get('id')))
  produ = base.consulta("select * from detalle_factura,producto where detalle_factura.id_producto=producto.id_producto and detalle_factura.id_factura = {}".format(request.values.get('id')))
  base.cerrar()
  return json.dumps({'factura':details[0],'produ':produ}),200,{'Content-Type': 'application/json'}

@app.route('/PDFfactura')
def _pdfFactura():
  if request.method == 'GET':
    import reporte
    from io import BytesIO
    return send_file(BytesIO(reporte.export_to_pdf(request.values.get('id'))),
                 attachment_filename="Reporte-Prestamo.pdf",
                 mimetype='application/pdf',
                 as_attachment=True,
                 cache_timeout=-1)

@app.route('/MostSeller')
def _MS():
  base = bd()
  produ = base.consulta("SELECT SUM(detalle_factura.cantidad_detalle_factura) as sm,producto.nombre_producto from detalle_factura,producto WHERE detalle_factura.id_producto = producto.id_producto GROUP BY detalle_factura.id_producto ORDER BY sm DESC LIMIT 10")
  resp = []
  for i in produ:
    resp.append([int(i[0]),str(i[1])])
  base.cerrar()
  return json.dumps({'produ':resp}),200,{'Content-Type': 'application/json'}

#"""
@app.route('/predic')
def _pr():
  try:
    base = bd()
    details = base.consulta("select * from producto where id_producto = {}".format(predic().predict(request.values.get("foto"))))
    base.cerrar()
    return json.dumps({'producto':details[0]}),200,{'Content-Type': 'application/json'}
  except Exception as err:
    print(err)
    return json.dumps({'err':err}),200,{'Content-Type': 'application/json'}
#"""

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)   