from datetime import date

class Persona():
    def __init__(self, id, nombre, apellido, telefono, fechaNacimiento):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.fechaNacimiento = fechaNacimiento


class Cliente(Persona):
    def __init__(self, id, nombre, apellido, telefono, fechaNacimiento, numeroVisitas):
        super().__init__(id, nombre, apellido, telefono, fechaNacimiento)
        self.numeroVisitas = numeroVisitas

class Empleado(Persona):
    def __init__(self, id, nombre, apellido, telefono, fechaNacimiento, apellidoMaterno, direccion, fechaContratacion, estatus, privilegios):
        super().__init__(id, nombre, apellido, telefono, fechaNacimiento)
        self.apellidoMaterno = apellidoMaterno
        self.direccion = direccion
        self.fechaContratacion = fechaContratacion
        self.estatus = estatus
        self.privilegios = privilegios

class Barbero(Empleado):
    def __init__(self, id, nombre, apellido, telefono, fechaNacimiento, apellidoMaterno, direccion, 
                 fechaContratacion, estatus, privilegios, especialidad, calificacion, idBarbero):
        super().__init__(id, nombre, apellido, telefono, fechaNacimiento, apellidoMaterno, direccion,
                          fechaContratacion, estatus, privilegios)
        self.especialidad = especialidad
        self.calificacion = calificacion
        self.idBarbero = idBarbero

class Recepcionista(Empleado):
    def __init__(self, id, nombre, apellido, telefono, fechaNacimiento, 
                 apellidoMaterno, direccion, fechaContratacion, estatus, privilegios, idRecepcionista, usuario, password):
        super().__init__(id, nombre, apellido, telefono, fechaNacimiento,
                          apellidoMaterno, direccion, fechaContratacion, estatus, privilegios)
        self.idRecepcionista = idRecepcionista
        self.usuario = usuario
        self.password = password

class Cita():
    def __init__(self, idCita, fecha, hora, estatus, comentario, idCliente, idBarbero):
        self.idCita = idCita
        self.fecha = fecha
        self.hora = hora
        self.estatus = estatus
        self.comentario = comentario
        self.idCliente = idCliente
        self.idBarbero = idBarbero

class Producto():
    def __init__(self, idProducto, nombre, descripcion, costo, cantidad):
        self.idProducto = idProducto
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo = costo
        self.cantidad = cantidad

class Servicio():
    def __init__(self, idServicio, nombre, descripcion, costo, duracion, estatus):
        self.idServicio = idServicio
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo = costo
        self.duracion = duracion
        self.estatus = estatus

class Ticket():
    def __init__(self, idTicket, idCliente, fechaVenta, totalVenta, metodoPago, idCita):
        self.idTicket = idTicket
        self.idCliente= idCliente
        self.fechaVenta = fechaVenta
        self.totalVenta = totalVenta
        self.metodoPago = metodoPago
        self.idCita = idCita
"""barberoNuevo = Barbero(2, "Cristian", "Castro", "556964", date(2002, 10, 5), "López", "Cerrada del canal", date.today(), "Activo", 1, "Fade", 10, 1)
"print(f"El empleado {barberoNuevo.id} es un barbero con una calificacion del barbero es: {barberoNuevo.calificacion} y su id de Barbero es: {barberoNuevo.idBarbero}")
   """     

     
        