CREATE TABLE `articulos` (
  `art_ID` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `prov_ID` int(16) UNSIGNED NOT NULL,
  `art_cod_barras` varchar(20) NULL UNIQUE KEY,
  `art_descripcion` varchar(20) NOT NULL,
  `art_marca` varchar(20) NOT NULL,
  `art_agrupacion` varchar(20) NOT NULL,
  `art_stock_minimo` int(8) NOT NULL,
  `art_stock_ideal` int(8) NOT NULL,
  `art_activo` tinyint (1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `operarios` (
  `ope_ID` int(16) UNSIGNED NOT NULL AUTO_INCREMENT,
  `ope_legajo` int(16) NOT NULL,
  `ope_nombre` varchar(20) NOT NULL,
  `ope_apellido` varchar(20) NOT NULL,
  `ope_puesto` varchar(20) NOT NULL,
  `ope_dni` int(13)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `prov_ID` int(16) UNSIGNED NOT NULL AUTO_INCREMENT,
  `prov_nombre` varchar(20) NOT NULL,
  `prov_razonsocial` varchar(20) NOT NULL,
  `prov_cuit` varchar(20),
  `prov_direccion` varchar(40),
  `prov_telefono` varchar(20),
  `prov_telefono_dos` varchar(20),
  `prov_contacto` varchar(20),
  `prov_mail` varchar(30)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `agrupaciones` (
  `ag_ID` int(16) UNSIGNED NOT NULL AUTO_INCREMENT,
  `ag_nombre` varchar(20) NOT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `destino` (
  `des_ID` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `des_maquina` varchar(20) NOT NULL,
  `des_descripcion` varchar(20),
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `stock` (
  `stock_ID` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `art_ID` int(16) UNSIGNED NOT NULL ,
  `ing_ID` int(16) UNSIGNED NOT NULL ,
  -- `stock_fecha` date(20) NOT NULL, --
  `cantidad` int(20) UNSIGNED NOT NULL,
  `stock_costo` int(20),
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `ingreso` (
  `ing_ID` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `prov_ID` int(16) UNSIGNED NOT NULL,
  `fecha` date NOT NULL  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `egreso` (
  `eg_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `ope_id` int(16) NOT NULL,
  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `comprobante` (
  `comp_id` int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `comp_prefijo` varchar(10) NOT NULL,
  `comp_numero` int(20),
  `ing_id` int(16) UNSIGNED NOT NULL 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
