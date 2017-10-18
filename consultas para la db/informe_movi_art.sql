use corupel;
select 
#	articulos.art_id, art_descripcion, movimientos_ingreso.art_id, movi_id, movi_restante, movi_cantidad, movi_costo, ing_fecha  
	ing_fecha, art_descripcion, movi_cantidad, movi_costo
    from articulos, movimientos_ingreso
	join ingresos on ingresos.ing_id = movimientos_ingreso.ing_id
	where articulos.art_id = movimientos_ingreso.art_id
    AND ing_fecha BETWEEN '2017-10-9' AND '2017-10-20';
    AND movimientos_ingreso.art_id = 1214;