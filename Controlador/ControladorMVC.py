#from ..Modelo.Conexion import *
from Vista.VentanaPrincipal import BarberiaPrincipal
import tkinter as tk
from Modelo.ManejoClientes import *
from Modelo.Conexion import *
from Modelo.ManejoCitas import *
from Modelo.Clases import *

class Controlador:
    def __init__(self, parent):
        self.parent = parent
        self.vista =  BarberiaPrincipal(parent = self.parent, controlador_recibido= self)
        self.conexion = Conexion("root", "Cris8426")
        self.manejoClientes = QuerysCliente(self.conexion)
        self.manejoCitas = QuerysCita(self.conexion)
        
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
        

if __name__ == "__main__":
    root = tk.Tk()
    control = Controlador(root)

    root.resizable(False, False)
    root.mainloop()
    
    