CREATE SCHEMA ferramas;

USE ferramas;

CREATE TABLE `user` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `mail` varchar(30),
  `rut` varchar(10),
  `nombre` varchar(20),
  `apellido` varchar(20),
  `password` varchar(255),
  `rol` int
);

CREATE TABLE `rol` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `nombreRol` varchar(255)
);

CREATE TABLE `producto` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `nombre` varchar(30),
  `marca` varchar(20),
  `codigo` varchar(20),
  `precio` float,
  `vigente` boolean
);

CREATE TABLE `ventas` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `cliente` int,
  `fecVenta` datetime,
  `valorVenta` float,
  `estadoVenta` varchar(20)
);

CREATE TABLE `detalleVentas` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `venta` int,
  `producto` int,
  `cantidad` int
);

CREATE TABLE `pago` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `venta` int,
  `montoPago` float,
  `token` varchar(64),
  `status` varchar(64),
  `card_detail` varchar(255),
  `transaction_date` datetime
);

CREATE TABLE `despacho` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `estadoDespacho` varchar(20),
  `fecEstado` datetime,
  `venta` int,
  `direccion` varchar(50),
  `comuna` int
);

ALTER TABLE `detalleVentas` ADD FOREIGN KEY (`producto`) REFERENCES `producto` (`id`);

ALTER TABLE `detalleVentas` ADD FOREIGN KEY (`venta`) REFERENCES `ventas` (`id`);

ALTER TABLE `ventas` ADD FOREIGN KEY (`cliente`) REFERENCES `user` (`id`);

ALTER TABLE `pago` ADD FOREIGN KEY (`venta`) REFERENCES `ventas` (`id`);

ALTER TABLE `despacho` ADD FOREIGN KEY (`venta`) REFERENCES `ventas` (`id`);

ALTER TABLE `user` ADD FOREIGN KEY (`rol`) REFERENCES `rol` (`id`);
