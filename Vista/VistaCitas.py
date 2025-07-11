import tkinter as tk #Libreria básica
from tkinter import * 
from tkinter import ttk #Libreria con nuevow wg
from tkcalendar import Calendar #Calendario


from Modelo.Clases import *
import datetime

class CitasFrame(tk.Frame):
    #Iniciador del Frame
    def __init__(self, parent, controlador):
        super().__init__(parent, bg= "#2C2525")
        self.controlador = controlador
        self.iniciarFramesCitas()
        self.iniciarWidgetsCitas()


    def iniciarFramesCitas(self):
        #Se iniciia el Frame en el que irán los otros dos Frames
        
        self.frameCitaI = Frame(self, width=370, height=440, bg="#333333", # Gris oscuro para el fondo del calendario/tabla
                                relief="flat", bd=0, highlightbackground="#555555", highlightthickness=1)
       
        #self.frameCitaI = Frame(self, width=370, height=440, bg="white")
        self.frameCitaI.grid(row=0, column=0, padx=7, pady=10)
        self.frameCitaI.grid_propagate(False) #Evita que no muestre el tamaño original

        self.frameCitaD = Frame(self, width=259, height=440, bg="#333333", # Gris oscuro para el formulario de detalles
                                relief="flat", bd=0, highlightbackground="#555555", highlightthickness=1)
        
        #self.frameCitaD = Frame(self, width=250, height= 440, bg="white")
        self.frameCitaD.grid(column=1, row=0, padx=7, pady=10)
        self.frameCitaD.grid_propagate(False)

    def iniciarWidgetsCitas(self):
        #Se crea una variable en el cual irá almacenado el día almacenado
        self.diaSeleccionado= ""

        # Estilo para el calendario
        cal_style = {
            "selectbackground": "#4A90E2", # Azul para la fecha seleccionada
            "selectforeground": "white",
            "background": "#EB43C1", # Fondo del calendario
            "foreground": "#000000", # Texto de los días
            "headersbackground": "#4B2A4A", # Fondo de los encabezados (mes/año)
            "headersforeground": "white",
            "normalbackground": "#000000",
            "normalforeground": "#E0E0E0",
            "othermonthforeground": "#FFFFFF", # Días de otros meses más tenues
            "othermonthbackground": "#011847",
            "bordercolor": "#555555",
            "weekendbackground": "#410658",
            "weekendforeground": "#FFFFFF",
            "font": ("Arial", 14)
        }
        
        self.calendarioCitas = Calendar(self.frameCitaI, showweeknumbers = False, **cal_style)
        #self.calendarioCitas.config(font = ("Roboto", 14)) #Se le da tamaño al calendario
        self.calendarioCitas.grid(row = 0, column=0, padx = 10, pady = 10, columnspan = 2) #Columnspan para asignarle cuanos espacios ocupará
        self.calendarioCitas.bind("<<CalendarSelected>>", self.fechaSeleccionada) #Se le asigna un evento al calendario

        #Citas del día
        
        #Se selecciona la fecha actual, por lo que se mostrarán las citas del día
        self.diaSeleccionado = self.calendarioCitas.selection_get() #Se le asigna la fecha
        self.etiquetaGestionT = Label(self.frameCitaI, text=f"Citas del dia: {self.diaSeleccionado.strftime('%d / %m/ %Y')}", anchor="w", bg="#333333", fg="#E0E0E0", font=("Roboto", 11, "bold"))
        self.etiquetaGestionT.grid(row=1, column=0, pady=5)

         # Botón Mostrar Citas con estilo oscuro
        button_style = {
            "bg": "#4A90E2",  # Azul vibrante
            "fg": "white",    # Texto blanco
            "font": ("Segoe UI", 9, "bold"),
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2",
            "activebackground": "#357ABD",
            "activeforeground": "white",
            "padx": 15,
            "pady": 5
        }

        self.botonMostrarCitas = Button(self.frameCitaI, text="Mostrar", command=lambda: self.mostrarCitas(), **button_style)
        self.botonMostrarCitas.grid(row=1, column=1, pady=5)

        # Tabla de Citas
        style = ttk.Style()
        style.theme_use("clam") # Tema moderno
        style.configure("Treeview", 
                        background="#444444", # Fondo oscuro de la tabla
                        foreground="#E0E0E0", # Texto claro
                        rowheight=20, # Altura de fila
                        fieldbackground="#444444",
                        font=("Segoe UI", 9))
        style.map("Treeview", 
                  background=[('selected', '#2980B9')]) # Azul brillante para selección

        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 10, "bold"), 
                        background="#2C3E50", # Encabezados oscuros
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading", 
                  background=[('active', '#34495E')]) # Color al pasar el ratón por encabezados"""



        columnasTabla = ("Hora", "Cliente", "Barbero") #Tupla con los nombres de las columnas, la primera es con #0
        self.tablaCitas = ttk.Treeview(self.frameCitaI, columns= columnasTabla, height=5, show="tree headings") #Constructor de la tabla
        self.tablaCitas.grid(row=2, column=0, padx=10, pady=8, columnspan=2)

        #se le asigna el ancho a cada columna
        self.tablaCitas.column("#0", width=50)
        for col in columnasTabla:
            self.tablaCitas.column(col, width=100)

        #Se le asigna nombre a las columnas
        self.tablaCitas.heading("#0", text="ID")
        self.tablaCitas.heading("Hora", text="Hora")
        self.tablaCitas.heading("Cliente", text="Cliente")
        self.tablaCitas.heading("Barbero", text="Barbero")
        

        self.tablaCitas.bind('<<TreeviewSelect>>', self.seleccionadorCita) #Se le asigna un evento al seleccionar una fila
        
        #Detalles de la cita
        etiquetaIzquierda = Label(self.frameCitaD, text="Detalles de la cita",  font=("Roboto", 15, "bold"), bg="#333333", fg="#E0E0E0")
        etiquetaIzquierda.grid(row=0, column=0, padx=30, columnspan=3, pady=15)
        
        # Estilo para Labels y Entrys en el formulario oscuro
        label_style = {"bg": "#333333", "fg": "#E0E0E0", "font": ("Segoe UI", 9, "bold")}
        entry_style = {"bg": "#444444", "fg": "#E0E0E0", "bd": 1, "relief": "solid", 
                       "font": ("Segoe UI", 8), "insertbackground": "white", # Cursor blanco
                       "highlightbackground": "#555555", "highlightcolor": "#4A90E2", "highlightthickness": 1}
        
        style.configure("TCombobox", 
                        fieldbackground="#444444", # Fondo del campo de entrada
                        foreground="#E0E0E0",     # Texto del campo de entrada
                        background="#333333",     # Fondo de los botones del combobox
                        selectbackground="#566679",# Fondo al seleccionar en el desplegable
                        selectforeground="white",  # Texto al seleccionar en el desplegable
                        bordercolor="#555555",
                        lightcolor="#555555",
                        darkcolor="#333333",
                        arrowcolor="#E0E0E0",     # Color de la flecha
                        font=("Segoe UI", 9))
        # Mapeo para los estados del Combobox
        style.map('TCombobox', 
                  fieldbackground=[('readonly', '#444444'), ('focus', '#4A90E2')],
                  foreground=[('readonly', '#E0E0E0')],
                  selectbackground=[('readonly', '#4A90E2')],
                  selectforeground=[('readonly', '#FFFFFF')],
                  background=[('readonly', '#333333')],
                  arrowcolor=[('!disabled', '#E0E0E0')],
                  bordercolor=[('focus', '#4A90E2')])

        x = 0
        etiquetaCliente = Label(self.frameCitaD, text="Cliente(id): ",  **label_style)
        etiquetaCliente.grid(row=1, column=0, pady=5, sticky="w")
        self.campoCliente = Entry(self.frameCitaD, **entry_style)
        self.campoCliente.grid(row=1, column=1, padx=(0, x), columnspan=2, sticky="w")

        etiquetaBarbero = Label(self.frameCitaD, text="Barbero (id): ", **label_style)
        etiquetaBarbero.grid(row=2, column=0, pady=5, sticky="w")
        self.campoBarbero = Entry(self.frameCitaD, **entry_style)
        self.campoBarbero.grid(row=2, column=1, padx=(0, x), columnspan=2, sticky="w")

        #Cambiar por comboBox

        etiquetaHora  = Label(self.frameCitaD, text="Hora: ",  **label_style)
        etiquetaHora.grid(row=3, column=0, pady=5, sticky="w")

        self.listaHoras = list()

        for hora in range(10, 20):
            for minutos in range(0, 31, 30):
                if(minutos == 0):
                    minutosNuevos = "00"
                    horaMinutos = str(hora)+":"+str(minutosNuevos)
                else:
                    horaMinutos = str(hora)+":"+str(minutos)
                
                self.listaHoras.append(horaMinutos)

        self.comboHora = ttk.Combobox(self.frameCitaD, state="readonly", values=self.listaHoras, width=18)
        self.comboHora.grid(row=3, column=1, padx=(0, x), columnspan=2, sticky="w")

        self.listaEstatus = ["Activo", "Pendiente", "Cancelado"]

        etiquetaEstatus = Label(self.frameCitaD, text="Estatus: ", **label_style)
        etiquetaEstatus.grid(row=4, column=0, pady=5, sticky="w")
        self.comboEstatus = ttk.Combobox(self.frameCitaD, state="readonly", values = self.listaEstatus, width=18)
        self.comboEstatus.grid(row=4, column=1, padx=(0, x), columnspan=2, sticky="w")
        
        etiquetaId = Label(self.frameCitaD, text="ID", **label_style)
        etiquetaId.grid(row=5, column=0, pady=5, sticky="w")
        self.campoId = Entry(self.frameCitaD, state="normal", **entry_style)
        self.campoId.grid(row=5, column=1, pady=5, padx=(0, x), columnspan=2, sticky="w")

        etiquetaServicios = Label(self.frameCitaD, text="Servicios: ", **label_style)
        etiquetaServicios.grid(row=6, column=0, pady=5, sticky="w")
        self.campoServicios = Text(self.frameCitaD, width=27, height=4, **entry_style)
        self.campoServicios.grid(row=7, column=0, columnspan=3, padx= 2, pady = 5)

        #Botones de acción

        # Botones de acción (Insertar y Actualizar Cita)
        button_action_style_dark = {
            "bg": "#4A90E2",  # Azul principal
            "fg": "white",    # Texto blanco
            "font": ("Segoe UI", 9, "bold"),
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2",
            "activebackground": "#357ABD",
            "activeforeground": "white",
            "padx": 15,
            "pady": 8
        }

        self.botonInsertarCita = Button(self.frameCitaD, text="Insertar Cita", command= lambda: self.insercionCita(), **button_action_style_dark)
        self.botonInsertarCita.grid(row=8, column=0, pady=5, padx=5, sticky="w")
        self.botonActualizarCita = Button(self.frameCitaD, text="Actualizar Cita", command= lambda: self.actualizarCita(), **button_action_style_dark)
        self.botonActualizarCita.grid(row=9, column=0, pady=5, padx=5, sticky="w")

    def fechaSeleccionada(self, event):
        self.diaSeleccionado = self.calendarioCitas.selection_get() #Se le asigna la fecha
        self.etiquetaGestionT.config(text=f"Citas del dia: {self.diaSeleccionado.strftime('%d / %m/ %Y')}") #Se le da formato a la fecha


    def mostrarCitas(self):
        
        self.limpiarTabla()
        tuplaRecibidaCitas = self.controlador.mostrarCitas(self.obtenerValores())

        for i in tuplaRecibidaCitas:
            tuplaNueva = (i[1], i[2], i[3])
            self.tablaCitas.insert("", "end", text = i[0], values=tuplaNueva)


    def obtenerValores(self):
        fecha = self.calendarioCitas.selection_get()
        hora = self.comboHora.get()
        estatus = self.comboEstatus.get()
        comentarios = self.campoServicios.get(1.0, END)
        idCliente = self.campoCliente.get()
        idBarbero = self.campoBarbero.get()
        id = self.campoId.get()

        citaObtenida = Cita(id, fecha, hora, estatus, comentarios, idCliente, idBarbero)
        
        return citaObtenida

    def insercionCita(self):
        self.controlador.insercionCita(self.obtenerValores())
        self.limpiarEntrys()

    def actualizarCita(self):
        self.controlador.actualizarCita(self.obtenerValores())

    def limpiarTabla(self):
        self.tablaCitas.delete(*self.tablaCitas.get_children())

    def limpiarEntrys(self):
        self.campoId.delete(0, END)
        self.campoCliente.delete(0, END)
        self.campoBarbero.delete(0, END)
        self.campoServicios.delete(1.0, END)
        self.comboEstatus.set("")
        self.comboHora.set("")

    def seleccionadorCita(self, event):
        self.limpiarEntrys()
        
        citaSeleccionada = self.tablaCitas.selection()

        #Se le asigna un if para verificar que la tupla que se devuelve no está vacia
        #Se hace de esta manera por que al eliminar todos los elementos de la tabla se genera de nuevo el evento
        if citaSeleccionada:
            citaBuscar = Cita(self.tablaCitas.item(citaSeleccionada, 'text'), None, None, None, None, None, None)
            citaRecibida = self.controlador.buscarCita(citaBuscar)

            for citita in citaRecibida:
                #Creamos un string que vamos a usar para compararlo con la lista de horas
                horaRecibida = (datetime.datetime.min + citita[2]).time()
                horaFormateada = horaRecibida.strftime('%H:%M')

                #print(citaRecibida)

            
                #print(self.tablaClientes.item(clienteSeleccionado, 'text'))
                self.campoId.insert(0, string = citita[0])

                self.comboHora.current(self.listaHoras.index(horaFormateada))
                self.comboEstatus.current(self.listaEstatus.index(citita[3]))
                self.campoServicios.insert(1.0, citita[4])
                self.campoCliente.insert(0, string= citita[5])
                self.campoBarbero.insert(0, string= citita[6])

    def buscarCita(self):
        pass
        # self.controlador.buscarCita()
