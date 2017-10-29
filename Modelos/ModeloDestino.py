from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from lib.db import querier
import cerberus

class ModeloDestino(QtCore.QAbstractListModel):


    __v = cerberus.Validator()


    def __init__(self, parent = None):
        super(ModeloDestino, self).__init__()
        self.__querier = querier.Querier(tabla = "destinos", prefijo = "des_")

        self.__destinos = ["Destino"]

        try:
            resultados = self.__querier.traerElementos(campos = ["des_maquina"] )
            print("Resultados: ", resultados)
            for resultado in resultados:
                self.__destinos.append(resultado[0])
            self.layoutChanged.emit()

        except:
            # mensaje el observer que hay un error, guardarlo en el log de errores y cerrar
            print('ERROR - No se pudieron levantar los destinos')

        print (self.__destinos)

    def rowCount(self, parent):
        return len(self.__destinos)

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            fila = index.row()
            valor = self.__destinos[fila]

            return valor

    def setData(self, index, valor, role = QtCore.Qt.EditRole):

        if role == QtCore.Qt.DisplayRole:
            fila = index.row()
            valor = self.__destinos[fila]

            return valor
