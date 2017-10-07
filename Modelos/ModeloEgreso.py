# egreso.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from lib.db import querier
import cerberus
# from lib import Validator


# Cambios para github solamente de prueba.

class ModeloEgreso(QtCore.QAbstractTableModel):

    # db = mysql.connector.connect(user = 'admin', password = 'admin1234', host = '127.0.0.1', database = 'corupel')
    __querier = querier.Querier( tabla = "egresos", prefijo = "egr_")
    __querierMovi = querier.Querier( tabla = "movimientos_egreso", prefijo = "movi_")
    __querierArt = querier.Querier( tabla = "articulos", prefijo = "art_")
    __querierOpe = querier.Querier( tabla = "operarios", prefijo = "ope_")

    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloEgreso, self).__init__()

        self.__scEgreso = {
        'egr_id' : {'type' : 'integer', 'max' : 9999999999999999 },
        'egr_columna1' : {'type' : 'string' },
        'egr_columna2' : {'type' : 'string' },
        'egr_columna3' : {'type' : 'string' },
        'egr_columna4' : {'type' : 'string' },
        }

        self.__scMovEgreso = {
        'movi_' : { 'type' : 'something' },
        'movi_' : { 'type' : 'something' },
        'movi_' : { 'type' : 'something' },
        'egr_id' : { 'type' : 'integer', 'max' : 9999999999999999 },
        }

        self.__headers = ["Codigo", "Descripcion", "Cantidad"]

        # self.__movimientos = self.__querier.traerElementos(self.__busqueda)
        self.__movimientos = [["", "", ""]]
        self.egreso = {}

    def crearEgreso(self, egresoNuevo):
        print(self.__v.validate(egresoNuevo, self.__scEgreso))
        print("ERRORES: ",self.__v.errors)
        self.__querier.insertarEgreso(egresoNuevo)

    def verListaEgresos(self, campos = None, condiciones = None, limite = None):
        if not campos:
            campos = self.__busqueda

        self.__movimientos = self.__querier.traerElementos(campos, condiciones, limite)
        self.layoutChanged.emit()

    def verDetallesEgreso(self, egreso, campos = None, condiciones = None):
        egreso = self.__movimientos[egreso.row()]
        condiciones = [('egr_id', '=', egreso[0])]
        resultado = self.__querier.traerElementos(campos, condiciones, 1)
        self.egreso = resultado[0]
        return self.egreso

    def modificarEgreso(self, egreso):
        self.__querier.actualizarEgreso(egreso)

    def toggleEgresoActivo(self, egreso):
        if egreso['egr_activo']:
            egreso['egr_activo'] = 0
        else:
            egreso['egr_activo'] = 1
        self.__querier.actualizarEgreso(egreso)

    def buscarOperario(self, campos = None, condiciones = None):
        self.__operario = {}
        resultado = self.__querierOpe.traerElementos(campos, condiciones)
        if resultado:
            self.__operario = resultado[0]
        return self.__operario

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
