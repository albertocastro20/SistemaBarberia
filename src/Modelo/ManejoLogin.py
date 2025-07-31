import bcrypt
from Modelo.Conexion import *

class ManejoIniciarSesion():
    def __init__(self, conexion):
        self.conexion = conexion

    def registrar_usuario(self, username, password):
        cone = self.conexion.conectar()
        if cone:
            try:
                cursor = cone.cursor()
                # Generar el hash de la contraseña
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                sql = "INSERT INTO usuarios (username, password_hash, email, rol) VALUES (%s, %s, %s, %s)"
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
                        
                else:
                    print("Usuario no encontrado o inactivo.")
                    
            except Error as err:
                print(f"Error al verificar credenciales: {err}")
                

        print("Si llega")
        print(logueado)
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