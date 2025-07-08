
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
        super().__init__(parent)
        self.controlador = controlador
        self.iniciarFramesCitas()
        self.iniciarWidgetsCitas()


    def iniciarFramesCitas(self):
        #Se iniciia el Frame en el que irán los otros dos Frames
        self.frameCitaP = Frame(self, width=650, height=460, bg="black")
        self.frameCitaP.grid(row=0, column=0)
        self.frameCitaP.grid_propagate(False)
        
        self.frameCitaI = Frame(self.frameCitaP, width=370, height=440, bg="white")
        self.frameCitaI.grid(row=0, column=0, padx=7, pady=10)
        self.frameCitaI.grid_propagate(False) #Evita que no muestre el tamaño original

        self.frameCitaD = Frame(self.frameCitaP, width=250, height= 440, bg="white")
        self.frameCitaD.grid(column=1, row=0, padx=7, pady=10)
        self.frameCitaD.grid_propagate(False)

    def iniciarWidgetsCitas(self):
        #Se crea una variable en el cual irá almacenado el día almacenado
        self.diaSeleccionado= ""
        
        self.calendarioCitas = Calendar(self.frameCitaI, showweeknumbers = False, showothermonthdays = False, background= "black")
        self.calendarioCitas.config(font = ("Arial", 14)) #Se le da tamaño al calendario
        self.calendarioCitas.grid(row = 0, column=0, padx = 10, pady = 10, columnspan = 2) #Columnspan para asignarle cuanos espacios ocupará
        self.calendarioCitas.bind("<<CalendarSelected>>", self.fechaSeleccionada) #Se le asigna un evento al calendario

        #Citas del día
        
        #Se selecciona la fecha actual, por lo que se mostrarán las citas del día
        self.diaSeleccionado = self.calendarioCitas.selection_get() #Se le asigna la fecha
        self.etiquetaGestionT = Label(self.frameCitaI, text=f"Citas del dia: {self.diaSeleccionado.strftime('%d / %m/ %Y')}", anchor="w")
        self.etiquetaGestionT.grid(row=1, column=0, pady=5)

        self.botonMostrarCitas = Button(self.frameCitaI, text="Mostrar", command=lambda: self.mostrarCitas())
        self.botonMostrarCitas.grid(row=1, column=1, pady=5)

        columnasTabla = ("Hora", "Cliente", "Barbero") #Tupla con los nombres de las columnas, la primera es con #0
        self.tablaCitas = ttk.Treeview(self.frameCitaI, columns= columnasTabla, height=6, show="tree headings") #Constructor de la tabla
        self.tablaCitas.grid(row=2, column=0, padx=10, pady=5, columnspan=2)

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
        etiquetaIzquierda = Label(self.frameCitaD, text="Detalles de la cita", font=("Arial", 15))
        etiquetaIzquierda.grid(row=0, column=0, padx=35, columnspan=3, pady=15)
        

        etiquetaCliente = Label(self.frameCitaD, text="Cliente(id): ", font=("Arial", 13))
        etiquetaCliente.grid(row=1, column=0, pady=5, sticky="w")
        self.campoCliente = Entry(self.frameCitaD)
        self.campoCliente.grid(row=1, column=2)

        etiquetaBarbero = Label(self.frameCitaD, text="Barbero (id): ", font=("Arial", 13))
        etiquetaBarbero.grid(row=2, column=0, pady=5, sticky="w")
        self.campoBarbero = Entry(self.frameCitaD)
        self.campoBarbero.grid(row=2, column=2)

        #Cambiar por comboBox

        etiquetaHora  = Label(self.frameCitaD, text="Hora: ", font=("Arial", 13))
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

        self.comboHora = ttk.Combobox(self.frameCitaD, state="readonly", values=self.listaHoras)
        self.comboHora.grid(row=3, column=2)

        self.listaEstatus = ["Activo", "Pendiente", "Cancelado"]

        etiquetaEstatus = Label(self.frameCitaD, text="Estatus: ", font=("Arial", 13))
        etiquetaEstatus.grid(row=4, column=0, pady=5, sticky="w")
        self.comboEstatus = ttk.Combobox(self.frameCitaD, state="readonly", values = self.listaEstatus)
        self.comboEstatus.grid(row=4, column=2)
        
        etiquetaId = Label(self.frameCitaD, text="ID", font=("Arial", 13))
        etiquetaId.grid(row=5, column=0, pady=5, sticky="w")
        self.campoId = Entry(self.frameCitaD, state="normal")
        self.campoId.grid(row=5, column=2, pady=5)

        etiquetaServicios = Label(self.frameCitaD, text="Servicios: ", font=("Arial", 13))
        etiquetaServicios.grid(row=6, column=0, pady=5, sticky="w")
        self.campoServicios = Text(self.frameCitaD, width=27, height=4)
        self.campoServicios.grid(row=7, column=0, columnspan=3, padx= 2, pady = 5)

        #Botones de acción
        self.botonInsertarCita = Button(self.frameCitaD, text="Insertar Cita", command= lambda: self.insercionCita())
        self.botonInsertarCita.grid(row=8, column=0, pady=5, padx=5, sticky="w")
        self.botonActualizarCita = Button(self.frameCitaD, text="Actualizar Cita", command= lambda: self.actualizarCita())
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
        super().__init__(parent)
        self.controlador = controlador
        
        self.campoId = None
        self.campoNombre = None
        self.campoApellido = None
        self.campoTelefono = None
        self.campoNacimiento = None
        self.campoId = None

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
        

        etiquetaTitulo = Label(self.frameArribaC, text="Clientes registrados", font=("Arial", 13))
        etiquetaTitulo.grid(row=0, column=0)
        #Creación de la tabla
        columnasTabla = ("nombre", "apellido", "telefono", "fecha", "numeroVisitas") #Tupla con los nombres de las columnas, la primera es con #0
        self.tablaClientes = ttk.Treeview(self.frameArribaC, columns= columnasTabla, height=10, show="tree headings") #Constructor de la tabla
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
        etiquetaTituloClientes = Label(self.frameAbajoC, text="Registro de clientes", font=("Arial", 12))
        etiquetaTituloClientes.grid(row=0, column=0)


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

        etiquetaNacimiento = Label(self.frameAbajoC, text="Fecha de Nacimiento: ")
        etiquetaNacimiento.grid(row=4, column=0, sticky="w", pady=4)
        self.campoNacimiento = Entry(self.frameAbajoC)
        self.campoNacimiento.grid(row=4, column=1, padx=5)

        etiquetaId = Label(self.frameAbajoC, text="Id: ")
        etiquetaId.grid(row=5, column=0, sticky="w", pady=4)
        self.campoId = Entry(self.frameAbajoC)
        self.campoId.grid(row=5, column=1, padx=5)

        self.botonMostrar = Button(self.frameAbajoC, text="Mostrar clientes", command= lambda: self.consultaGeneralClientes())
        self.botonMostrar.grid(row=1, column=2, sticky="e", padx=10)
        
        self.botonBuscar = Button(self.frameAbajoC, text="Buscar Cliente", command= lambda: self.consultaCliente())
        self.botonBuscar.grid(row=3, column=2, sticky="e", padx=10)
        
        self.botonRegistrar = Button(self.frameAbajoC, text="Registrar Cliente", command= lambda: self.insertarValoresCliente())
        self.botonRegistrar.grid(row=4, column=2, sticky="e", padx=10)

        self.botonActualizar = Button(self.frameAbajoC, text="Actualizar Cliente", command= lambda: self.actualizarValoresCliente())
        self.botonActualizar.grid(row=5, column=2, sticky="e", padx=10)

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
        

        self.iniciarWidgets()

        self.mostrarFrame("Citas")

        self.conexion = Conexion("root", "Cris8426")

    def iniciarWidgets(self):
        self.iniciarBarraMenu()
        self.iniciarFrames()
        self.componentesBarraLateral()
        self.crearFramesSeccion()
        
    def iniciarFrames(self):
        #vamos a cambiar la interfaz gráfica
        
        self.frameTitulo = Frame(self.parent, width=850, height=100, bg="black")
        self.frameTitulo.grid(row=0, column=0, padx=25, pady=10, columnspan=2)
        self.frameTitulo.grid_propagate(False)
        #Se asigna la etiqueta al Frame
        titulo = Label(self.frameTitulo, text="Barberia Principal")
        titulo.config(font=("Arial", 30))
        titulo.grid(row=0, column=0, padx=250, pady=20)
        
        self.frameBotones = Frame(self.parent, width=150, height=460, bg = "black")
        self.frameBotones.grid(row = 1, column = 0, padx=10, pady= 10)
        self.frameBotones.grid_propagate(False)

        self.framePrincipal = Frame(self.parent, width=650, height=460, bg = "white")
        self.framePrincipal.grid(row = 1, column= 1, padx=10, pady=10)
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
        
        
        #Pestaña izquierda, aqui tendremos todos los botones para acceder a las acciones en el Frame Principal
        botonCita =  Button(self.frameBotones, text="Citas", bg="skyblue", width=19, height=3, command= lambda: self.mostrarFrame("Citas"), bd=0).grid(row=0, column=0, padx=5, pady=5)

        botonClientes =  Button(self.frameBotones, text="Clientes", bg="skyblue", width=19, height=3, command= lambda: self.mostrarFrame("Clientes"), bd=0).grid(row=1, column=0, padx=5, pady=5)

        botonServicios =  Button(self.frameBotones, text="Servicios", bg="skyblue", width=19, height=3, command= lambda: self.mostrarFrame("Servicios"), bd=0).grid(row=2, column=0, padx=5, pady=5)

        botonBarberos =  Button(self.frameBotones, text="Barberos", bg="skyblue", width=19, height=3, command= lambda: self.mostrarFrame("Barberos"), bd=0).grid(row=3, column=0, padx=5, pady=5)

        botonInventario =  Button(self.frameBotones, text="Inventario", bg="skyblue", width=19, height=3,  bd=0).grid(row=4, column=0, padx=5, pady=5)

        botonReportes =  Button(self.frameBotones, text="Reportes", bg="skyblue", width=19, height=3, bd=0).grid(row=5, column=0, padx=5, pady=5)

    def iniciarBarraMenu(self):
        barraMenuP = Menu()
        menuArchivo = Menu(barraMenuP, tearoff=0)
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


"""if __name__ == "__main__":
    root = tk.Tk()
    Ventana =  BarberiaPrincipal(root)
    Ventana.mainloop()
    #root.destroy()
"""