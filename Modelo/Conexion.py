from mysql.connector import *

class Conexion():
    #Clase que permitirá la conexión
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self._conectado = None

    def conectar(self):
        if self._conectado is None or not self._conectado.is_connected():
            try:
                self._conectado = connect(
                    host = "localhost",
                    user = self.user,
                    password = self.password,
                    database = "barberia" 
                    
                )
                print("Conexion establecida")
            except Error as e:
                print(e)
                self._conectado = None
        
        return self._conectado
    
    def cerrarConexion(self):
        if self._conectado is not None and self._conectado.is_connected():
            self._conectado.close()
            self._conectado = None
            print("Conexion cerrada")
    

        