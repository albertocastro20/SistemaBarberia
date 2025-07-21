import tkinter as tk
from tkinter import ttk
from tkinter import *
#from tkinter import messagebox
from tkinter.simpledialog import askinteger
import datetime

class VentasFrame(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador

        self.iniciarFrames()
        self.iniciarWidgets()
        self.after(3, self.llenarTablaServicios)
        self.after(3, self.llenarTablaProductos)
        self.after(3, self.llenarBarberos)

        #self.llenarTablaServicios()

    def iniciarFrames(self):
        self.frameIzquierdo = Frame(self, width=270, height=460, bg="#333333", # Gris oscuro para el fondo del calendario/tabla
                                relief="flat", bd=0, highlightbackground="#555555", highlightthickness=1)
        self.frameIzquierdo.grid(row=0, column=0)
        self.frameIzquierdo.grid_propagate(False)

        self.frameDerecho = Frame(self, width=380, height=460, bg="#333333", # Gris oscuro para el fondo del calendario/tabla
                                relief="flat", bd=0, highlightbackground="#555555", highlightthickness=1)
        self.frameDerecho.grid(row=0, column=1)
        self.frameDerecho.grid_propagate(False)

    def iniciarWidgets(self):
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
        label_style = {"bg": "#333333", "fg": "#E0E0E0", "font": ("Segoe UI", 9, "bold")}
        entry_style = {"bg": "#444444", "fg": "#E0E0E0", "bd": 1, "relief": "solid", 
                       "font": ("Segoe UI", 8), "insertbackground": "white", # Cursor blanco
                       "highlightbackground": "#555555", "highlightcolor": "#4A90E2", "highlightthickness": 1}

        eventoBotones = tk.Event()
        
        #Componentes del Frame Izquierdo
        frameTitulo = Frame(self.frameIzquierdo, width=260, height=30, bg="#333333", # Gris oscuro para el fondo del calendario/tabla
                                relief="flat", bd=0, highlightbackground="#555555", highlightthickness=1)
        frameTitulo.grid(row=0, column=0, padx=5, pady=5)
        frameTitulo.grid_propagate(False)

        etiquetaTitulo = Label(frameTitulo, text="Selección de Ventas", anchor="center", **label_style)
        etiquetaTitulo.grid(row=0, column=0, sticky="nsew")
        frameTitulo.grid_columnconfigure(0, weight=1)

        #Frame para el buscador
        frameBuscadorCliente = Frame(self.frameIzquierdo, width=260, height=60, bg="#333333", # Gris oscuro para el fondo del calendario/tabla
                                relief="flat", bd=0, highlightbackground="#555555", highlightthickness=1)
        frameBuscadorCliente.grid(row=1, column=0, padx=5, pady=5)
        frameBuscadorCliente.grid_propagate(False)

        etiquetaCliente = Label(frameBuscadorCliente, text="Cliente: ", **label_style)
        etiquetaCliente.grid(row=0, column=0, pady=2)

        self.campoCliente = Entry(frameBuscadorCliente, width=15, **entry_style)
        self.campoCliente.grid(row=0, column=1, pady=2)

        self.botonIniciarVenta = Button(frameBuscadorCliente, text="Añadir", command= lambda: self.iniciarVenta(), **button_style)
        self.botonIniciarVenta.grid(row=0, column=2, padx=(7, 3), pady=2)

        etiquetaBarbero = Label(frameBuscadorCliente, text="Barbero: ", **label_style)
        etiquetaBarbero.grid(row=1, column=0, pady=2)

        self.comboBarbero = ttk.Combobox(frameBuscadorCliente, font=("Arial", 10), width=15, state = "readonly")
        self.comboBarbero.grid(row=1, column=1, pady=2)

        #Frame para el Nootebook
        self.notebookInformacion = ttk.Notebook(self.frameIzquierdo)
        self.notebookInformacion.grid(row=2, column=0)

        #Pestaña de Servicios
        
        frameServicios = Frame(self.notebookInformacion, height=320, width= 250, bg="#333333", # Gris oscuro para el fondo del calendario/tabla
                                relief="flat", bd=0, highlightbackground="#555555", highlightthickness=1)
        self.notebookInformacion.add(frameServicios, text="Servicios")

        etiquetaInternaServicios = Label(frameServicios, text="Lista de servicios", **label_style)
        etiquetaInternaServicios.pack(side="top")
        
        columnasServicios = ("Servicio", "Precio")
        self.tablaServicios = ttk.Treeview(frameServicios, columns=columnasServicios, show="headings")
        

        self.tablaServicios.column("Servicio", width=165)
        self.tablaServicios.column("Precio", width=75)

        for col in columnasServicios:
            self.tablaServicios.heading(col, text=col)
        self.tablaServicios.pack(padx=5)


        self.botonAgregarServicio = Button(frameServicios, text="Añadir Servicios", command= lambda: self.agregarItemsTabla(1), **button_style)
        self.botonAgregarServicio.pack(padx=15, pady=15, fill="x")

        self.tablaServicios.bind('<<TreeviewSelect>>', self.seleccionServicios) #Se le asigna un evento al seleccionar una fila



        #Pestaña de Productos

        frameProductos = Frame(self.notebookInformacion, height=320, width= 250, bg="#333333", # Gris oscuro para el fondo del calendario/tabla
                                relief="flat", bd=0, highlightbackground="#555555", highlightthickness=1)
        self.notebookInformacion.add(frameProductos, text="Productos")

        etiquetaInternaProductos = Label(frameProductos, text="Lista de productos", **label_style)
        etiquetaInternaProductos.pack(side="top")
        
        columnasProductos = ("Producto", "Precio")
        self.tablaProductos = ttk.Treeview(frameProductos, columns=columnasProductos, show="headings")
        

        self.tablaProductos.column("Producto", width=165)
        self.tablaProductos.column("Precio", width=75)

        for col in columnasProductos:
            self.tablaProductos.heading(col, text=col)
        self.tablaProductos.pack(padx=5)

        self.botonAgregarProducto = Button(frameProductos, text="Añadir Producto", command= lambda: self.agregarItemsTabla(2), **button_style)
        self.botonAgregarProducto.pack(padx=15, pady=15, fill="x")

        self.tablaProductos.bind('<<TreeviewSelect>>', self.seleccionProductos) #Se le asigna un evento al seleccionar una fila

        #Componentes del Frame Derecho

        etiquetaTituloD = Label(self.frameDerecho, text="Ticket de compra", **label_style)
        etiquetaTituloD.grid(row=0, column=0, pady=3, columnspan=2)

        self.etiquetaMostrarCliente = Label(self.frameDerecho, text="Cliente:  ", **label_style)
        self.etiquetaMostrarCliente.grid(row=1, column=0, sticky="w", padx=5)
        
        self.etiquetaMostrarBarbero = Label(self.frameDerecho, text="Barbero: ", **label_style)
        self.etiquetaMostrarBarbero.grid(row=1, column=1, padx=5)

        self.etiquetaIdVenta = Label(self.frameDerecho, text="ID Venta: ", **label_style)
        self.etiquetaIdVenta.grid(row=2, column=0, sticky="w", padx=10)
        
        columnasTabla = ("Item", "Cantidad", "Precio/U", "Subtotal")
        self.tablaResumenVenta = ttk.Treeview(self.frameDerecho, columns=columnasTabla, height=9, show="headings")
        self.tablaResumenVenta.grid(row=3, column=0, pady=5, padx=3, columnspan=2)

        self.tablaResumenVenta.column("Item", width=140)
        self.tablaResumenVenta.heading("Item", text="Item")

        for col in columnasTabla:
            if(col != "Item"):
                self.tablaResumenVenta.column(col, width=75)
                self.tablaResumenVenta.heading(col, text= col)

        #Componentes del Frame del Total
        
        frameTotal = Frame(self.frameDerecho, width=370, height=160, bg="#333333", # Gris oscuro para el fondo del calendario/tabla
                                relief="flat", bd=0, highlightbackground="#555555", highlightthickness=1)
        frameTotal.grid(row=4, column=0, padx=5, pady=3, columnspan=2)
        frameTotal.grid_propagate(False)

        fuente = ("Arial", 11)
        etiquetaSubtotal = Label(frameTotal, text="Subtotal: ", **label_style)
        etiquetaSubtotal.grid(row=0, column=0, pady=5, sticky="w", padx=10)

        self.etiquetaPSubtotal = Label(frameTotal, text="$ 0.00", **label_style)
        self.etiquetaPSubtotal.grid(row=0, column=1, pady=5, sticky="e")

        etiquetaDescuento = Label(frameTotal, text="Descuento (%): ", **label_style)
        etiquetaDescuento.grid(row=1, column=0, pady=5, sticky="w", padx=10)

        self.campoDescuento = Entry(frameTotal, width=10, **entry_style)
        self.campoDescuento.grid(row=1, column=1, pady=5, padx=5, sticky="e")
        self.campoDescuento.bind("<KeyRelease>", self.aplicarDescuento)

        etiquetaTotal = Label(frameTotal, text="Total a pagar: ", **label_style)
        etiquetaTotal.grid(row=2, column=0, pady=5, sticky="w", padx=10)

        self.etiquetaPTotal = Label(frameTotal, text="$ 0.00", **label_style)
        self.etiquetaPTotal.grid(row=2, column=1, sticky="e")

        etiquetaMetodo = Label(frameTotal, text="Método de pago: ", **label_style)
        etiquetaMetodo.grid(row=3, column=0, padx=5, pady=5)
        self.comboMetodoPago = ttk.Combobox(frameTotal, values=("Efectivo", "Tarjeta", "Transferencia"), state="readonly", width=20)
        self.comboMetodoPago.grid(row=3, column=1, padx=10, pady=5)


        self.botonEliminarItem = Button(frameTotal, text="Eliminar Item", **button_style)
        self.botonEliminarItem.grid(row=4, column=0, columnspan=1, sticky="w", padx=10)

        self.botonFinalizarV = Button(frameTotal, text="Finalizar Venta", command=lambda: self.finalizarVenta(), **button_style)
        self.botonFinalizarV.grid(row=4, column=1, columnspan=1, sticky="w", padx=10)

    def llenarTablaServicios(self):
        tuplaServicios = self.controlador.consultaServiciosVenta() 

        for i in tuplaServicios:
            tuplaNueva = (i[1], i[2])
            self.tablaServicios.insert("", "end", text = i[0], values=tuplaNueva)

    def llenarTablaProductos(self):
        tuplaProductos = self.controlador.consultaProductos() 

        for i in tuplaProductos:
            tuplaNueva = (i[1], i[2])
            self.tablaProductos.insert("", "end", text = i[0], values=tuplaNueva)
    
    def limpiarTabla(self):
        self.tablaResumenVenta.delete(*self.tablaResumenVenta.get_children())

    def seleccionServicios(self, event):
        servicioSeleccionado = self.tablaServicios.selection()
        
        #Se le asigna un if para verificar que la tupla que se devuelve no está vacia
        #Se hace de esta manera por que al eliminar todos los elementos de la tabla se genera de nuevo el evento
        if servicioSeleccionado:
        
            self.idServicio = self.tablaServicios.item(servicioSeleccionado, "text")
            valoresServicio = self.tablaServicios.item(servicioSeleccionado, "values")
            self.tuplaServicioSeleccionado = (valoresServicio[0], 1, valoresServicio[1], valoresServicio[1] * 1) #El valor 1 es el precio
            self.precioServicio = self.tuplaServicioSeleccionado[3]


    def seleccionProductos(self, evento):
        productoSeleccionado = self.tablaProductos.selection()
        
        #Se le asigna un if para verificar que la tupla que se devuelve no está vacia
        #Se hace de esta manera por que al eliminar todos los elementos de la tabla se genera de nuevo el evento
        if productoSeleccionado:
        
            self.idProducto = self.tablaProductos.item(productoSeleccionado, "text")
            valoresProducto = self.tablaProductos.item(productoSeleccionado, "values")
            self.nombreProducto = valoresProducto[0]
            self.precioProducto = valoresProducto[1]
    
    def agregarItemsTabla(self, boton):
        
        if (boton == 1):
            #tuplaServicio = self.seleccionServicios    
            fecha = datetime.datetime.now()
            cadenaFecha = fecha.strftime('%Y-%m-%d %H:%M')
            #print(self.tuplaServicioSeleccionado)
            self.tablaResumenVenta.insert("", "end", values=self.tuplaServicioSeleccionado)
            #print(f"El id es {self.idServicio}")

            tuplaServicioRealizado = (cadenaFecha, self.idTicket, self.idServicio, self.indiceBarbero)
            self.controlador.insertarServicioRealizado(tuplaServicioRealizado)

            self.subtotal += int(self.precioServicio)

            self.etiquetaPSubtotal.config(text=str("$ "+str(self.subtotal)))

            self.tablaServicios.selection_remove(*self.tablaServicios.get_children())

        if(boton == 2):
            cantidad = askinteger("Cantidad", "Ingrese una cantidad: ")
            tuplaProductosTabla = (self.nombreProducto, cantidad, self.precioProducto, cantidad*int(self.precioProducto))
            tuplaProductosQuery = (cantidad, int(self.precioProducto), cantidad*int(self.precioProducto), self.idTicket, self.idProducto)
            self.controlador.insertarDProducto(tuplaProductosQuery)

            self.tablaResumenVenta.insert("", "end", values = tuplaProductosTabla)

            self.subtotal += int(tuplaProductosTabla[3])
            self.etiquetaPSubtotal.config(text="$ "+str(self.subtotal))

            self.tablaProductos.selection_remove(*self.tablaProductos.get_children())

    def iniciarVenta(self):
        self.idTicket = self.controlador.iniciarVenta(self.campoCliente.get())
        self.etiquetaMostrarCliente.config(text="Cliente: "+self.campoCliente.get())
        self.etiquetaIdVenta.config(text="Venta: "+str(self.idTicket))
        
        self.indiceBarbero = self.comboBarbero.current() + 1
        #print(f"el Id del barbero es {self.indiceBarbero}")
        self.etiquetaMostrarBarbero.config(text="Barbero: "+self.comboBarbero.get())

        self.subtotal = 0

        self.botonIniciarVenta.config(state= "disabled")
        tk.messagebox.showinfo("Nueva venta", "Has iniciado una nueva venta.")

    def llenarBarberos(self):
        tuplaBarberos = self.controlador.obtenerBarberos()
        listaNombreBarberos = list()

        for i in tuplaBarberos:
            cadenaBarberos = str(i[0])+" - "+i[1]+" "+i[2]
            listaNombreBarberos.append(cadenaBarberos)

        #print(listaNombreBarberos)
        self.comboBarbero.config(values=listaNombreBarberos)

    def aplicarDescuento(self, event):
        self.descuento = int(self.campoDescuento.get())
        self.totalVenta = self.subtotal - (self.subtotal * (self.descuento / 100))

        self.etiquetaPTotal.config(text="$ "+str(self.totalVenta))

    def finalizarVenta(self):
        datosFaltantes = (self.totalVenta, self.comboMetodoPago.get(), self.descuento, self.subtotal, self.idTicket)
        print(datosFaltantes)
        self.controlador.finalizarVenta(datosFaltantes)

        self.subtotal = 0
        self.limpiarWidgets()

        tk.messagebox.showinfo("Venta finalizada", "Venta concluida correctamente")
        

    def limpiarWidgets(self):
        self.tablaResumenVenta.delete(*self.tablaResumenVenta.get_children())
        self.campoCliente.delete(0, END)
        self.botonIniciarVenta.config(state= "normal")
        self.comboBarbero.set("")
        self.etiquetaIdVenta.config(text="Venta: ")
        self.etiquetaMostrarBarbero.config(text="Barbero: ")
        self.etiquetaMostrarCliente.config(text="Cliente: ")
        self.etiquetaPSubtotal.config(text="$ 0.00")
        self.etiquetaPTotal.config(text="$ 0.00")
        self.campoDescuento.delete(0, END)
        self.comboMetodoPago.set("")