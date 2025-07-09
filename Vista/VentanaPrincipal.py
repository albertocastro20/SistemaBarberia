
#Se importan todas las librerias que utilizaremos
import tkinter as tk #Libreria básica
from tkinter import * 
from tkinter import ttk #Libreria con nuevow wg
from tkcalendar import Calendar #Calendario

from Modelo.Conexion import *
from Modelo.Clases import *
from Controlador.ControladorMVC import *

import datetime


#Frame principal 650x460

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
                  background=[('active', '#34495E')]) # Color al pasar el ratón por encabezados



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



class ClientesFrame(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent, bg="#2C2525")
        self.controlador = controlador
        
        self.campoId = None
        self.campoNombre = None
        self.campoApellido = None
        self.campoTelefono = None
        self.campoNacimiento = None

        self.iniciarFrames()
        self.iniciarWidgets()

    def iniciarFrames(self):

        #self.frameArribaC = Frame(self, width=640, height=270, bg="white")
        self.frameArribaC = Frame(self, width=640, height=260, bg="#333333", # Fondo blanco para la tabla
                                  relief="flat", bd=0, highlightbackground="#E0E0E0", highlightthickness=1)
        self.frameArribaC.grid(row=0, column=0, padx=5, pady=5)
        self.frameArribaC.grid_propagate(False)

        #self.frameAbajoC = Frame(self, width=640, height=170, bg="white")
        self.frameAbajoC = Frame(self, width=640, height=180, bg="#333333", # Fondo blanco para el formulario
                                 relief="flat", bd=0, highlightbackground="#E0E0E0", highlightthickness=1)
        self.frameAbajoC.grid(row=1, column=0, padx=5, pady=5)
        self.frameAbajoC.grid_propagate(False)

    def iniciarWidgets(self):
        

        etiquetaTitulo = Label(self.frameArribaC, text="Clientes registrados", font=("Roboto", 20, "bold"), bg="#333333", fg="#FFFFFF")
        etiquetaTitulo.grid(row=0, column=0)
        #Creación de la tabla

        #Aqui le daremos el diseño que tendrá la tabla 

        """style = ttk.Style()
        style.theme_use("clam") # Un tema más moderno para ttk
        style.configure("Treeview", 
                        background="#FFFFFF", 
                        foreground="#333333", 
                        rowheight=20, # Altura de fila un poco mayor
                        fieldbackground="#FFFFFF",
                        font=("Segoe UI", 8))
        style.map("Treeview", 
                  background=[('selected', '#4A90E2')]) # Azul vibrante para la selección

        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 10, "bold"), 
                        background="#E0E0E0", # Gris claro para encabezados
                        foreground="#333333",
                        relief="flat")
        style.map("Treeview.Heading", 
                  background=[('active', '#CCCCCC')]) # Gris más oscuro al pasar el ratón por el encabezado
"""

        columnasTabla = ("nombre", "apellido", "telefono", "fecha", "numeroVisitas") #Tupla con los nombres de las columnas, la primera es con #0
        self.tablaClientes = ttk.Treeview(self.frameArribaC, columns= columnasTabla, height=9, show="tree headings") #Constructor de la tabla
        self.tablaClientes.grid(row=1, column=0, padx=10, pady=5)

        #se le asigna el ancho a cada columna
        self.tablaClientes.column("#0", width=80)
        for col in columnasTabla:
            self.tablaClientes.column(col, width=108)

        #Se le asigna nombre a las columnas
        self.tablaClientes.heading("#0", text="ID")
        self.tablaClientes.heading("nombre", text="Nombre")
        self.tablaClientes.heading("apellido", text="Apellido")
        self.tablaClientes.heading("fecha", text="FechaN")
        self.tablaClientes.heading("telefono", text="Telefono")
        self.tablaClientes.heading("numeroVisitas", text="Visitas")

        self.tablaClientes.bind('<<TreeviewSelect>>', self.seleccionCliente) #Se le asigna un evento al seleccionar una fila


        #Etiquetas del segundo frame
        etiquetaTituloClientes = Label(self.frameAbajoC, text="Registro de clientes", font=("Roboto", 18, "bold"), bg="#333333", fg="#FFFFFF")
        etiquetaTituloClientes.grid(row=0, column=0)

        # Estilo para Labels y Entrys
        label_style = {"bg": "#333333", "fg": "#E0E0E0", "font": ("Segoe UI", 9, "bold")}
        entry_style = {"bg": "#444444", "fg": "#E0E0E0", "bd": 1, "relief": "solid", 
                       "font": ("Segoe UI", 10), "highlightbackground": "#CCCCCC", "highlightcolor": "#4A90E2", "highlightthickness": 1}



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

        etiquetaNacimiento = Label(self.frameAbajoC, text="Fecha de Nacimiento: ", **label_style)
        etiquetaNacimiento.grid(row=4, column=0, sticky="w", pady=4)
        self.campoNacimiento = Entry(self.frameAbajoC, **entry_style)
        self.campoNacimiento.grid(row=4, column=1, padx=5)

        etiquetaId = Label(self.frameAbajoC, text="Id: ", **label_style)
        etiquetaId.grid(row=5, column=0, sticky="w", pady=4)
        self.campoId = Entry(self.frameAbajoC, **entry_style)
        self.campoId.grid(row=5, column=1, padx=5)

        #Configuracion de los botones
        #Estilo:
        button_action_style = {
            "bg": "#4A90E2",  # Azul principal
            "fg": "white",    # Texto blanco
            "font": ("Segoe UI", 10, "bold"),
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2",
            "activebackground": "#357ABD",
            "activeforeground": "white",
            "padx": 15,       # Padding horizontal interno
            "pady": 3         # Padding vertical interno
        }

        #Se configuran

        # Usamos un Frame para agrupar los botones y luego lo posicionamos con grid
        button_group_frame = Frame(self.frameAbajoC, bg="#333333")
        button_group_frame.grid(row=0, column=4, rowspan=7, padx=(20,20), pady=(5, 5), sticky="ne") # Alinear a la derecha superior
        

        self.botonMostrar = Button(button_group_frame, text="Mostrar clientes", command= lambda: self.consultaGeneralClientes(), **button_action_style)
        self.botonMostrar.grid(row=1, column=0, sticky="e", padx=10, pady=(10, 6))
        
        self.botonBuscar = Button(button_group_frame, text="Buscar Cliente", command= lambda: self.consultaCliente(), **button_action_style)
        self.botonBuscar.grid(row=3, column=0, sticky="e", padx=10, pady=6)
        
        self.botonRegistrar = Button(button_group_frame, text="Registrar Cliente", command= lambda: self.insertarValoresCliente(), **button_action_style)
        self.botonRegistrar.grid(row=4, column=0, sticky="e", padx=10, pady=6)

        self.botonActualizar = Button(button_group_frame, text="Actualizar Cliente", command= lambda: self.actualizarValoresCliente(), **button_action_style)
        self.botonActualizar.grid(row=5, column=0, sticky="e", padx=10, pady=6)

        self.frameAbajoC.grid_columnconfigure(2, weight=1)

    def obtenerValores(self):
        """Esta funcion obtiene los valores de los campos"""
        id = self.campoId.get()
        nombre = self.campoNombre.get()
        apellido = self.campoApellido.get()
        telefono = self.campoTelefono.get()
        nacimiento = self.campoNacimiento.get()
        cli = Cliente(id, nombre, apellido, telefono, nacimiento, None)

        #Retorna un objeto de Cliente que servirá para tfodas las demas funciones
        return cli
        
    def insertarValoresCliente(self):
        #Llama a la funcion que inserta un cliente en la BD
        self.controlador.insercionCliente(self.obtenerValores())

    def actualizarValoresCliente(self):
        #Funcion que actualiza los valores de un cliente
        self.controlador.actualizarCliente(self.obtenerValores())

    #Consulta a un cliente en específico
    def consultaCliente(self):
        self.limpiarTabla()
        tupla = self.controlador.consultarCliente(self.obtenerValores())
        
        for i in tupla:
            valores = (i[1], i[2], i[3], i[4], i[5])
            self.tablaClientes.insert("", "end", text=i[0], values=valores)

    #Consulta todos los clientes
    def consultaGeneralClientes(self):
        
        self.limpiarEntrys()
        self.limpiarTabla()
        
        valoresTabla = self.controlador.consultaGeneralCliente()

        for i in valoresTabla:
            tuplaNueva = (i[1], i[2], i[3], i[4], i[5])
            self.tablaClientes.insert("", "end", text = i[0], values=tuplaNueva)

    def seleccionCliente(self, evento):
        self.limpiarEntrys()
        
        #Con esa función se obtiene los id de las filas seleccionadas
        clienteSeleccionado = self.tablaClientes.selection()

        #Se le asigna un if para verificar que la tupla que se devuelve no está vacia
        #Se hace de esta manera por que al eliminar todos los elementos de la tabla se genera de nuevo el evento
        if clienteSeleccionado:
        
            #print(self.tablaClientes.item(clienteSeleccionado, 'text'))
            self.campoId.insert(0, string = (self.tablaClientes.item(clienteSeleccionado, 'text')))

            #for i in clienteSeleccionado:
            tuplaValores = self.tablaClientes.item(clienteSeleccionado, "values")

            self.campoNombre.insert(0, string=tuplaValores[0])
            self.campoApellido.insert(0, string = tuplaValores[1])
            self.campoTelefono.insert(0, string = tuplaValores[2])
            self.campoNacimiento.insert(0, string= tuplaValores[3])

        #self.tablaClientes.selection_remove(self.tablaClientes.get_children())

    def limpiarEntrys(self):
        
        #END especifica el ultimo caracter
        self.campoId.delete(0, END)
        self.campoNombre.delete(0, END)
        self.campoApellido.delete(0, END)
        self.campoTelefono.delete(0, END)
        self.campoNacimiento.delete(0, END)

    def limpiarTabla(self):
        self.tablaClientes.delete(*self.tablaClientes.get_children())
        #self.tablaClientes.selection_remove(*self.tablaClientes.get_children())
        

