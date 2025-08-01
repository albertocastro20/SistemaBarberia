#Se importan todas las librerias que utilizaremos
#Librerias de Diseño
import tkinter as tk #Libreria básica
from tkinter import * 
from tkinter import ttk #Libreria con nuevow wg
from tkcalendar import Calendar #Calendario

#Librerias del Modelo
from Modelo.Conexion import *
from Modelo.Clases import *

#Librerias de Vista
from Vista.VistaBarberos import BarberosFrame
from Vista.VistaCitas import CitasFrame
from Vista.VistaClientes import ClientesFrame
from Vista.VistaServicios import ServiciosFrame
from Vista.VentanaVentas import VentasFrame
from Vista.RegistrarUsuario import VRegistrarUsuario

#Librerias del Controlador
#from Controlador.ControladorMVC import *

#Librerias de Trabajo en la clase
import datetime

#Frame principal 650x460

class BarberiaPrincipal(tk.Frame):

    def __init__(self, parent, controlador_recibido, sesion):
        super().__init__(parent)
        self.parent = parent
        self.controlador_recibido = controlador_recibido
        self.sesion = sesion
        self.parent.title("Barberia")
        self.parent.geometry("900x600")
        self.parent.config(bg="#1A1A1A") # Fondo oscuro para un look moderno
        self.parent.resizable(False, False)
        #self.master.eval('tk::PlaceWindow . center')

        self.framesSeccion = {}
        self.active_button = None
    
        self.iniciarWidgets()
        #self.iniciarBarraMenu()

        self.mostrarFrame("Citas")

        #self.conexion = Conexion("root", "Cris8426")


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
        for F in (CitasFrame, ClientesFrame, BarberosFrame, VentasFrame, ServiciosFrame):
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
        self.botonVentas = create_sidebar_button(self.frameBotones, "  VENTAS", lambda: activate_button(self.botonVentas, "Ventas"), 5)

        self.botonInventario.config(state= "disabled")

        #Desahibilta los botones dependiendo el usuario que inicio la sesión
        if (self.sesion !=2):
            self.botonServicios.config(state="disabled")
            self.botonBarberos.config(state="disabled")



    def iniciarBarraMenu(self):
        barraMenuP = Menu(self.parent, bg="#34495E", fg="#ECF0F1", 
                       activebackground="#4E6D8F", activeforeground="#FFFFFF",
                       font=("Segoe UI", 10))
        
        self.parent.config(menu= barraMenuP)
        menuArchivo = Menu(barraMenuP,  tearoff=0, bg="#333333", fg="#FFFFFF", 
                         activebackground="#555555", activeforeground="#FFFFFF")
        menuArchivo.add_command(label= "Establecer conexion", command= lambda: self.conexion.conectar())
        
        if (self.sesion == 2):
            menuArchivo.add_command(label= "Registrar Usuario", command= lambda:self.abrirRegistrarUsuario())

        menuArchivo.add_command(label= "Cambiar de usuario")
        menuArchivo.add_command(label= "Cerrar Sesion")
        menuArchivo.add_command(label= "Salir de la Aplicación", command= lambda: self.parent.destroy())
        barraMenuP.add_cascade(label="Inicio", menu=menuArchivo)


        """menuVentanas = Menu(barraMenuP, tearoff=0)
        menuVentanas.add_command(label= "Ventana Principal")
        menuVentanas.add_command(label= "Gestion de citas")
        menuVentanas.add_command(label= "Productos")
        menuVentanas.add_command(label= "Clientes")
        menuVentanas.add_command(label= "Servicios")
        menuVentanas.add_command(label= "Barberos")
        barraMenuP.add_cascade(label="Navegación", menu=menuVentanas)"""


        self.parent.config(menu=barraMenuP)

    def abrirRegistrarUsuario(self):
        # Crea la ventana principal de la aplicación        
        self.master.destroy()
        main_root = tk.Tk()
        app = VRegistrarUsuario(main_root, self.controlador_recibido)
        main_root.mainloop()
