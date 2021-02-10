import json
import requests
from conexion import baseDatos as bd
subscriptionKey = "e3b3133adec845c2bd9d498c60110175"
customConfigId = "8ebea03e-1825-4f23-ae14-0d8a83636ac5"

def searchPhoto(searchTerm):
    resp = []    
    url = 'https://api.bing.microsoft.com/v7.0/custom/images/search?' + 'q=' + searchTerm + '&' + 'customconfig=' + customConfigId + "&count=15"
    r = requests.get(url, headers={'Ocp-Apim-Subscription-Key': subscriptionKey}).json()
    r = r['value']
    for h in r:
        resp.append(h['contentUrl'])
    return json.dumps(resp)

def registrarse(name,uname,email,password):
    base = bd()
    em = base.consulta("select * from usuario where email = '{}'".format(email))
    if em:
        return False,"Ya se encuentra Registrado"
    else:
        base.insertar("insert into usuario(nombre,apellido,email,password) values('{}','{}','{}','{}')".format(name,uname,email,password))
        return True,"Registrado con exito"
    return False

def login(email,password):
    base = bd()
    resp = base.consulta("select * from usuario where email = '{}' and password = '{}'".format(email,password))
    base.cerrar()
    if resp:
        return True,"Inicio Session Exitoso",[resp[0][3],resp[0][4]]
    else:
        return False,"Credenciales Incorrectas",[]

def updatePerson(edad,email,name,uname,direccion,ciudad,pais,acerca):
    base = bd()
    base.insertar("update usuario set edad='{}', nombre = '{}', apellido = '{}', direccion='{}', ciudad='{}', pais='{}',acercaMi='{}' where email = '{}'".format(edad,name,uname,direccion,ciudad,pais,acerca,email))
    base.cerrar()
    return True, "Actualizado Exitosamente"

def registrarProducto(nombrep,preciop,stockp,estadop,imgs):
    base = bd()
    base.insertar("insert into producto(nombre_producto,precio_producto,stock_producto,estado_producto) values('{}',{},{},'{}')".format(nombrep,preciop,stockp,estadop))
    id = base.consulta('select max(id_producto) from producto')
    for x,i in enumerate(imgs.split(',')):
        base.insertar("insert into producto_img (id_producto,nombre_img_producto,img_producto) values({},'{}','{}')".format(id[0][0],nombrep+str(x),i))
    base.cerrar()
    return json.dumps({'ok':200})

def actualizarProducto(idp,nombrep,preciop,stockp,estadop):
    base = bd()
    base.insertar("update producto set nombre_producto = '{}', precio_producto = {}, stock_producto={},estado_producto = '{}' where id_producto = {}".format(nombrep,preciop,stockp,estadop,idp))
    base.cerrar()
    return json.dumps({'ok':200})

def registrarFactura(nombref,cedulaf,telefonof,direccionf,totalf,estadof,produ):
    base = bd()
    base.insertar("insert into factura(nombre_factura,cedula_factura,telefono_factura,direccion_factura,total_factura,estado_factura) values('{}','{}','{}','{}',{},'{}')".format(nombref,cedulaf,telefonof,direccionf,totalf,estadof))
    id = base.consulta('select max(id_factura) from factura')
    for x,i in enumerate(json.loads(produ)):
        base.insertar("insert into detalle_factura (id_producto,id_factura,cantidad_detalle_factura) values({},'{}','{}')".format(i[0],id[0][0],i[3]))
    base.cerrar()
    return json.dumps({'ok':200})

