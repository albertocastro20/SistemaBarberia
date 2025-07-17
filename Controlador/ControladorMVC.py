#from ..Modelo.Conexion import *
from Vista.VentanaPrincipal import BarberiaPrincipal
import tkinter as tk
from Modelo.Conexion import *
from Modelo.ManejoClientes import *
from Modelo.ManejoCitas import *
from Modelo.Clases import *
from Modelo.ManejoVentas import QuerysVentas

class Controlador:
    def __init__(self, parent):
        self.parent = parent
        self.vista =  BarberiaPrincipal(parent = self.parent, controlador_recibido= self) #Se pasa root y asi mismo como controlador
        self.conexion = Conexion("root", "Cris8426")
        self.manejoClientes = QuerysCliente(self.conexion)
        self.manejoVentas = QuerysVentas(self.conexion) 
        self.manejoCitas = QuerysCita(self.conexion)
        
# --------------------------- Querys Cliente -----------------------------------
    def insercionCliente(self, cliente):
        self.manejoClientes.insertarClientes(cliente)

    def actualizarCliente(self, cliente):
        self.manejoClientes.actualizarCliente(cliente)

    def consultarCliente(self, cliente):
        tuplaSola = self.manejoClientes.consultarCliente(cliente)
        return tuplaSola

    def consultaGeneralCliente(self):
        tuplita = self.manejoClientes.consultaGeneral()
        return tuplita
    
# --------------------------- Querys Cita -----------------------------------
    
    def insercionCita(self, cita):
        self.manejoCitas.insertarCita(cita)

    def actualizarCita(self, cita):
        self.manejoCitas.actualizarCita(cita)

    def mostrarCitas(self, cita):
        tuplaCitas = self.manejoCitas.mostrarCitas(cita)
        return tuplaCitas
    
    def buscarCita(self, cita):
        citaRecibida = self.manejoCitas.consultarCita(cita)
        return citaRecibida
    
# --------------------------- Querys Venta -----------------------------------
    
    def consultaProductos(self):
        #tuplaServicios = self.manejoVentas.consultaServicios()
        tuplaProductos = self.manejoVentas.consultaProductos()

        return tuplaProductos
    
    def iniciarVenta(self, idCliente):
        self.manejoVentas.iniciarVenta(idCliente)
        idTicket = self.manejoVentas.obtenerIdTicket()

        return idTicket
    
    def insertarDProducto(self, detalleProducto):
        self.manejoVentas.insertarDetalleProducto(detalleProducto)

    def obtenerBarberos(self):
        tuplaBarberos = self.manejoVentas.obtenerBarberos()

        return tuplaBarberos
    
    def consultaServiciosVenta(self):
        #tuplaServicios = self.manejoVentas.consultaServicios()
        tuplaServicios = self.manejoVentas.consultaServicios()

        return tuplaServicios
    
    def insertarServicioRealizado(self, servicioRealizado):
        self.manejoVentas.insertarServicioRealizado(servicioRealizado)

    def finalizarVenta(self, datosFaltantes):
        self.manejoVentas.actualizarVenta(datosFaltantes)
        

if __name__ == "__main__":
    root = tk.Tk()
    control = Controlador(root)

    root.resizable(False, False)
    root.mainloop()
    
    