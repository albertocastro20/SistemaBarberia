#Librerias de Diseño
import tkinter as tk #Libreria básica
from tkinter import * 
from tkinter import ttk #Libreria con nuevow wg
from tkcalendar import Calendar #Calendario

class ServiciosFrame(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.iniciarFrames()
        self.iniciarWidgets()

    def iniciarFrames(self):
        self.framePrincipal = Frame(self, width=650, height=460, bg="black")
        self.framePrincipal.grid(row=0, column=0)
        self.framePrincipal.grid_propagate(False)

        self.frameArribaC = Frame(self.framePrincipal, width=640, height=270, bg="white")
        self.frameArribaC.grid(row=0, column=0, padx=5, pady=5)
        self.frameArribaC.grid_propagate(False)

        self.frameAbajoC = Frame(self.framePrincipal, width=640, height=170, bg="white")
        self.frameAbajoC.grid(row=1, column=0, padx=5, pady=5)
        self.frameAbajoC.grid_propagate(False)

    def iniciarWidgets(self):
        etiquetaTitulo = Label(self.frameArribaC, text="Catálogo de Servicios", font=("Arial", 13))
        etiquetaTitulo.grid(row=0, column=0)
        #Creación de la tabla
        columnasTabla = ("nombre", "costo", "duracion", "estatus", "descripcion") #Tupla con los nombres de las columnas, la primera es con #0
        self.tablaServicios = ttk.Treeview(self.frameArribaC, columns= columnasTabla, height=20) #Constructor de la tabla
        self.tablaServicios.grid(row=1, column=0, padx=10, pady=5)

        #se le asigna el ancho a cada columna
        self.tablaServicios.column("#0", width=60)
        for col in columnasTabla:
            self.tablaServicios.column(col, width=95)
            if (col == "descripcion"):
                self.tablaServicios.column(col, width=180)

        #Se le asigna nombre a las columnas
        self.tablaServicios.heading("#0", text="ID")
        self.tablaServicios.heading("nombre", text="Nombre")
        self.tablaServicios.heading("descripcion", text="Descripcion")
        self.tablaServicios.heading("costo", text="Costo")
        self.tablaServicios.heading("duracion", text="Duración")
        self.tablaServicios.heading("estatus", text="Estatus")


        #Etiquetas del segundo frame
        etiquetaTituloBarberos = Label(self.frameAbajoC, text="Registro de Servicios", font=("Arial", 12))
        etiquetaTituloBarberos.grid(row=0, column=0)


        #Etiquetas para entrys
        etiquetaNombre = Label(self.frameAbajoC, text="Nombre: ")
        etiquetaNombre.grid(row=1, column=0, sticky="w", pady=4)
        self.campoNombre = Entry(self.frameAbajoC)
        self.campoNombre.grid(row=1, column=1, padx=5)

        etiquetaDescripcion = Label(self.frameAbajoC, text="Descripción: ")
        etiquetaDescripcion.grid(row=1, column=2, sticky="w", pady=4)
        self.campoDescripcion = Entry(self.frameAbajoC)
        self.campoDescripcion.grid(row=1, column=3, padx=5)

        etiquetaCosto = Label(self.frameAbajoC, text="Costo: ")
        etiquetaCosto.grid(row=3, column=0, sticky="w", pady=4)
        self.campoCosto = Entry(self.frameAbajoC)
        self.campoCosto.grid(row=3, column=1, padx=5)

        etiquetaDuracion = Label(self.frameAbajoC, text="Duración: ")
        etiquetaDuracion.grid(row=4, column=0, sticky="w", pady=4)
        self.campoDuracion = Entry(self.frameAbajoC)
        self.campoDuracion.grid(row=4, column=1, padx=5)

        etiquetaId = Label(self.frameAbajoC, text="Id: ")
        etiquetaId.grid(row=5, column=0, sticky="w", pady=4)
        self.campoId = Entry(self.frameAbajoC)
        self.campoId.grid(row=5, column=1, padx=5)

        etiquetaEstatus = Label(self.frameAbajoC, text="Estatus: ")
        etiquetaEstatus.grid(row=2, column=0, sticky="w", pady=4)
        self.campoEstatus = Entry(self.frameAbajoC)
        self.campoEstatus.grid(row=2, column=1, padx=5)

        self.botonRegistrar = Button(self.frameAbajoC, text="Registrar Servicio")
        self.botonRegistrar.grid(row=4, column=4, sticky="e", padx=10)

        self.botonActualizar = Button(self.frameAbajoC, text="Actualizar Servicio")
        self.botonActualizar.grid(row=5, column=4, sticky="e", padx=10)

        self.botonEliminar =  Button(self.frameAbajoC, text="Eliminar Servicio")
        self.botonEliminar.grid(row=3, column=4, sticky="e", padx=10)

        self.frameAbajoC.grid_columnconfigure(4, weight=1)