#Frame de los barberos

class BarberosFrame(tk.Frame):
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
        etiquetaTitulo = Label(self.frameArribaC, text="Barberos", font=("Arial", 13))
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
        etiquetaTituloBarberos = Label(self.frameAbajoC, text="Registro de Barberos", font=("Arial", 12))
        etiquetaTituloBarberos.grid(row=0, column=0)


        #Etiquetas para entrys
        etiquetaNombre = Label(self.frameAbajoC, text="Nombre: ")
        etiquetaNombre.grid(row=1, column=0, sticky="w", pady=4)
        self.campoNombre = Entry(self.frameAbajoC)
        self.campoNombre.grid(row=1, column=1, padx=5)

        etiquetaApellido = Label(self.frameAbajoC, text="Apellido: ")
        etiquetaApellido.grid(row=2, column=0, sticky="w", pady=4)
        self.campoApellido = Entry(self.frameAbajoC)
        self.campoApellido.grid(row=2, column=1, padx=5)

        etiquetaTelefono = Label(self.frameAbajoC, text="Telefono: ")
        etiquetaTelefono.grid(row=3, column=0, sticky="w", pady=4)
        self.campoTelefono = Entry(self.frameAbajoC)
        self.campoTelefono.grid(row=3, column=1, padx=5)

        etiquetaEspecialidad = Label(self.frameAbajoC, text="Especialidad: ")
        etiquetaEspecialidad.grid(row=4, column=0, sticky="w", pady=4)
        self.campoEspecialidad = Entry(self.frameAbajoC)
        self.campoEspecialidad.grid(row=4, column=1, padx=5)

        etiquetaId = Label(self.frameAbajoC, text="Id: ")
        etiquetaId.grid(row=5, column=0, sticky="w", pady=4)
        self.campoId = Entry(self.frameAbajoC)
        self.campoId.grid(row=5, column=1, padx=5)

        etiquetaCalificacion = Label(self.frameAbajoC, text="Calificacion: ")
        etiquetaCalificacion.grid(row=1, column=2, sticky="w", pady=4)
        self.campoCalificacion = Entry(self.frameAbajoC)
        self.campoCalificacion.grid(row=1, column=3, padx=5)

        etiquetaEstatus = Label(self.frameAbajoC, text="Estatus: ")
        etiquetaEstatus.grid(row=2, column=2, sticky="w", pady=4)
        self.campoEstatus = Entry(self.frameAbajoC)
        self.campoEstatus.grid(row=2, column=3, padx=5)

        self.botonRegistrar = Button(self.frameAbajoC, text="Registrar Barbero")
        self.botonRegistrar.grid(row=4, column=4, sticky="e", padx=10)

        self.botonActualizar = Button(self.frameAbajoC, text="Actualizar Barbero")
        self.botonActualizar.grid(row=5, column=4, sticky="e", padx=10)

        self.botonEliminar =  Button(self.frameAbajoC, text="Eliminar Barbero")
        self.botonEliminar.grid(row=3, column=4, sticky="e", padx=10)

        self.frameAbajoC.grid_columnconfigure(4, weight=1)

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



