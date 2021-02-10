import itertools
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import  cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from conexion import baseDatos as bd

def export_to_pdf(id):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    #Consulta BD
    base = bd()
    dF = base.consulta("select * from factura where id_factura = {}".format(id))
    detalle_factura = base.consulta("select * from detalle_factura,producto where producto.id_producto = detalle_factura.id_producto and  detalle_factura.id_factura = {}".format(id))
    base.cerrar()

    #Header
    c.setFont('Helvetica-Bold',20)
    c.drawCentredString(320,780,'Papeleria Rosita')
    c.setFont('Helvetica-Bold',15)
    c.drawCentredString(320,750,'Factura #{}'.format(str(dF[0][0]),))

    #Datos
    c.setFont('Helvetica-Bold',12)
    c.drawString(50,710,'Cedula: ')
    c.setFont('Helvetica-Bold',12)
    c.drawString(400,710,'Nombre: ') 
    c.setFont('Helvetica-Bold',12)
    c.drawString(50,680,'Teléfono: ')
    c.setFont('Helvetica-Bold',12)
    c.drawString(400,680,'Dirección: ') 

    c.setFont('Helvetica',12)
    c.drawString(110,710,dF[0][1])
    c.setFont('Helvetica',12)
    c.drawString(485,710,dF[0][2])
    c.setFont('Helvetica',12)
    c.drawString(110,680,dF[0][3])
    c.setFont('Helvetica',12)
    c.drawString(485,680,dF[0][4])


    #Tabla
    styles = getSampleStyleSheet()
    styleBH = styles['Normal']
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    

    #titulo tabla
    id_producto = Paragraph('<b>ID</b>',styleBH)
    nombre = Paragraph('<b>Nombre</b>',styleBH)
    precio = Paragraph('<b>Precio</b>',styleBH)
    cantidad = Paragraph('<b>Cantidad</b>',styleBH)
    precio_total = Paragraph('<b>Precio Total</b>',styleBH)

    #estructura tabla
    tabla_datos = []
    tabla_datos.append([id_producto,nombre,precio,cantidad,precio_total])

   
    #Body Tabla
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    high = 600
    
    for datos in detalle_factura:
        dp = [datos[1],datos[5],datos[6],datos[3],(datos[6]*datos[3])]
        tabla_datos.append(dp)
        high = high - 18
    tabla_datos.append(['-','-','-','Total',dF[0][5]])

    width, height = A4
    tabla = Table(tabla_datos,colWidths=[1.8 * cm ,5.4 * cm,2.6 * cm,2.6 * cm,2.6 * cm])
    tabla.setStyle(TableStyle([
        ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
        ('BOX',(0,0),(-1,-1),0.25,colors.black),
        ('BACKGROUND',(0,0),(4,0),colors.azure)
    ]))

    tabla.wrapOn(c,height,width)
    tabla.drawOn(c,80,high)
    c.showPage() 



    c.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf
