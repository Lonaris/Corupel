# ingreso.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from lib.db import querier
import cerberus
# from lib import Validator


# Cambios para github solamente de prueba.

class ModeloIngreso(QtCore.QAbstractTableModel):

    # db = mysql.connector.connect(user = 'admin', password = 'admin1234', host = '127.0.0.1', database = 'corupel')
    __querier = querier.Querier( tabla = "ingresos", prefijo = "ing_")
    __querierMovi = querier.Querier( tabla = "movimientos_ingreso", prefijo = "movi_")
    __querierArt = querier.Querier( tabla = "articulos", prefijo = "art_")
    __querierProv = querier.Querier( tabla = "proveedores", prefijo = "prov_")

    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloIngreso, self).__init__()

        self.__scIngreso = {
        'ing_id' : {'type' : 'integer', 'max' : 9999999999999999 },
        'ing_columna1' : {'type' : 'string' },
        'ing_columna2' : {'type' : 'string' },
        'ing_columna3' : {'type' : 'string' },
        'ing_columna4' : {'type' : 'string' },
        }

        self.__scMovIngreso = {
        'movi_' : { 'type' : 'something' },
        'movi_' : { 'type' : 'something' },
        'movi_' : { 'type' : 'something' },
        'ing_id' : { 'type' : 'integer', 'max' : 9999999999999999 },
        }

        self.__headers = ["Codigo", "Descripcion", "Cantidad", "Costo"]

        # self.__movimientos = self.__querier.traerElementos(self.__busqueda)
        self.__movimientos = [["", "", "", ""]]
        self.ingreso = {}
        self.__proveedor = {}

    def crearIngreso(self, ingresoNuevo):
        print(self.__v.validate(ingresoNuevo, self.__scIngreso))
        print("ERRORES: ",self.__v.errors)
        self.__querier.insertarIngreso(ingresoNuevo)

    def verListaIngresos(self, campos = None, condiciones = None, limite = None):
        if not campos:
            campos = self.__busqueda

        self.__movimientos = self.__querier.traerElementos(campos, condiciones, limite)
        self.layoutChanged.emit()

    def verDetallesIngreso(self, ingreso, campos = None, condiciones = None):
        ingreso = self.__movimientos[ingreso.row()]
        condiciones = [('ing_id', '=', ingreso[0])]
        resultado = self.__querier.traerElementos(campos, condiciones, 1)
        self.ingreso = resultado[0]
        return self.ingreso

    def modificarIngreso(self, ingreso):
        self.__querier.actualizarIngreso(ingreso)

    def toggleIngresoActivo(self, ingreso):
        if ingreso['ing_activo']:
            ingreso['ing_activo'] = 0
        else:
            ingreso['ing_activo'] = 1
        self.__querier.actualizarIngreso(ingreso)

    def buscarProveedor(self, campos = None, condiciones = None):
        self.__proveedor = {}
        resultado = self.__querierProv.traerElementos(campos, condiciones)
        if resultado:
            self.__proveedor = resultado[0]
        return self.__proveedor

    def getMovimientos(self):
        return self.__movimientos
# ===============================================================
# Funciones para Modelo de tabla para PyQt
# ===============================================================
    def rowCount(self, parent):
        return len(self.__movimientos)

    def columnCount(self, parent):
        if self.__movimientos:
            return len(self.__movimientos[0])
        else:
            return 0

    def flags(self, index):
        columna = index.column()
        fila = index.row()

        if (columna == 2 or columna == 3) and self.__movimientos[fila][0]:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        if columna == 0:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__movimientos[row][column]

            return value

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

            self.__articulo = {}
            if self.__proveedor:
                provId = self.__proveedor[0]
            # if not provId:
            #     return False
            if column == 0:
                try:
                    value = int(value)
                    # resultado = self.__querierArt.traerElementos(campos = ("art_id", "art_descripcion"), condiciones = [("art_id", " = ", value), ("prov_id", " = ", provId)], union = ['articulos_de_proveedores', '`proveedores`.`prov_id` = `articulos_de_proveedores`.`proveedor`'])
                    resultado = self.__querierArt.traerElementos(campos = ("art_id", "art_descripcion"), condiciones = [("art_id", " = ", value)])
                    self.__articulo = list(resultado[0])
                    self.__articulo.append(0)
                    self.__articulo.append(0)
                except:
                    return False
                if not self.__movimientos[row][0]:
                    self.insertRows(1, 1)
                else:
                    self.__movimientos[row] = self.__articulo
                self.dataChanged.emit(index, index)
                return True
            else:
                try:
                    value = int(value)
                except:
                    return False
                self.__movimientos[row][column] = value
                self.dataChanged.emit(index, index)
                return True

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                return self.__headers[section]

    def insertRows(self, row, count = 1, parent = QtCore.QModelIndex()):

        self.beginInsertRows(parent, 1, 1)
        self.__movimientos.insert(1, self.__articulo)
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
