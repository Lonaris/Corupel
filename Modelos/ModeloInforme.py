# informe.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from lib.db import querier
import cerberus

class ModeloInforme(QtCore.QAbstractTableModel):

    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloInforme, self).__init__()

        self.__busqueda = []

        self.__propiedadesArticulos = ["Fecha", "Descripcion", "Cantidad", "Costo", "Costo total"]
        self.__propiedadesProveedores = []
        self.__propiedadesOperarios = []

        self.informe = [["", "", "", "", ""]]

    def traerInforme(self, filtros):
        # querier = {}

        if filtros['tipo'] == 0:
            campos = ["ingresos.ing_fecha", "articulos.art_descripcion", "movimientos_ingreso.movi_cantidad", "movimientos_ingreso.movi_costo"]
            tablas = 'articulos, movimientos_ingreso'
            union = 'ingresos'
            on = "ingresos.ing_id = movimientos_ingreso.ing_id"
            condiciones = [
                ("articulos.art_id", "=", "movimientos_ingreso.art_id"),
                ("ingresos.ing_fecha", "BETWEEN", "'{}' AND '{}'".format(filtros['desde'], filtros['hasta'])),
                ("articulos.art_descripcion", "LIKE", "'%{}%'".format(filtros['busqueda']))
                ]
            limite = 20

            qr = querier.Querier(tabla = tablas)
            self.informe = qr.traerElementos(campos = campos,
                condiciones = condiciones,
                union = (union, on),
                limite = limite)
            self.__acomodarInforme(tipo = 0)

        elif filtros['tipo'] == 1:
            campos = []
            tablas = 'articulos, movimientos_egreso'
            union = 'egresos'

        elif filtros['tipo'] == 2:
            campos = []
            tablas = 'movimientos_ingreso, proveedores'
            union = 'ingresos'

        elif filtros['tipo'] == 3:
            campos = []
            tablas = 'movimientos_egreso, operarios'
            union = 'egresos'
        else:
            return False
        self.layoutChanged.emit()

    def __acomodarInforme(self, tipo):
        if tipo == 0:
            reinforme = []
            for item in self.informe:
                item = list(item)
                item.append(str(item[2] * item[3]))
                item[0] = str(item[0])
                item[3] = str(item[3])
                reinforme.append(item)
            self.informe = reinforme




# ===============================================================
# Funciones para Modelo de tabla para PyQt
# ===============================================================
    def rowCount(self, parent):
        return len(self.informe)

    def columnCount(self, parent):
        if self.informe:
            return len(self.informe[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.informe[row][column]

            return value

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

            value = self.informe[row][column]

            return value

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                return self.__propiedadesArticulos[section]

    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows()
        self.endInsertRows()

    def removeRows():
        self.beginRemoveRows()
        self.endRemoveRows()
