# egreso.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from datetime import date
from lib.db import querier
import cerberus
# from lib import Validator


# Cambios para github solamente de prueba.

class ModeloEgreso(QtCore.QAbstractTableModel):

    # db = mysql.connector.connect(user = 'admin', password = 'admin1234', host = '127.0.0.1', database = 'corupel')
    __querier = querier.Querier( tabla = "egresos", prefijo = "egr_")
    __querierMove = querier.Querier( tabla = "movimientos_egreso", prefijo = "move_")
    __querierMovi = querier.Querier( tabla = "movimientos_ingreso", prefijo = "movi_")
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
        self.__maximos = [0]
        self.egreso = {}

    def crearEgreso(self, operario, detalles):
        if len(self.__movimientos) == 1:
            return False

        hoy = date.today()

        egreso = { 'egr_fecha' : hoy, 'ope_legajo' : operario }

        self.__querier.insertarElemento(egreso)
        egrId = self.__querier.traerElementos(campos = ["egr_id"], orden = ("egr_id", "DESC"), limite = 1)
        egrId = egrId[0][0]

        for movimiento in self.__movimientos:
            if movimiento[2] == 0 or movimiento[2] == '':
                continue
            movimiento = { 'art_id' : movimiento[0],
            'egr_id' : egrId,
            'move_cantidad' : movimiento[2],
            'move_destino' : detalles[0],
            'move_sector' : detalles[1]
            }

            stock = int(movimiento['move_cantidad'])
            restantesIn = self.__querierMovi.traerElementos(campos = ["movi_id, movi_restante"],
                orden = ("movi_id", "ASC"),
                condiciones = [("art_id", " = ", movimiento['art_id'])])
            restantesOut = []
            for restante in restantesIn:
                restante = list(restante)
                if restante[1] > stock:
                    restante[1] -= stock
                else:
                    stock -= restante[1]
                    restante[1] = 0
                restantesOut.append({ 'movi_id' : restante[0], 'movi_restante' : restante[1]})
            print ("DEBUG - Los restantes a actualizar en la base de datos son: ", restantesOut)

            if not movimiento['art_id']:
                continue
            self.__querierMove.insertarElemento(movimiento)
            for elemento in restantesOut:
                self.__querierMovi.actualizarElemento(elemento)
        # self.reiniciarTablaEgreso()
        return True

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

    def reiniciarTablaEgreso(self):
        self.__maximos = [0]
        self.egreso = {}
        self.removeRows()

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
        return QtCore.Qt.ItemIsEnabled

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

            if column == 0:
                for articulo in self.__movimientos:
                    if value == str(articulo[0]):
                        return False

            self.__articulo = {}

            stockTotal = 0
            if column == 0:
                try:
                    value = int(value)
                    # resultado = self.__querierArt.traerElementos(campos = ("art_id", "art_descripcion"), condiciones = [("art_id", " = ", value), ("prov_id", " = ", provId)], union = ['articulos_de_proveedores', '`proveedores`.`prov_id` = `articulos_de_proveedores`.`proveedor`'])
                    resultado = self.__querierArt.traerElementos(campos = ("art_id", "art_descripcion"),
                        condiciones = [("art_id", " = ", value)])
                    cantidadesRestantes = self.__querierMovi.traerElementos(campos = ["movi_restante"], condiciones = [("art_id", " = ", value), ("movi_restante", " > ", 0)])
                    print("DEBUG - Cantidades restantes del articulo: ", cantidadesRestantes)
                    for cantidad in cantidadesRestantes:
                        stockTotal += cantidad[0]
                    print ("DEBUG - Stock total del articulo. ", stockTotal)
                    self.__articulo = list(resultado[0])
                    self.__articulo.append(stockTotal)
                    print(self.__articulo)
                except:
                    return False
                if not self.__movimientos[row][0]:
                    self.insertRows(self.rowCount(self), 1)
                    self.__maximos.insert(self.rowCount(self), stockTotal)
                else:
                    self.__movimientos[row] = self.__articulo
                    self.__maximos[row] = stockTotal
                self.dataChanged.emit(index, index)
                return True
            else:

                try:
                    value = int(value)
                    print(value, self.__movimientos[row][2])
                    if value < 0:
                        return False
                    elif value > self.__maximos[row]:
                        return False
                except:
                    return False
                self.__movimientos[row][column] = value
                self.dataChanged.emit(index, index)
                return True
            return False

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                return self.__headers[section]

    def insertRows(self, row, count, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, row, row)
        self.__movimientos.insert(row, self.__articulo)
        self.endInsertRows()

    def removeRows(self, row = 1, parent = QtCore.QModelIndex()):
        last = self.rowCount(parent) - 1
        self.beginRemoveRows(parent, row, last)
        self.__movimientos = [["", "", "", ""]]
        # self.dataChanged.emit()
        self.endRemoveRows()
