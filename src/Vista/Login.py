import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar 
import datetime
from Vista.VentanaPrincipal import BarberiaPrincipal

class LoginWindow:
    def __init__(self, master, controlador):
        self.master = master
        self.controlador =  controlador
        self.master.title("Iniciar Sesión - Barbería")
        self.master.geometry("400x400") # Aumentamos un poco el tamaño para el combobox
        self.master.resizable(False, False)
        self.master.eval('tk::PlaceWindow . center')

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
                             font=("Segoe UI", 10, "bold")) # Un poco más grande para mejor legibilidad

        # Estilo para el Título del Login
        self.style.configure('LoginHeader.TLabel', 
                             background=self.bg_dark, 
                             foreground=self.text_light, 
                             font=("Segoe UI", 20, "bold"))

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
                             font=("Segoe UI", 11, "bold"),
                             relief='flat', # Estilo plano
                             padding=(15, 8)) # Padding generoso
        self.style.map('LoginButton.TButton',
                       background=[('active', self.active_blue)], # Color al pasar el mouse/clicar
                       foreground=[('active', 'white')])


        # --- Contenedor del Login ---
        self.login_frame = ttk.Frame(master, style='Login.TFrame') # Aplicamos el estilo al frame
        self.login_frame.pack(expand=True, fill="both", padx=20, pady=20) # Añadimos padding al frame

        # Título del Login
        ttk.Label(self.login_frame, text="Iniciar Sesión", style='LoginHeader.TLabel').pack(pady=(10, 20))
        
        # Campo de Usuario
        ttk.Label(self.login_frame, text="Usuario:", style='Login.TLabel').pack(anchor="w", padx=50, pady=(10, 0))
        self.campoUser = ttk.Entry(self.login_frame, style='Login.TEntry')
        self.campoUser.pack(pady=5, padx=50, fill="x")

        # Campo de Contraseña
        ttk.Label(self.login_frame, text="Contraseña:", style='Login.TLabel').pack(anchor="w", padx=50, pady=(10, 0))
        self.campoContraseña = ttk.Entry(self.login_frame, show="*", style='Login.TEntry')
        self.campoContraseña.pack(pady=5, padx=50, fill="x")

        # Botón de Iniciar Sesión
        ttk.Button(self.login_frame, text="Iniciar Sesión", command=self.check_login, style='LoginButton.TButton').pack(pady=20)

    def check_login(self):
        
        username = self.campoUser.get()
        password = self.campoContraseña.get()
        listaRecibida = self.controlador.comprobarLogueo(username, password)
        

        # Lógica de autenticación de prueba
        
        if listaRecibida[0]:
            self.master.destroy()
            if listaRecibida[1] == 2:
                messagebox.showinfo("Éxito", "Sesión de Dueño iniciada correctamente!")
            else:
                messagebox.showinfo("Éxito", "Iniciaste sesión como Recepcionista!")

            self.open_main_app(listaRecibida[1]) # Llama a la función que abre la app principal

        else:
            messagebox.showerror("Error de Login", "Credenciales incorrectas o tipo de usuario no válido.")

    def open_main_app(self, sesion):
        # Crea la ventana principal de la aplicación        
        main_root = tk.Tk()
        app = BarberiaPrincipal(main_root, self.controlador, sesion)
        main_root.mainloop()

        

# --- Punto de entrada de la aplicación ---

