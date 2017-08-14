# articulo.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from lib.db import querier


class ModeloArticulo(object):

    db = mysql.connector.connect(user = 'admin', password = 'admin1234', host = '127.0.0.1', database = 'corupel')
    __querier = querier.Querier( tabla = "articulos", prefijo = "art_")

    def __init__(self, articulo):
        self.articulo = {}
        self.propiedades = ('art_ID', 'art_cod_barras',
            'art_descripcion',
            'art_marca', 'art_agrupacion',
            'art_stock_min', 'art_stock_actual',
            'art_activo'
            )
        # self.crearArticulo(articulo)

    def crearArticulo(self, articuloNuevo):
        # self.articulo = articuloNuevo
        # if not self.__esArticuloValido(articuloNuevo):
        #     #return (ERROR, "El articulo no es valido")
        #     return "El articulo no es valido"
        #
        # for key, value in articuloNuevo.items():
        #     if self.__esPropiedadValida(key):
        #         self.articulo[key] = value

        self.__querier.insertarElemento(articuloNuevo)


    # def toggleArticuloStatus(self):
    #     if self.articulo[status] == "Activo":
    #         self.articulo[status] = "Inactivo"
    #     else:
    #         self.articulo[status] = "Activo"
    #     __actualizarArticulo()

    def sumarStockArticulo():
        pass

    def restarStockArticulo():
        pass

    def verListaArticulos():
        pass

    def verDetallesArticulo():
        pass

    def modificarArticulo(self, modificacion):
        # if not self.__esArticuloValido(modificacion):
        #     # return (ERROR, "Modificacion no valida")
        #     return "Las modificaciones no son validas" #Deberia entrar en mas detalle

        # self.articulo = modificacion

        self.__querier.actualizarElemento(modificacion)

    def asociarProveedor(self, proveedor = { 'prov_nombre' : 'Indeterminado' }):
        # El ID de proveedor por defecto no debe ser 0000, sino el que sea creado para el proveedor con nombre "Indeterminado"

        prov_id = proveedor.fetchID()
        art_id = self.fetchID()

        if prov_id:
            QUERY = "UPDATE articulos SET prov_ID = " + prov_id
            + " WHERE articulos.art_ID = " + art_id
        else:
            print("El proveedor no existe")

    def deshabilitarArticulo(self, articulo):

        #VALIDACIONES

        #===========

        #Funcion propiamente dicha

        articulo['status'] = "Inactivo"
        self.__querier.actualizarElemento(articulo)

    def habilitarArticulo(self, articulo):
        articulo['status'] = "Activo"
        self.__querier.actualizarElemento(articulo)

    def __esArticuloValido(self, articulo):
        # propiedades se encuentra en el scope global de la clase

        campos_faltantes = []

        try:
            for propiedad in self.propiedades:
                if propiedad not in articulo:
                    campos_faltantes.insert(0, propiedad)
            if campos_faltantes:
                raise ValueError(campos_faltantes)
        except ValueError as vError:
            print("Error. Faltan los siguientes campos: ")
            for error in campos_faltantes:
                print(error)
            return False
        return True

    def __esPropiedadValida(self, propiedad):
        try:
            if propiedad not in self.propiedades:
                raise ValueError(propiedad)
        except ValueError:
            print ("El valor {} no es valido para un articulo".format(propiedad))
            return False
        return True

# ===============================================================
# Modelo de tabla para PyQt
# ===============================================================

class ArticuloTableModel(QtCore.QAbstractTableModel):

    def __init__(self, articulos = [], parent = None):
        self.articulos = {}

        for articulo in articulos:
            for key, value in articulo.items():
                try:
                    if key in self.propiedades:
                        self.articulos[key] = value
                    else:
                        raise ValueError(key)
                except ValueError:
                    print ("El valor {} no es valido para un articulo".format(key))

            if articuloInsertadoEsValido(articulo) == False:
                #delete articulo
                pass



    def articuloInsertadoEsValido(self, articulo):
        pass

    def rowCount(self, parent):
        pass

    def data(self, index, role):
        pass

    def insertRows():
        pass
