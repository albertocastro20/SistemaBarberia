import tkinter as tk #Libreria básica
from tkinter import * 
from tkinter import ttk #Libreria con nuevow wg
from tkcalendar import Calendar #Calendario

from Modelo.Clases import Cliente

import datetime

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
                       "font": ("Segoe UI", 10), "highlightbackground": "#CCCCCC", "highlightcolor": "#4A90E2", "highlightthickness": 1, "readonlybackground": "#444444", "disabledforeground": "#E0E0E0"}



        #Etiquetas para entrys
        etiquetaNombre = Label(self.frameAbajoC, text="Nombre: ", **label_style)
        etiquetaNombre.grid(row=1, column=0, sticky="w", pady=4)
        self.campoNombre = Entry(self.frameAbajoC, **entry_style, )
        self.campoNombre.grid(row=1, column=1, padx=5)

        etiquetaApellido = Label(self.frameAbajoC, text="Apellido: ", **label_style)
        etiquetaApellido.grid(row=2, column=0, sticky="w", pady=4)
        self.campoApellido = Entry(self.frameAbajoC, **entry_style)
        self.campoApellido.grid(row=2, column=1, padx=5)

        etiquetaTelefono = Label(self.frameAbajoC, text="Telefono: ", **label_style)
        etiquetaTelefono.grid(row=3, column=0, sticky="w", pady=4)
        self.campoTelefono = Entry(self.frameAbajoC, **entry_style)
        self.campoTelefono.grid(row=3, column=1, padx=5)

        
        #--------------------Seccion de Fechas de nacimiento ------------------------------------
        etiquetaNacimiento = Label(self.frameAbajoC, text="Fecha de Nacimiento (dd/mm/yyyy):", **label_style)
        etiquetaNacimiento.grid(row=4, column=0, sticky="w", pady=4)
        frameFecha = Frame(self.frameAbajoC, width=146, height=25, bg="#333333", # Fondo blanco para el formulario
                                 relief="flat", bd=0, highlightbackground="#E0E0E0", highlightthickness=1)
        frameFecha.grid(row=4, column=1)
        frameFecha.grid_propagate(False)

        listaDia = list()
        for i in range(1, 32, 1):
            listaDia.append(i)
        
        meses = ("Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")

        
        self.comboDia = ttk.Combobox(frameFecha, values=listaDia, width=3, state= "readonly")
        self.comboDia.grid(row=0, column=0, padx=2, pady=2)

        self.comboMes = ttk.Combobox(frameFecha, values= meses, width=4, state= "readonly")
        self.comboMes.grid(row=0, column=1, padx=2, pady=2)

        listaYear = list()

        for i in range(2025, 1940, -1):
            listaYear.append(i)

        self.comboYear = ttk.Combobox(frameFecha, values=listaYear, width=5, state= "readonly")
        self.comboYear.grid(row=0, column=2, padx=2, pady=2)
        #self.campoNacimiento = Entry(self.frameAbajoC, **entry_style)
        #self.campoNacimiento.grid(row=4, column=1, padx=5)


        #------------------------------------------------------------------------------------------

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
        nombre = self.campoNombre.get().capitalize()
        apellido = self.campoApellido.get().capitalize()
        telefono = self.campoTelefono.get()

        #---Fecha----
        print(self.comboYear.get())
        print(str(self.comboMes.current() + 1))
        print(self.comboDia.get())
        nacimiento = self.comboYear.get() +"-"+str(self.comboMes.current() + 1)+"-"+self.comboDia.get()



        #nacimiento = self.campoNacimiento.get()
        cli = Cliente(id, nombre, apellido, telefono, nacimiento, None)

        #Retorna un objeto de Cliente que servirá para tfodas las demas funciones
        return cli
        
    def insertarValoresCliente(self):
        #Llama a la funcion que inserta un cliente en la BD
        validado = self.validarCampos()
        if(validado):
            self.controlador.insercionCliente(self.obtenerValores())
            tk.messagebox.showinfo("Nuevo Cliente", "Cliente registrado correctamente")
            self.limpiarEntrys()
        else:
            tk.messagebox.showinfo("Error", "Error en alguno de los campos")

    def actualizarValoresCliente(self):
        #Funcion que actualiza los valores de un cliente
        validado = self.validarCampos()
        if(validado):
            self.controlador.actualizarCliente(self.obtenerValores())
            tk.messagebox.showinfo("Actualización Cliente", "Información Actualizada")

            self.limpiarEntrys()
        
        else:
            tk.messagebox.showinfo("Error", "Error en alguno de los campos")

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
        self.campoId.config(state="normal")
        
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
            #self.campoNacimiento.insert(0, string= tuplaValores[3])
            fecha = tuplaValores[3]
            self.comboDia.set(fecha[8:])
            mes = int(fecha[5:7])

            self.comboMes.current(mes-1)
            self.comboYear.set(fecha[:4])

            #self.comboDia[:-2]

        self.campoId.config(state= "readonly")
        #self.tablaClientes.selection_remove(self.tablaClientes.get_children())

    def limpiarEntrys(self):
        
        #END especifica el ultimo caracter
        self.campoId.config(state="normal")
        self.campoId.delete(0, END)
        self.campoNombre.delete(0, END)
        self.campoApellido.delete(0, END)
        self.campoTelefono.delete(0, END)
        #self.campoNacimiento.delete(0, END)
        self.comboDia.set("")
        self.comboMes.set("")
        self.comboYear.set("")

    def limpiarTabla(self):
        self.tablaClientes.delete(*self.tablaClientes.get_children())
        #self.tablaClientes.selection_remove(*self.tablaClientes.get_children())

    def validarCampos(self):
        validado = True
        if(self.campoTelefono.get().isnumeric() == False):
            validado = False

        if(len(self.campoTelefono.get()) != 10 ):
            validado = False

        if(self.campoNombre.get().isalpha() == False or self.campoApellido.get().isalpha() == False):
            validado = False

        if(self.comboDia.get() == "" or self.comboMes.get() == "" or self.comboYear.get() == ""):
            validado = False

        return validado
            
