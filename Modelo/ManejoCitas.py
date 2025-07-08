from Modelo.Conexion import *
from Modelo.Clases import Cita
import datetime


class QuerysCita():
    def __init__(self, conexion):
        self.conexion = conexion
        

    def insertarCita(self, cita):
        
        #Se recibe un cliente y se contruye una cadena que será el query que usaremos
        qInsertarCliente = """
        INSERT INTO cita (fecha, hora, estatus, comentarios, idCliente, idBarbero)
        values (%s, %s, %s, %s, %s, %s)
        """

        #En esta tupla acomodamos los valores recibidos y que queremos insertar
        tuplaCita = (cita.fecha, cita.hora, cita.estatus, cita.comentario, cita.idCliente, cita.idBarbero)

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qInsertarCliente, tuplaCita)
                cone.commit()
                print("Registro exitoso")
                
            
            except Error as e:
                print(f"Error: {e}")

    def actualizarCita(self, cita):
        #Se recibe al objeto de Cliente que viene de los campos de texto
        
        #actualizaremos la cadena del query dependiendo de cuales valores ya están iguales y cuales no

        #Creamos una tupla en la que vendrán los elementos de cliente acomodados
        citaVentana = (cita.idCita, cita.fecha, cita.hora, cita.estatus, cita.comentario, cita.idCliente, cita.idBarbero)

        #Creamos una tupla que recibirá lo que retorne la función de contruir, le pasaremos de argumento la tupla anterior y el método para 
        # buscar a una cita en específico
        tuplaRecibida = self.construirActualizar(citaVentana, self.consultarCita(cita))
        #print(tuplaRecibida)

        #En base a la cadena recibida la concatenamos a la otra parte de nuestro query
        qActualizarCita = "UPDATE Cita SET"+tuplaRecibida[0]+" WHERE idCita = %s"
        
        #Creamos una nueva tupla en la que vienen los valores que se van a cambiar
        tuplaValores = tuple(tuplaRecibida[1])

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qActualizarCita, tuplaValores)
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
        for citaBD in tuplaBD:

            #Evaluaremos si son iguales los campos recibidos de la BD con la de los Entrys

            #Manejamos la fecha recibida
            #fechaRecibida = citaBD[1].strftime('%Y-%m-%d') #Como se recibe un objeto de date, le damos formato para que se convierta en str

            if(tuplaVentana[1] != citaBD[1]):
                cadenaquery = cadenaquery+" fecha = %s," #Si son diferentes, se agrega una parte de la cadena
                listaValores.append(tuplaVentana[1]) #Y se agregará el nuevo elemento a una lista

            #manejamos la hora recibida dandole formato
            horaRecibida = (datetime.datetime.min + citaBD[2]).time()
            horaFormateada = horaRecibida.strftime('%H:%M')

            if(tuplaVentana[2] != horaFormateada):
                cadenaquery = cadenaquery+" hora = %s,"
                listaValores.append(tuplaVentana[2])

            if(tuplaVentana[3] != citaBD[3]):
                cadenaquery = cadenaquery+" estatus = %s,"
                listaValores.append(tuplaVentana[3])

            if(tuplaVentana[4] != citaBD[4]):
                cadenaquery = cadenaquery+" comentarios = %s,"
                listaValores.append(tuplaVentana[4])

            #int porque en los Entrys son cadenas
            if(int(tuplaVentana[5]) != citaBD[5]):
                cadenaquery = cadenaquery+" idCliente = %s,"
                listaValores.append(tuplaVentana[5])

            if(int(tuplaVentana[6]) != citaBD[6]):
                cadenaquery = cadenaquery+" idBarbero = %s,"
                listaValores.append(tuplaVentana[6])

        cadenaquery = cadenaquery[:-1] #De nuestra cadena final, le quitamos el ultimo valor que siempre será una ,

        listaValores.append(tuplaVentana[0]) #Se le agrega al final el valor del id

        tuplaRetornos = (cadenaquery, listaValores) #Almacenamos en una tupla la cadena creada y la lista de valores

        return tuplaRetornos
    
    def consultarCita(self, cita):
        qConsultaCitaId = """SELECT * FROM Cita 
        WHERE idCita = %s"""
        idCita = (cita.idCita,)
        #tuplaRecibida = ()

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qConsultaCitaId, idCita)
                tuplaRecibida = cursor.fetchall()
            except Error as e:
                print(e)
        
        return tuplaRecibida
    
    def mostrarCitas(self, cita):
        qConsultarCitas =  """SELECT idCita, hora, idCliente, idBarbero FROM Cita WHERE fecha = %s
        """

        tuplaCita = (cita.fecha,)

        cone = self.conexion.conectar()

        if cone:
            try:
                cursor = cone.cursor()
                cursor.execute(qConsultarCitas, tuplaCita)
                tuplaRecibida = cursor.fetchall()
            except Error as e:
                print(e)
        
        #print(tuplaRecibida)
        return tuplaRecibida

