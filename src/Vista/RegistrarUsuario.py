import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from Modelo.Clases import Empleado
import datetime

class VRegistrarUsuario(tk.Frame):
    def __init__(self, master, controlador):
            super().__init__(master)
            self.pack(fill="both", expand=True)
            self.master = master
            self.controlador =  controlador
            self.master.title("Registrar Usuario")
            self.master.geometry("450x650") # Aumentamos un poco el tamaño para el combobox
            #self.master.resizable(False, False)
            self.master.eval('tk::PlaceWindow . center')

            self.iniciarBarraMenu()

            # --- Estilos personalizados para el Login (basados en tu ejemplo) ---
            self.style = ttk.Style()
            self.style.theme_use('clam') # Seguimos usando clam como base

            # Colores y fuentes base de tu ejemplo
            self.bg_dark = "#333333" # Fondo del frame principal
            self.border_color = "#555555"
            self.text_light = "#E0E0E0" # Color del texto claro
            self.entry_bg = "#444444" # Fondo de los Entry
            self.accent_blue = "#4A90E2" # Azul vibrante para botones y highlight
            self.active_blue = "#357ABD" # Azul más oscuro para activebackground

            # Estilo para el Frame principal del login
            self.style.configure('Login.TFrame', 
                                background=self.bg_dark,
                                relief='flat',
                                bordercolor=self.border_color, # Se aplica si el tema lo soporta bien
                                borderwidth=1) # Añadido para que el highlight funcione sobre el frame

            # Estilo para los Labels
            self.style.configure('Login.TLabel', 
                                background=self.bg_dark, 
                                foreground=self.text_light, 
                                font=("Segoe UI", 9, "bold")) # Un poco más grande para mejor legibilidad

            # Estilo para el Título del Login
            self.style.configure('LoginHeader.TLabel', 
                                background=self.bg_dark, 
                                foreground=self.text_light, 
                                font=("Segoe UI", 15, "bold"))

            # Estilo para los Entry (ttk.Entry)
            # Nota: ttk.Entry es más limitado en personalización directa de 'bg', 'fg', 'bd', etc.
            # Estas propiedades se controlan principalmente por el tema.
            # Sin embargo, podemos influir en el color del campo con 'fieldbackground' si el tema lo permite,
            # y el highlight sí funciona bien.
            self.style.configure('Login.TEntry', 
                                fieldbackground=self.entry_bg, 
                                foreground=self.text_light,
                                font=("Segoe UI", 9),
                                insertcolor="white") # Cursor blanco
            # Esto mapea el color del borde y el resaltado cuando el Entry está en foco
            self.style.map('Login.TEntry',
                        selectbackground=[('!disabled', self.accent_blue)], # Color de selección
                        selectforeground=[('!disabled', 'white')],
                        focuscolor=[('!disabled', self.accent_blue)])

            # Estilo para los Combobox (ttk.Combobox)
            self.style.configure('Login.TCombobox', 
                                fieldbackground=self.entry_bg, # Fondo del campo de texto
                                foreground=self.text_light,
                                selectbackground=self.accent_blue, # Fondo de la selección en la lista desplegable
                                selectforeground='white',
                                font=("Segoe UI", 9),
                                arrowcolor=self.text_light, # Color de la flecha
                                padding=5) # Padding para que se vea un poco más grande
            self.style.map('Login.TCombobox',
                        fieldbackground=[('readonly', self.entry_bg)], # Asegurarse que sea este color en readonly
                        foreground=[('readonly', self.text_light)],
                        focuscolor=[('!disabled', self.accent_blue)])
            
            # Estilo para los Botones (ttk.Button)
            self.style.configure('LoginButton.TButton', 
                                background=self.accent_blue, 
                                foreground='white', 
                                font=("Segoe UI", 9, "bold"),
                                relief='flat', # Estilo plano
                                padding=(15, 8)) # Padding generoso
            self.style.map('LoginButton.TButton',
                        background=[('active', self.active_blue)], # Color al pasar el mouse/clicar
                        foreground=[('active', 'white')])

            


            # --- Contenedor del Login ---
            self.config(bg="#333333")
            self.pack(expand=True, fill="both", padx=20, pady=20)  # Coloca este frame en root

            # Título del Login
            ttk.Label(self, text="Registrar Usuario", style='LoginHeader.TLabel').pack(pady=(10, 10))

            #Tipo de usuario
            ttk.Label(self, text="Tipo de Usuario:", style='Login.TLabel').pack(anchor="w", padx=50)
            self.tipoUsuario = ttk.Combobox(self, 
                                                values=["Dueño", "Recepcionista", "Barbero"], 
                                                state="readonly", # No permitir escribir
                                                style='Login.TCombobox')
            self.tipoUsuario.pack(pady=5, padx=50, fill="x")
            self.tipoUsuario.set("") # Valor por defecto

            self.tipoUsuario.bind("<<ComboboxSelected>>", self.seleccionCombo)
            
            # Campo de Nombre
            ttk.Label(self, text="Nombre:", style='Login.TLabel').pack(anchor="w", padx=50, pady=(5, 0))
            self.campoNombre = ttk.Entry(self, style='Login.TEntry')
            self.campoNombre.pack(pady=5, padx=50, fill="x")

            # Campo de apellido Paterno
            ttk.Label(self, text="Apellido Paterno: ", style='Login.TLabel').pack(anchor="w", padx=50, pady=(5, 0))
            self.campoApellidoP = ttk.Entry(self, style='Login.TEntry')
            self.campoApellidoP.pack(pady=5, padx=50, fill="x")

            # Campo de apellido Materno
            ttk.Label(self, text="Apellido Materno: ", style='Login.TLabel').pack(anchor="w", padx=50, pady=(5, 0))
            self.campoApellidoM = ttk.Entry(self, style='Login.TEntry')
            self.campoApellidoM.pack(pady=5, padx=50, fill="x")

            # Campo de Fecha de Nacimiento
            ttk.Label(self, text="Fecha de Nacimiento: ", style='Login.TLabel').pack(anchor="w", padx=50, pady=(5, 0))
            self.campoFechaN = ttk.Entry(self, style='Login.TEntry')
            self.campoFechaN.pack(pady=5, padx=50, fill="x")

            # Campo de Telefono
            ttk.Label(self, text="Telefono: ", style='Login.TLabel').pack(anchor="w", padx=50, pady=(5, 0))
            self.campoTelefono = ttk.Entry(self, style='Login.TEntry')
            self.campoTelefono.pack(pady=5, padx=50, fill="x")

            # Campo de Dirección
            ttk.Label(self, text="Direccion: ", style='Login.TLabel').pack(anchor="w", padx=50, pady=(5, 0))
            self.campoDireccion = ttk.Entry(self, style='Login.TEntry')
            self.campoDireccion.pack(pady=5, padx=50, fill="x")
            
            # Campo de Usuario
            ttk.Label(self, text="Usuario:", style='Login.TLabel').pack(anchor="w", padx=50, pady=(5, 0))
            self.campoUser = ttk.Entry(self, style='Login.TEntry')
            self.campoUser.pack(pady=5, padx=50, fill="x")

            # Campo de Contraseña
            ttk.Label(self, text="Contraseña:", style='Login.TLabel').pack(anchor="w", padx=50, pady=(5, 0))
            self.campoContraseña = ttk.Entry(self, show="*", style='Login.TEntry')
            self.campoContraseña.pack(pady=5, padx=50, fill="x")

            # Botón de Iniciar Sesión
            ttk.Button(self, text="Registrar Usuario",style='LoginButton.TButton', command=lambda: self.registrarBarbero()).pack(pady=10)#

            
    def iniciarBarraMenu(self):
        barraMenuP = Menu(self.master, bg="#34495E", fg="#ECF0F1", 
                    activebackground="#4E6D8F", activeforeground="#FFFFFF",
                    font=("Segoe UI", 10))
    
        self.master.config(menu= barraMenuP)
        menuArchivo = Menu(barraMenuP,  tearoff=0, bg="#333333", fg="#FFFFFF", 
                            activebackground="#555555", activeforeground="#FFFFFF")
        menuArchivo.add_command(label= "Menu Principal", command= lambda: self.cambiarVentana())

        barraMenuP.add_cascade(label="Opciones", menu=menuArchivo)


    def cambiarVentana(self):
        self.controlador.mostrar_principal(2)


    def seleccionCombo(self, event):
          tipoSeleccionado = self.tipoUsuario.get()

          if tipoSeleccionado:
                if tipoSeleccionado == "Barbero":
                    self.campoUser.config(state="disabled")
                    self.campoContraseña.config(state="disabled")
                
                else: 
                    self.campoUser.config(state="normal")
                    self.campoContraseña.config(state="normal")
                     

    def obtenerDatosBarbero(self, tipoUsuario):
        nombre = self.campoNombre.get()
        apellidoPaterno = self.campoApellidoP.get()
        apellidoMaterno = self.campoApellidoM.get()
        fechaNacimiento = self.campoFechaN.get()
        telefono = self.campoTelefono.get()
        direccion = self.campoDireccion.get()
        fechaContratacion = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        estatus = "activo"
        
        
        if tipoUsuario == "Barbero":
            idPrivilegio = 1
            empleado = Empleado(None, nombre, apellidoPaterno, apellidoMaterno, fechaNacimiento, telefono, direccion, fechaContratacion, 
                                estatus, idPrivilegio, None, None)
            
        else:
            usuario = self.campoUser.get()
            contra = self.campoContraseña.get()
            
            if tipoUsuario == "Recepcionista":
                idPrivilegio = 3
            elif tipoUsuario == "Dueño":
                idPrivilegio = 2

            empleado = Empleado(None, nombre, apellidoPaterno, apellidoMaterno, fechaNacimiento, telefono, direccion, fechaContratacion, 
                                estatus, idPrivilegio, usuario, contra)
        
        
        return empleado
    
    def registrarBarbero(self):
        
        if self.tipoUsuario.get() == "Barbero":
            self.controlador.registrarBarbero(self.obtenerDatosBarbero("Barbero"))
            self.limpiarCampos()
        elif self.tipoUsuario.get() == "Recepcionista":
            self.controlador.registrarUsuario(self.obtenerDatosBarbero("Recepcionista"))
            self.limpiarCampos()
        else:
            self.controlador.registrarUsuario(self.obtenerDatosBarbero("Dueño"))
            self.limpiarCampos()

    def limpiarCampos(self):
        self.campoNombre.delete(0, END)
        self.campoApellidoP.delete(0, END)
        self.campoApellidoM.delete(0, END)
        self.campoFechaN.delete(0, END)
        self.campoTelefono.delete(0, END)
        self.campoDireccion.delete(0, END)
        self.campoUser.delete(0, END)
        self.campoContraseña.delete(0, END)