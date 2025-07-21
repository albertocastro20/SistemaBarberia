-- Insercion de datos
INSERT INTO producto (
    nombre,
    descripcion,
    precio,
    cantidad
) VALUES
('Cera para Cabello Fuerte', 'Cera de fijación extra fuerte para peinados duraderos.', 150, 50),
('Aceite para Barba Premium', 'Aceite hidratante y suavizante para barba, con aroma a sándalo.', 220, 30),
('Shampoo Anticaída', 'Shampoo especializado para fortalecer el cabello y prevenir la caída.', 180, 40),
('Bálsamo Post-Afeitado', 'Bálsamo calmante y refrescante para después del afeitado.', 130, 60),
('Navaja Clásica', 'Navaja de afeitar de acero inoxidable, ideal para afeitado tradicional.', 350, 20),
('Crema de Afeitar Clásica', 'Crema espumosa para un afeitado suave y sin irritaciones.', 100, 75),
('Tijeras de Corte Profesional', 'Tijeras de alta calidad para cortes de cabello precisos.', 500, 15),
('Peine de Barba de Madera', 'Peine de madera natural para desenredar y estilizar la barba.', 80, 55),
('Loción Capilar Tonificante', 'Loción que estimula el cuero cabelludo y fortalece el cabello.', 190, 35),
('Kit de Cuidado de Barba', 'Incluye aceite, bálsamo y peine para el cuidado completo de la barba.', 450, 25);

INSERT INTO empleado (
    nombre,
    apellido_paterno,
    apellido_materno,
    fecha_nacimiento,
    telefono,
    direccion,
    fecha_contratacion,
    estatus,
    idPrivilegio,
    idHorario
) VALUES
('Juan', 'Perez', 'Garcia', '1990-05-15', '5512345678', 'Calle Falsa 123', '2020-01-10', 'Activo', 1, 1),
('Maria', 'Lopez', 'Martinez', '1988-11-22', '5587654321', 'Avenida Siempre Viva 45', '2019-03-20', 'Activo', 1, 2),
('Carlos', 'Gonzalez', 'Sanchez', '1992-03-01', '5511223344', 'Blvd. de los Sueños 67', '2021-07-05', 'Activo', 1, 3),
('Ana', 'Rodriguez', 'Fernandez', '1995-07-30', '5599887766', 'Paseo de la Reforma 89', '2022-01-15', 'Activo', 3, 4),
('Luis', 'Hernandez', 'Diaz', '1985-01-20', '5544556677', 'Via Lactea 101', '2018-09-01', 'Activo', 2, 5),
('Sofia', 'Martinez', 'Ruiz', '1993-09-10', '5533221100', 'Calle del Sol 202', '2020-11-25', 'Activo', 1, 6),
('Diego', 'Ramirez', 'Torres', '1991-04-03', '5577889900', 'Avenida Luna 303', '2021-04-12', 'Activo', 1, 7),
('Valeria', 'Flores', 'Vazquez', '1994-02-18', '5566554433', 'Calle Estrella 404', '2022-09-01', 'Activo', 2, 8),
('Pedro', 'Morales', 'Jimenez', '1987-08-07', '5522334455', 'Camino Real 505', '2019-06-10', 'Activo', 1, 9),
('Laura', 'Ortiz', 'Castillo', '1996-12-05', '5500998877', 'Privada del Bosque 606', '2023-02-20', 'Activo', 1, 10);



INSERT INTO catalogo_servicios (
    nombre,
    descripcion,
    precio,
    duracion,
    estatus
) VALUES
('Corte de Cabello Clásico', 'Corte de cabello para caballero con estilo tradicional.', 200, 30, 1),
('Afeitado Clásico', 'Afeitado con navaja, toallas calientes y productos premium.', 250, 45, 1),
('Arreglo de Barba', 'Diseño y recorte de barba con perfilado y productos especializados.', 150, 20, 1),
('Corte y Barba Completo', 'Paquete de corte de cabello y arreglo de barba.', 320, 60, 1),
('Lavado y Peinado', 'Lavado de cabello y peinado con productos de estilizado.', 80, 15, 1),
('Tratamiento Capilar Hidratante', 'Mascarilla hidratante para cabello seco o dañado.', 180, 25, 1),
('Diseño de Cejas', 'Perfilado y arreglo de cejas para caballero.', 100, 15, 1),
('Masaje Capilar Relajante', 'Masaje en el cuero cabelludo para estimular la circulación.', 120, 20, 1),
('Corte para Niños', 'Corte de cabello para niños menores de 12 años.', 150, 25, 1),
('Coloración de Barba', 'Aplicación de tinte para barba para cubrir canas o cambiar tono.', 300, 50, 1);

INSERT INTO cliente (
    nombre,
    apellidoPaterno,
    numero,
    fechaNacimiento,
    numeroVisitas
) VALUES
('Roberto', 'Gomez', '5511223344', '1985-03-10', 5),
('Miguel', 'Castro', '5533445566', '1978-01-15', 10),
('Andres', 'Morales', '5555667788', '1982-05-05', 7),
('Javier', 'Serrano', '5577889900', '1975-02-28', 12),
('Ricardo', 'Vargas', '5599001122', '1993-06-01', 6),
('Eduardo', 'Guerrero', '5510203040', '1991-08-14', 2),
('Daniel', 'Herrera', '5532435465', '1979-10-02', 11),
('Jorge', 'Salazar', '5554657687', '1983-07-19', 5),
('Fernando', 'Ruiz', '5544556677', '1990-11-30', 3),
('Carlos', 'Ortega', '5566778899', '1995-09-18', 1),
('Gustavo', 'Reyes', '5588990011', '1988-04-03', 4),
('Alejandro', 'Mendoza', '5500112233', '1980-12-08', 8),
('Sergio', 'Prieto', '5521324354', '1987-03-25', 9),
('Pablo', 'Cruz', '5543546576', '1994-01-07', 3),
('Manuel', 'Diaz', '5522334455', '1992-07-22', 2);