class BarberiaPrincipal(tk.Frame):

    def __init__(self, parent, controlador_recibido):
        super().__init__(parent)
        self.parent = parent
        self.controlador_recibido = controlador_recibido
        self.parent.title("Barberia")
        self.parent.geometry("900x600")
        self.parent.config(bg="#1A1A1A") # Fondo oscuro para un look moderno

        self.framesSeccion = {}
        self.active_button = None
    
        self.iniciarWidgets()
        #self.iniciarBarraMenu()

        self.mostrarFrame("Citas")

        self.conexion = Conexion("root", "Cris8426")

    def iniciarWidgets(self):
        self.iniciarBarraMenu()
        self.iniciarFrames()
        self.componentesBarraLateral()
        self.crearFramesSeccion()
        
    def iniciarFrames(self):
        #vamos a cambiar la interfaz gráfica
        
        self.frameTitulo = Frame(self.parent, width=850, height=100, bg="#333333", highlightbackground="#555555", highlightthickness=1) # Fondo oscuro y borde sutil
        self.frameTitulo.grid(row=0, column=0, padx=25, pady=10, columnspan=2)
        self.frameTitulo.grid_propagate(False)
        #Se asigna la etiqueta al Frame
        titulo = Label(self.frameTitulo, text="¡Bienvenido a tu Barbería!", bg="#333333", fg="#E0E0E0") # Texto claro y fondo oscuro
        titulo.config(font=("Segoe UI", 28, "bold")) # Fuente moderna y negrita
        titulo.grid(row=0, column=0, padx=240, pady=20)
        
        self.frameBotones = Frame(self.parent, width=150, height=460, bg="#2C2C2C", highlightbackground="#555555", highlightthickness=1) # Fondo más oscuro y borde sutil
        self.frameBotones.grid(row=1, column=0, padx=10, pady=10)
        self.frameBotones.grid_propagate(False)

        self.framePrincipal = Frame(self.parent, width=650, height=460, bg="#000000", highlightbackground="#000000", highlightthickness=1) # Fondo claro para el contenido principal
        self.framePrincipal.grid(row=1, column=1, padx=10, pady=10)
        self.framePrincipal.grid_propagate(False)

        

    def crearFramesSeccion(self):
        for F in (CitasFrame, ClientesFrame, BarberosFrame, ServiciosFrame):
            pageName = F.__name__.replace("Frame", "")
            frame =  F(parent = self.framePrincipal, controlador = self.controlador_recibido)
            self.framesSeccion[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")


    def mostrarFrame(self, pageName):
        frame = self.framesSeccion[pageName]
        frame.tkraise()


    def componentesBarraLateral(self):
        # Estilo de botones consistente y atractivo
        button_style = {
            #"bg": "#4A90E2",  # Un azul vibrante
            "fg": "white",    # Texto blanco
            "width": 15,
            "height": 2,
            "bd": 0,          # Sin borde
            "font": ("Segoe UI", 12, "bold"), # Fuente un poco más grande y negrita
            "relief": "flat",
            #"activebackground": "#357ABD", # Color al hacer click
            #"activeforeground": "white",
            "cursor": "hand2", # Cambiar el cursor al pasar por encima
            "anchor": "w",
            "padx": 10

        }

        default_bg = "#5A5A5A" # Fondo normal (azul oscuro)
        hover_bg = "#28333F"   # Fondo al pasar el ratón (azul más claro)
        active_bg = "#000000"  # Fondo del botón activo (azul más brillante)

        
        #Se crean los objetos de boton en los cuales crearemos objetos
        def create_sidebar_button(parent_frame, text, command_func, row_idx):
            btn = Button(parent_frame, text=text, command=command_func, 
                         bg=default_bg, **button_style)
            btn.pack(padx=10,pady=(12, 10)) # Se usa pack dentro de frameBotones
            
            # Efecto hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=hover_bg) if b != self.active_button else None)
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=default_bg) if b != self.active_button else None)
            return btn
        
        
        #Funcion para verificar si el boton está activo
        def activate_button(button_to_activate, frame_name):
            if self.active_button:
                self.active_button.config(bg=default_bg) # Resetear el anterior botón activo
            button_to_activate.config(bg=active_bg) # Establecer el nuevo botón activo
            self.active_button = button_to_activate
            self.mostrarFrame(frame_name) # Llamar a la función de mostrar frame

        # Separación entre botones
        self.botonCita = create_sidebar_button(self.frameBotones, "  CITAS", lambda: activate_button(self.botonCita, "Citas"), 0)
        self.botonClientes = create_sidebar_button(self.frameBotones, "  CLIENTES", lambda: activate_button(self.botonClientes, "Clientes"), 1)
        self.botonServicios = create_sidebar_button(self.frameBotones, "  SERVICIOS", lambda: activate_button(self.botonServicios, "Servicios"), 2)
        self.botonBarberos = create_sidebar_button(self.frameBotones, "  BARBEROS", lambda: activate_button(self.botonBarberos, "Barberos"), 3)
        self.botonInventario = create_sidebar_button(self.frameBotones, "  INVENTARIO", lambda: activate_button(self.botonInventario, "Inventario"), 4)
        self.botonReportes = create_sidebar_button(self.frameBotones, "  REPORTES", lambda: activate_button(self.botonReportes, "Reportes"), 5)



    def iniciarBarraMenu(self):
        barraMenuP = Menu(self.parent, bg="#34495E", fg="#ECF0F1", 
                       activebackground="#4E6D8F", activeforeground="#FFFFFF",
                       font=("Segoe UI", 10))
        
        self.parent.config(menu= barraMenuP)
        menuArchivo = Menu(barraMenuP,  tearoff=0, bg="#333333", fg="#FFFFFF", 
                         activebackground="#555555", activeforeground="#FFFFFF")
        menuArchivo.add_command(label= "Establecer conexion", command= lambda: self.conexion.conectar())
        menuArchivo.add_command(label= "Iniciar Sesion")
        menuArchivo.add_command(label= "Cambiar de usuario")
        menuArchivo.add_command(label= "Cerrar Sesion")
        menuArchivo.add_command(label= "Salir de la Aplicación", command= lambda: self.parent.destroy())
        barraMenuP.add_cascade(label="Inicio", menu=menuArchivo)


        menuVentanas = Menu(barraMenuP, tearoff=0)
        menuVentanas.add_command(label= "Ventana Principal")
        menuVentanas.add_command(label= "Gestion de citas")
        menuVentanas.add_command(label= "Productos")
        menuVentanas.add_command(label= "Clientes")
        menuVentanas.add_command(label= "Servicios")
        menuVentanas.add_command(label= "Barberos")
        barraMenuP.add_cascade(label="Navegación", menu=menuVentanas)


        self.parent.config(menu=barraMenuP)
