import bcrypt
from Modelo.Conexion import *

class ManejoIniciarSesion():
    def __init__(self, conexion):
        self.conexion = conexion

    def registrarBarbero(self, barbero):
        
        #Se recibe un cliente y se contruye una cadena que será el query que usaremos
        qInsertarEmpleadoBarbero = """
        INSERT INTO Empleado (nombre, apellido_paterno, apellido_materno, fecha_nacimiento, telefono, direccion, fecha_contratacion, estatus, idPrivilegio)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        #En esta tupla acomodamos los valores recibidos y que queremos insertar
        tuplaBarbero = (barbero.nombre, barbero.apellido, barbero.apellidoMaterno, barbero.fechaNacimiento, barbero.telefono, 
                        barbero.direccion, barbero.fechaContratacion, barbero.estatus, barbero.privilegios)

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qInsertarEmpleadoBarbero, tuplaBarbero)
                cone.commit()
                print("Registro exitoso")
                
            
            except Error as e:
                print(f"Error: {e}")

    def registrarUsuario(self, empleado):
        #Se recibe un cliente y se contruye una cadena que será el query que usaremos
        qInsertarEmpleadoBarbero = """
        INSERT INTO Empleado (nombre, apellido_paterno, apellido_materno, fecha_nacimiento, telefono, direccion, fecha_contratacion, estatus, idPrivilegio, usuario, password)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        contra = empleado.contra
        hashed_password = bcrypt.hashpw(contra.encode('utf-8'), bcrypt.gensalt())

        #En esta tupla acomodamos los valores recibidos y que queremos insertar
        tuplaEmpleado = (empleado.nombre, empleado.apellido, empleado.apellidoMaterno, empleado.fechaNacimiento, empleado.telefono, 
                        empleado.direccion, empleado.fechaContratacion, empleado.estatus, empleado.privilegios, 
                        empleado.usuario, hashed_password.decode('utf-8'))

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qInsertarEmpleadoBarbero, tuplaEmpleado)
                cone.commit()
                print("Registro exitoso")
                
            
            except Error as e:
                print(f"Error: {e}")

    
    def registrar_usuario(self, username, password):
        cone = self.conexion.conectar()
        if cone:
            try:
                cursor = cone.cursor()
                # Generar el hash de la contraseña
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                sql = "INSERT INTO usuarios (nombre, username, password_hash, email, rol) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (username, hashed_password.decode('utf-8')))
                cone.commit()
                return True
            except Error as err:
                print(f"Error al registrar usuario: {err}")
                return False

    def verificar_credenciales(self, username, password):
        logueado = list()
        cone = self.conexion.conectar()
        if cone:
            try:
                cursor = cone.cursor(dictionary=True) # dictionary=True para obtener resultados como diccionarios
                sql = "SELECT idEmpleado, usuario, password, idPrivilegio FROM empleado WHERE usuario = %s"
                cursor.execute(sql, (username,))
                user = cursor.fetchone()

                if user:
                    # Verificar la contraseña ingresada con el hash almacenado
                    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                        print(f"Login exitoso para el usuario: {user['usuario']}")
                        logueado = [True, user['idPrivilegio']]
                        
                    else:
                        print("Contraseña incorrecta.")
                        logueado = [False , None]
                        
                else:
                    print("Usuario no encontrado o inactivo.")
                    logueado = [False , None]
                    
            except Error as err:
                print(f"Error al verificar credenciales: {err}")
                
        return logueado
            

# Ejemplo de uso:
# usuario_logueado = verificar_credenciales("nuevo_barbero", "miPasswordSeguro123!")
# if usuario_logueado:
#     print(f"¡Bienvenido, {usuario_logueado['username']}! Tu rol es: {usuario_logueado['rol']}")
# else:
#     print("Credenciales inválidas.")

# Ejemplo de uso:
# if registrar_usuario("nuevo_barbero", "miPasswordSeguro123!", "barbero@ejemplo.com", "barbero"):
#     print("Usuario registrado exitosamente.")
# else:
#     print("Fallo el registro del usuario.")