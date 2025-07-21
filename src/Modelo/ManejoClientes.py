from Modelo.Conexion import *
from Modelo.Clases import Cliente

class QuerysCliente():
    def __init__(self, conexion):
        self.conexion = conexion
        

    def insertarClientes(self, cliente):
        

        #Se recibe un cliente y se contruye una cadena que será el query que usaremos
        qInsertarCliente = """
        INSERT INTO cliente (nombre, apellidoPaterno, numero, fechaNacimiento)
        values (%s, %s, %s, %s)
        """

        #En esta tupla acomodamos los valores recibidos y que queremos insertar
        tuplaCliente = (cliente.nombre, cliente.apellido, cliente.telefono, cliente.fechaNacimiento)

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qInsertarCliente, tuplaCliente)
                cone.commit()
                print("Registro exitoso")
                
            
            except Error as e:
                print(f"Error: {e}")

        

    def actualizarCliente(self, cliente):
        #Se recibe al objeto de Cliente que viene de los campos de texto
        
        #altualizaremos la cadena del query dependiendo de cuales valores ya están iguales y cuales no

        #Creamos una tupla en la que vendrán los elementos de cliente acomodados
        clienteVentana = (cliente.id, cliente.nombre, cliente.apellido, cliente.telefono, cliente.fechaNacimiento, cliente.numeroVisitas)

        #Creamos una tupla que recibirá lo que retorne la función de contruir, le pasaremos de argumento la tupla anterior y el método para 
        # buscar a un cliente en específico
        tuplaRecibida = self.construirActualizar(clienteVentana, self.consultarCliente(cliente))

        #En base a la cadena recibida la concatenamos a la otra parte de nuestro query
        qActualizarCliente = "UPDATE Cliente SET"+tuplaRecibida[0]+" WHERE idCliente = %s"
        
        #Creamos una nueva tupla en la que vienen los valores que se van a cambiar
        tuplaValores = tuple(tuplaRecibida[1])

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qActualizarCliente, tuplaValores)
                cone.commit()
                print("Actualización realizada")
                
            
            except Error as e:
                print(f"Error: {e}")

        

    def construirActualizar(self, tuplaVentana, tuplaBD):
        
        #Creamos una cadena vacia
        cadenaquery = ""


        #Creamos una lista vacia
        listaValores = []

        #Accedemos a los valores de la tupla(Solo será un objeto cliente siempre)
        for clientitoBD in tuplaBD:

            #Evaluaremos si son iguales los campos recibidos de la BD con la de los Entrys
            if(tuplaVentana[1] != clientitoBD[1]):
                cadenaquery = cadenaquery+" nombre = %s," #Si son diferentes, se agrega una parte de la cadena
                listaValores.append(tuplaVentana[1]) #Y se agregará el nuevo elemento a una lista

            if(tuplaVentana[2] != clientitoBD[2]):
                cadenaquery = cadenaquery+" apellidoPaterno = %s,"
                listaValores.append(tuplaVentana[2])

            if(tuplaVentana[3] != clientitoBD[3]):
                cadenaquery = cadenaquery+" numero = %s,"
                listaValores.append(tuplaVentana[3])

            
            fechaRecibida = clientitoBD[4].strftime('%Y-%m-%d') #Como se recibe un objeto de date, le damos formato para que se convierta en str

            if(tuplaVentana[4] != fechaRecibida):
                cadenaquery = cadenaquery+" fechaNacimiento = %s,"
                listaValores.append(tuplaVentana[4])

        cadenaquery = cadenaquery[:-1] #De nuestra cadena final, le quitamos el ultimo valor que siempre será una ,

        listaValores.append(tuplaVentana[0]) #Se le agrega al final el valor del id

        tuplaRetornos = (cadenaquery, listaValores) #Almacenamos en una tupla la cadena creada y la lista de valores

        return tuplaRetornos
        

    def consultarCliente(self, cliente):
        #valoresCliente =  (cliente.nombre, cliente.apellido, cliente.telefono, cliente.fechaNacimiento, cliente.id)
        qConsultaClienteId = """SELECT * FROM Cliente 
        WHERE idCliente = %s"""
        idCliente = (cliente.id,)
        #tuplaRecibida = ()

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qConsultaClienteId, idCliente)
                tuplaRecibida = cursor.fetchall()
            except Error as e:
                print(e)
        
        return tuplaRecibida
        

    def consultaGeneral(self):
        qConsultaClienteId = """SELECT * FROM Cliente"""

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qConsultaClienteId)
                tuplaGeneral = cursor.fetchall()
            except Error as e:
                print(e)

        return tuplaGeneral
