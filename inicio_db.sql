CREATE TABLE `articulos` (
  `art_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `prov_id` int(16) UNSIGNED NOT NULL,
  `art_cod_barras` varchar(20) NULL UNIQUE KEY,
  `art_descripcion` varchar(30) NOT NULL,
  `art_marca` varchar(20) NOT NULL,
  `art_agrupacion` varchar(20) NOT NULL,
  `art_stock_minimo` int(8) NOT NULL,
  `art_stock_ideal` int(8) NOT NULL,
  `art_activo` tinyint (1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `operarios` (
  `ope_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `ope_legajo` int(16) NOT NULL,
  `ope_nombre` varchar(20) NOT NULL,
  `ope_apellido` varchar(20) NOT NULL,
  `ope_puesto` varchar(20) NOT NULL,
  `ope_dni` int(13)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `proveedores` (
  `prov_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `prov_nombre` varchar(20) NOT NULL,
  `prov_razon_social` varchar(20) NOT NULL,
  `prov_cuit` varchar(20),
  `prov_direccion` varchar(40),
  `prov_telefono` varchar(20),
  `prov_telefono_dos` varchar(20),
  `prov_email` varchar(30),
  `prov_activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `agrupaciones` (
  `ag_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `ag_nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `destinos` (
  `des_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `des_maquina` varchar(20) NOT NULL,
  `des_descripcion` varchar(20)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `movimientos_ingreso` (
  `movi_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `art_id` int(16) UNSIGNED NOT NULL ,
  `ing_id` int(16) UNSIGNED NOT NULL ,
  `movi_cantidad` int(20) UNSIGNED NOT NULL,
  `movi_costo` int(20)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `movimientos_egreso` (
  `move_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `art_id` int(16) UNSIGNED NOT NULL,
  `eg_id` int(16) UNSIGNED NOT NULL,
  `movi_id` int(16) UNSIGNED NOT NULL,
  `move_cantidad` int(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `ingresos` (
  `ing_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `prov_id` int(16) UNSIGNED NOT NULL,
  `ing_fecha` date NOT NULL  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `egresos` (
  `eg_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `ope_id` int(16) NOT NULL,
  `eg_fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `comprobantes` (
  `comp_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `comp_prefijo` varchar(10) NOT NULL,
  `comp_numero` int(20) NOT NULL,
  `comp_fecha` date NOT NULL,
  `ing_id` int(16) UNSIGNED NOT NULL 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `remitos` (
  `rem_id` int(16) UNSIGNED NOT NULL AUTO_iNCREMENT PRIMARY KEY,
  `rem_prefijo` varchar(10) NOT NULL,
  `rem_numero` int(20) NOT NULL,
  `rem_fecha` date NOT NULL,
  `eg_id` int(16) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;