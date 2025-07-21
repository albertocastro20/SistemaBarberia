import tkinter as tk #Libreria básica
from tkinter import * 
from tkinter import ttk #Libreria con nuevow wg
from tkcalendar import Calendar #Calendario
from tkinter import *

#Frame de los barberos

class BarberosFrame(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent, bg = "#2C2525")
        self.controlador = controlador
        self.iniciarFrames()
        self.iniciarWidgets()
        
    def iniciarFrames(self):

        self.frameArribaC = Frame(self, width=640, height=270, bg="#333333", # Fondo blanco para la tabla
                                  relief="flat", bd=0, highlightbackground="#E0E0E0", highlightthickness=1)
        self.frameArribaC.grid(row=0, column=0, padx=5, pady=5)
        self.frameArribaC.grid_propagate(False)

        self.frameAbajoC = Frame(self, width=640, height=170, bg="#333333", # Fondo blanco para la tabla
                                  relief="flat", bd=0, highlightbackground="#E0E0E0", highlightthickness=1)
        self.frameAbajoC.grid(row=1, column=0, padx=5, pady=5)
        self.frameAbajoC.grid_propagate(False)

    def iniciarWidgets(self):
        # Estilo para Labels y Entrys
        label_style = {"bg": "#333333", "fg": "#E0E0E0", "font": ("Segoe UI", 9, "bold")}
        entry_style = {"bg": "#444444", "fg": "#E0E0E0", "bd": 1, "relief": "solid", 
                       "font": ("Segoe UI", 10), "highlightbackground": "#CCCCCC", "highlightcolor": "#4A90E2", "highlightthickness": 1}
        #Estilo:
        button_action_style = {
            "bg": "#4A90E2",  # Azul principal
            "fg": "white",    # Texto blanco
            "font": ("Segoe UI", 9, "bold"),
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2",
            "activebackground": "#357ABD",
            "activeforeground": "white",
            "padx": 15,       # Padding horizontal interno
            "pady": 3         # Padding vertical interno
        }
        
        etiquetaTitulo = Label(self.frameArribaC, text="Barberos",  font=("Roboto", 20, "bold"), bg="#333333", fg="#FFFFFF")
        etiquetaTitulo.grid(row=0, column=0)
        #Creación de la tabla
        columnasTabla = ("nombre", "apellidoP", "telefono", "especialidad", "calificacion", "estatus") #Tupla con los nombres de las columnas, la primera es con #0
        self.tablaBarberos = ttk.Treeview(self.frameArribaC, columns= columnasTabla, height=20) #Constructor de la tabla
        self.tablaBarberos.grid(row=1, column=0, padx=10, pady=5)

        #se le asigna el ancho a cada columna
        self.tablaBarberos.column("#0", width=60)
        for col in columnasTabla:
            self.tablaBarberos.column(col, width=100)
            if (col == "estatus"):
                self.tablaBarberos.column(col, width=60)

        #Se le asigna nombre a las columnas
        self.tablaBarberos.heading("#0", text="ID")
        self.tablaBarberos.heading("nombre", text="Nombre")
        self.tablaBarberos.heading("apellidoP", text="Apellido")
        self.tablaBarberos.heading("telefono", text="Telefono")
        self.tablaBarberos.heading("especialidad", text="Especialidad")
        self.tablaBarberos.heading("calificacion", text="Calificacion")
        self.tablaBarberos.heading("estatus", text="Estatus")


        #Etiquetas del segundo frame
        etiquetaTituloBarberos = Label(self.frameAbajoC, text="Registro de Barberos", **label_style)
        etiquetaTituloBarberos.grid(row=0, column=0)


        #Etiquetas para entrys
        etiquetaNombre = Label(self.frameAbajoC, text="Nombre: ", **label_style)
        etiquetaNombre.grid(row=1, column=0, sticky="w", pady=4)
        self.campoNombre = Entry(self.frameAbajoC, **entry_style)
        self.campoNombre.grid(row=1, column=1, padx=5)

        etiquetaApellido = Label(self.frameAbajoC, text="Apellido: ", **label_style)
        etiquetaApellido.grid(row=2, column=0, sticky="w", pady=4)
        self.campoApellido = Entry(self.frameAbajoC, **entry_style)
        self.campoApellido.grid(row=2, column=1, padx=5)

        etiquetaTelefono = Label(self.frameAbajoC, text="Telefono: ", **label_style)
        etiquetaTelefono.grid(row=3, column=0, sticky="w", pady=4)
        self.campoTelefono = Entry(self.frameAbajoC, **entry_style)
        self.campoTelefono.grid(row=3, column=1, padx=5)

        etiquetaEspecialidad = Label(self.frameAbajoC, text="Especialidad: ", **label_style)
        etiquetaEspecialidad.grid(row=4, column=0, sticky="w", pady=4)
        self.campoEspecialidad = Entry(self.frameAbajoC, **entry_style)
        self.campoEspecialidad.grid(row=4, column=1, padx=5)

        etiquetaId = Label(self.frameAbajoC, text="Id: ", **label_style)
        etiquetaId.grid(row=5, column=0, sticky="w", pady=4)
        self.campoId = Entry(self.frameAbajoC, **entry_style)
        self.campoId.grid(row=5, column=1, padx=5)

        etiquetaCalificacion = Label(self.frameAbajoC, text="Calificacion: ", **label_style)
        etiquetaCalificacion.grid(row=1, column=2, sticky="w", pady=4)
        self.campoCalificacion = Entry(self.frameAbajoC, **entry_style)
        self.campoCalificacion.grid(row=1, column=3, padx=5)

        etiquetaEstatus = Label(self.frameAbajoC, text="Estatus: ", **label_style)
        etiquetaEstatus.grid(row=2, column=2, sticky="w", pady=4)
        self.campoEstatus = Entry(self.frameAbajoC, **entry_style)
        self.campoEstatus.grid(row=2, column=3, padx=5)

        self.botonRegistrar = Button(self.frameAbajoC, text="Registrar Barbero", **button_action_style)
        self.botonRegistrar.grid(row=4, column=4, sticky="e", padx=10)

        self.botonActualizar = Button(self.frameAbajoC, text="Actualizar Barbero", **button_action_style)
        self.botonActualizar.grid(row=5, column=4, sticky="e", padx=10)

        self.botonEliminar =  Button(self.frameAbajoC, text="Eliminar Barbero", **button_action_style)
        self.botonEliminar.grid(row=3, column=4, sticky="e", padx=10)

        self.frameAbajoC.grid_columnconfigure(4, weight=1)
