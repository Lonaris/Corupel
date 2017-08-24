# articulo.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from lib.db import querier

# from lib import Validator


class ModeloArticulo(QtCore.QAbstractTableModel):

    # db = mysql.connector.connect(user = 'admin', password = 'admin1234', host = '127.0.0.1', database = 'corupel')
    __querier = querier.Querier( tabla = "articulos", prefijo = "art_")

    def __init__(self, parent = None):
        super(ModeloArticulo, self).__init__()

        # self.articulos = [()]
        self.propiedades = ('art_id', 'prov_id','art_cod_barras',
            'art_descripcion',
            'art_marca', 'art_agrupacion',
            # 'art_stock_min', 'art_stock_actual',
            'art_activo'
            )
        # self.crearArticulo(articulo)
        self.__headers = self.propiedades
        self.articulos = self.__querier.traerElementos(self.__headers)
        self.articulo = {}

    def crearArticulo(self, articuloNuevo):
        self.__querier.insertarElemento(articuloNuevo)

    def verListaArticulos(self, campos = None, condiciones = None, limite = None):
        if not campos:
            campos = self.propiedades

        self.articulos = self.__querier.traerElementos(campos, condiciones, limite)
        self.layoutChanged.emit()

    def verDetallesArticulo(self, articulo, campos = None, condiciones = None):
        # condiciones = ()

        # print (articulo.row())
        articulo = self.articulos[articulo.row()]
        condiciones = [('art_id', '=', articulo[0])]
        resultado = self.__querier.traerElementos(campos, condiciones, 1)
        self.articulo = resultado[0]
        # print(self.articulo)
        return self.articulo


    def modificarArticulo(self, articulo):
        self.__querier.actualizarElemento(articulo)

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

        articulo['art_activo'] = 0
        self.__querier.actualizarElemento(articulo)

    def habilitarArticulo(self, articulo):
        articulo['art_activo'] = 1
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
# Funciones para Modelo de tabla para PyQt
# ===============================================================
    def rowCount(self, parent):
        return len(self.articulos)

    def columnCount(self, parent):
        return len(self.articulos[0])

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.articulos[row][column]

            return value

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

            value = self.articulos[row][column]

            return value

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                return self.__headers[section]

    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows()


        self.endInsertRows()

    def insertColumns(self, position, columns, parent = QtCore.QModelIndex()):
        self.beginInsertColumns()
        self.endInsertColumns()

    def removeRows():

        self.beginRemoveRows()
        self.endRemoveRows()


    def removeColumns():

        self.beginRemoveColumns()
        self.endRemoveColumns()
