import tkinter as tk
from tkinter import ttk
from tkinter import *

class VentasFrame(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador

        self.iniciarFrames()
        self.iniciarWidgets()
        self.after(3, self.llenarTablaServicios)
        self.after(3, self.llenarTablaProductos)

        #self.llenarTablaServicios()

    def iniciarFrames(self):
        self.frameIzquierdo = Frame(self, width=270, height=460, bg="grey")
        self.frameIzquierdo.grid(row=0, column=0)
        self.frameIzquierdo.grid_propagate(False)

        self.frameDerecho = Frame(self, width=380, height=460)
        self.frameDerecho.grid(row=0, column=1)
        self.frameDerecho.grid_propagate(False)

    def iniciarWidgets(self):
        #Componentes del Frame Izquierdo
        frameTitulo = Frame(self.frameIzquierdo, width=260, height=30, bg="grey")
        frameTitulo.grid(row=0, column=0, padx=5, pady=5)
        frameTitulo.grid_propagate(False)

        etiquetaTitulo = Label(frameTitulo, text="Selección de Ventas", font=("Arial", 14), anchor="center")
        etiquetaTitulo.grid(row=0, column=0, sticky="nsew")
        frameTitulo.grid_columnconfigure(0, weight=1)

        #Frame para el buscador
        frameBuscadorCliente = Frame(self.frameIzquierdo, width=260, height=30)
        frameBuscadorCliente.grid(row=1, column=0, padx=5, pady=5)
        frameBuscadorCliente.grid_propagate(False)

        etiquetaCliente = Label(frameBuscadorCliente, text="Cliente: ", font=("Arial", 10))
        etiquetaCliente.grid(row=0, column=0, pady=2)

        self.campoCliente = Entry(frameBuscadorCliente, font=("Arial", 10))
        self.campoCliente.grid(row=0, column=1, pady=2)

        self.botonBuscarCliente = Button(frameBuscadorCliente, text="Buscar")
        self.botonBuscarCliente.grid(row=0, column=2, padx=(7, 3), pady=2)

        #Frame para el Nootebook
        self.notebookInformacion = ttk.Notebook(self.frameIzquierdo)
        self.notebookInformacion.grid(row=2, column=0)

        #Pestaña de Servicios
        
        frameServicios = Frame(self.notebookInformacion, height=320, width= 250)
        self.notebookInformacion.add(frameServicios, text="Servicios")

        etiquetaInternaServicios = Label(frameServicios, text="Lista de servicios")
        etiquetaInternaServicios.pack(side="top")
        
        columnasServicios = ("Servicio", "Precio")
        self.tablaServicios = ttk.Treeview(frameServicios, columns=columnasServicios, show="headings")
        

        self.tablaServicios.column("Servicio", width=165)
        self.tablaServicios.column("Precio", width=75)

        for col in columnasServicios:
            self.tablaServicios.heading(col, text=col)
        self.tablaServicios.pack(padx=5)


        self.botonAgregarServicio = Button(frameServicios, text="Añadir Servicios")
        self.botonAgregarServicio.pack(padx=15, pady=15, fill="x")


        #Pestaña de Productos

        frameProductos = Frame(self.notebookInformacion, height=320, width= 250)
        self.notebookInformacion.add(frameProductos, text="Productos")

        etiquetaInternaProductos = Label(frameProductos, text="Lista de productos")
        etiquetaInternaProductos.pack(side="top")
        
        columnasProductos = ("Producto", "Precio")
        self.tablaProductos = ttk.Treeview(frameProductos, columns=columnasProductos, show="headings")
        

        self.tablaProductos.column("Producto", width=165)
        self.tablaProductos.column("Precio", width=75)

        for col in columnasProductos:
            self.tablaProductos.heading(col, text=col)
        self.tablaProductos.pack(padx=5)

        self.botonAgregarProducto = Button(frameProductos, text="Añadir Producto")
        self.botonAgregarProducto.pack(padx=15, pady=15, fill="x")

        #Componentes del Frame Derecho

        etiquetaTituloD = Label(self.frameDerecho, text="Ticket de compra", font=("Arial", 12))
        etiquetaTituloD.grid(row=0, column=0, pady=3)
        
        columnasTabla = ("Item", "Cantidad", "Precio/U", "Subtotal")
        self.tablaResumenVenta = ttk.Treeview(self.frameDerecho, columns=columnasTabla, height=10, show="headings")
        self.tablaResumenVenta.grid(row=1, column=0, pady=10, padx=5)

        self.tablaResumenVenta.column("Item", width=140)
        self.tablaResumenVenta.heading("Item", text="Item")

        for col in columnasTabla:
            if(col != "Item"):
                self.tablaResumenVenta.column(col, width=75)
                self.tablaResumenVenta.heading(col, text= col)

        frameTotal = Frame(self.frameDerecho, width=370, height=165, bg="grey")
        frameTotal.grid(row=2, column=0, padx=5)
        frameTotal.grid_propagate(False)

        #Componentes del Frame del Total

        fuente = ("Arial", 11)
        etiquetaSubtotal = Label(frameTotal, text="Subtotal: ", font=fuente)
        etiquetaSubtotal.grid(row=0, column=0, pady=5, sticky="w", padx=10)

        self.etiquetaPSubtotal = Label(frameTotal, text="$ 0.00", font=fuente)
        self.etiquetaPSubtotal.grid(row=0, column=1, pady=5, sticky="e")

        etiquetaDescuento = Label(frameTotal, text="Descuento (%): ", font=fuente)
        etiquetaDescuento.grid(row=1, column=0, pady=5, sticky="w", padx=10)

        self.campoDescuento = Entry(frameTotal, font=fuente, width=10)
        self.campoDescuento.grid(row=1, column=1, pady=5, padx=5, sticky="e")

        etiquetaTotal = Label(frameTotal, text="Total a pagar: ", font=fuente)
        etiquetaTotal.grid(row=2, column=0, pady=5, sticky="w", padx=10)

        self.etiquetaPTotal = Label(frameTotal, text="$ 0.00", font=fuente)
        self.etiquetaPTotal.grid(row=2, column=1, sticky="e")


        self.botonEliminarItem = Button(frameTotal, text="Eliminar Item", font=fuente)
        self.botonEliminarItem.grid(row=3, column=0, columnspan=1, sticky="w", padx=10)

        self.botonFinalizarV = Button(frameTotal, text="Finalizar Venta", font=fuente)
        self.botonFinalizarV.grid(row=4, column=0, columnspan=1, sticky="w", padx=10)

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
        