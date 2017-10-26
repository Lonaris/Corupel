# elemento.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from lib.db import querier
import cerberus

class ModeloRelacionador(QtCore.QAbstractTableModel):

    __v = cerberus.Validator()


    def __init__(self, config, parent = None):
        super(ModeloRelacionador, self).__init__()

        __ArtQuerier = querier.Querier( tabla = "articulos", prefijo = "art_")
        __ProvQuerier = querier.Querier( tabla = "proveedores", prefijo = "prov_")

        # self.elementos = self.__querier.traerElementos(self.__busqueda)
        self.elementos = {}
        self.elemento = {}


    def verListaElementos(self, campos = None, condiciones = None, limite = None):
        if not campos:
            campos = self.__busqueda

        self.elementos = self.__querier.traerElementos(campos, condiciones, limite)
        self.layoutChanged.emit()

    def setTipo(self, tipo):
        pass

# ===============================================================
# Funciones para Modelo de tabla para PyQt
# ===============================================================
    def rowCount(self, parent):
        return len(self.elementos)

    def columnCount(self, parent):
        if self.elementos:
            return len(self.elementos[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.elementos[row][column]

            return value

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            value = self.elementos[row][column]
            return value

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__headers[section]
