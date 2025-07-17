from Modelo.Conexion import *
from Modelo.Clases import Producto
from Modelo.Clases import Ticket
from Modelo.Clases import Servicio

import datetime


class QuerysVentas():
    def __init__(self, conexion):
        self.conexion = conexion

    def consultaServicios(self):
        qConsultaServicios = "SELECT idServicio, nombre, precio FROM catalogo_servicios"

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qConsultaServicios)
                tuplaServicios = cursor.fetchall()
            except Error as e:
                print(e)
        
        return tuplaServicios


    def consultaProductos(self):
        qConsultaServicios =  "SELECT idProducto, nombre, precio FROM Producto"

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qConsultaServicios)
                tuplaProductos = cursor.fetchall()
            except Error as e:
                print(e)

        return tuplaProductos
    
    def iniciarVenta(self, idCliente):
        fecha = datetime.datetime.now()
        cadenaFecha = fecha.strftime('%Y-%m-%d %H:%M')
        
        qIniciarVenta = """INSERT INTO Ticket (fecha_hora_venta, idCliente) values (%s, %s)"""
        tuplaVenta = (cadenaFecha, int(idCliente))

        cone = self.conexion.conectar()
        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qIniciarVenta, tuplaVenta)
                cone.commit()
            except Error as e:
                print(e)
        #print(tuplaVenta)


    def obtenerIdTicket(self):
        qObtenerId = """SELECT MAX(idTicket) from Ticket"""
        
        cone = self.conexion.conectar()
        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qObtenerId)
                id = cursor.fetchall()
            except Error as e:
                print(e)

        print(id)

        for i in id:
            idTicket = i[0]

        return idTicket
    
    def insertarDetalleProducto(self, detalleProducto):
        qInsertarDProducto = """INSERT INTO detalle_venta_producto (cantidad, precio_unitario, subtotal, idticket, idProducto)
        VALUES (%s, %s, %s, %s, %s)"""

        cone = self.conexion.conectar()
        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qInsertarDProducto, detalleProducto)
                cone.commit()
                print("Producto Insertado")
            except Error as e:
                print(e)

    def obtenerBarberos(self):
        qBarberos = """SELECT B.idBarbero, E.nombre as nombreBarbero, E.apellido_paterno as apellidoBarbero
        FROM Barbero AS B
        INNER JOIN Empleado AS E
        ON B.idEmpleado = E.idEmpleado"""

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qBarberos)
                tuplaBarberos = cursor.fetchall()
            except Error as e:
                print(e)

        return tuplaBarberos
    
    def insertarServicioRealizado(self, servicioRealizado):
        
        qInsertarServicio = """INSERT INTO servicio_realizado (fecha_hora_final, idticket, idServicio, idBarbero)
        VALUES (%s, %s, %s, %s)"""

        cone = self.conexion.conectar()
        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qInsertarServicio, servicioRealizado)
                cone.commit()
                print("Producto Insertado")
            except Error as e:
                print(e)

    def actualizarVenta(self, datosFaltantes):
        qActualizarVenta = """UPDATE ticket 
        SET total_venta = %s, metodo_pago = %s, descuento = %s, subtotal = %s 
        WHERE idTicket = %s"""

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qActualizarVenta, datosFaltantes)
                cone.commit()
                print("Actualización realizada")
                
            
            except Error as e:
                print(f"Error: {e}")




