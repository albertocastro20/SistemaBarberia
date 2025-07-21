create database barberia;

--Creaciones de tablas

CREATE TABLE Catalogo_Servicios(
idServicio int not null auto_increment,
nombre varchar(70),
descripcion text,
precio decimal,
duracion int,
estatus boolean,
primary key(idServicio)
);

CREATE TABLE Cliente(
idCliente int not null auto_increment,
nombre varchar(50),
apellidoPaterno varchar(50),
numero varchar (10),
fechaNacimiento varchar(50),
numeroVisitas int,
primary key(idCliente)
);


CREATE TABLE Turno(
idTurno int not null auto_increment,
nombre varchar(20),
hora_inicio time,
hora_final time, 
primary key(idTurno)
);

CREATE TABLE Empleado(
idEmpleado int not null auto_increment,
nombre varchar(30),
apellido_paterno varchar(30),
apellido_materno varchar(30),
fecha_nacimiento date,
telefono varchar(10),
direccion varchar(50),
fecha_contratacion date,
estatus varchar(25),
idPrivilegio int,
idHorario int
primary key(idEmpleado),
foreign key(idPrivilegio) references Privilegio(idPrivilegio)
foreign key(idHorario) references Horario_Laboral(idHorario)
);

CREATE TABLE Privilegio(
idPrivilegio int not null auto_increment,
nombre varchar (20),
primary key(idPrivilegio)
);

CREATE TABLE Producto(
idProducto int not null auto_increment,
nombre varchar(70),
descripcion text,
precio decimal,
cantidad int,
primary key(idProducto)
);

CREATE TABLE Barbero(
idBarbero int not null auto_increment,
especialidad varchar(30),
calificación int,
idEmpleado int,
primary key(idBarbero),
foreign key(idEmpleado) references Empleado(idEmpleado)
ON Delete CASCADE ON Update CASCADE 
);

CREATE TABLE Recepcionista(
idRecepcionista int not null auto_increment,
usuario varchar(30),
contrasenia varchar(30),
idEmpleado int,
primary key(idRecepcionista),
foreign key(idEmpleado) references Empleado(idEmpleado)
ON Delete CASCADE ON Update CASCADE 
);

CREATE TABLE Duenio(
idDuenio int not null auto_increment,
usuario varchar(30),
contrasenia varchar(30),
idEmpleado int,
primary key(idDuenio),
foreign key(idEmpleado) references Empleado(idEmpleado)
ON Delete CASCADE ON Update CASCADE 
);

CREATE TABLE Horario_Laboral(
idHorario int not null auto_increment,
diaDescanso varchar(15),
duracion int,
idTurno int,
primary key(idHorario),
foreign key(idTurno) references Turno(idTurno)
);

CREATE TABLE Cita(
idCita int not null auto_increment,
fecha date,
hora time,
estatus varchar(15),
comentarios text,
idCliente int,
idBarbero int,
primary key(idCita),
foreign key(idCliente) references Cliente(idCliente) ON Delete CASCADE ON Update CASCADE,
foreign key(idBarbero) references Barbero(idBarbero) ON Delete CASCADE ON Update CASCADE
);


CREATE TABLE Ticket(
idTicket int not null auto_increment,
fecha_hora_venta datetime,
total_venta float,
metodo_pago varchar(20),
idCliente int,
idCita int default null, 
subtotal float,
primary key(idTicket),
foreign key(idCliente) references Cliente(idCliente),
foreign key(idCita) references Cita(idCita) ON Delete SET null
);

CREATE TABLE Detalle_Venta_Producto(
idDVP int not null auto_increment,
cantidad int,
precio_unitario float,
subtotal float,
idTicket int,
idProducto int,
primary key(idDVP),
foreign key(idTicket) references Ticket(idTicket),
foreign key(idProducto) references Producto(idProducto)
);

CREATE TABLE Servicio_Realizado(
idServicio_Realizado int not null auto_increment,
fecha_hora_inicio datetime,
fecha_hora_final datetime,
idTicket int,
idServicio int,
idBarbero int,
primary key(idServicio_Realizado),
foreign key(idTicket) references Ticket(idTicket),
foreign key(idServicio) references Catalogo_Servicios(idServicio),
foreign key(idBarbero) references Barbero(idBarbero)
);


/*Restricciones para que no haya clientes y barberos con citas a la misma hora
*/
ALTER TABLE `cita`
ADD CONSTRAINT UQ_Cliente_FechaHora UNIQUE (`fecha`, `hora`, `idCliente`);

ALTER TABLE `cita`
ADD CONSTRAINT UQ_Barbero_FechaHora UNIQUE (`fecha`, `hora`, `idBarbero`);