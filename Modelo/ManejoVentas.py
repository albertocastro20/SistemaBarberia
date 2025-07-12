from Modelo.Conexion import *
from Modelo.Clases import Producto
from Modelo.Clases import Ticket
from Modelo.Clases import Servicio


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
