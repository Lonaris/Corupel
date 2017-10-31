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

        self.__header = ["","","","",""]

        self.informe = [["", "", "", "", ""]]

    def traerInforme(self, filtros):
        # querier = {}

        tablas = ''
        campos = []
        condiciones = []
        union = ''
        on = ''

        if filtros['tipo'] == 0:
            campos = ["ingresos.ing_fecha", "articulos.art_descripcion", "movimientos_ingreso.movi_cantidad", "movimientos_ingreso.movi_costo"]
            tablas = 'articulos, movimientos_ingreso'
            union = 'ingresos'
            on = "ingresos.ing_id = movimientos_ingreso.ing_id"
            uniones =[
                ['ingresos',
                "ingresos.ing_id = movimientos_ingreso.ing_id"]
            ]
            condiciones = [
                ("articulos.art_id", "=", "movimientos_ingreso.art_id"),
                ("ingresos.ing_fecha", "BETWEEN", "'{}' AND '{}'".format(filtros['desde'], filtros['hasta'])),
                ("articulos.art_descripcion", "LIKE", "'%{}%'".format(filtros['busqueda']))
                ]

            if filtros['agrupacion']:
                condiciones.append(("articulos.art_agrupacion", "LIKE", "'{}'".format(filtros['agrupacion'])))
            if filtros['tercero']:
                uniones.append(['proveedores',
                    "proveedores.prov_id = ingresos.prov_id"])
                condiciones.append(("proveedores.prov_id", "=", filtros['tercero']))

        elif filtros['tipo'] == 1:
            campos = ["egr_fecha", "art_descripcion", "move_cantidad"]
            tablas = 'articulos, movimientos_egreso'
            uniones =[
                ['egresos',
                "egresos.egr_id = movimientos_egreso.egr_id"]
            ]
            condiciones = [
                ("articulos.art_id", "=", "movimientos_egreso.art_id"),
                ("egr_fecha", "BETWEEN", "'{}' AND '{}'".format(filtros['desde'], filtros['hasta'])),
                ("articulos.art_descripcion", "LIKE", "'%{}%'".format(filtros['busqueda']))
            ]
            if filtros['agrupacion']:
                condiciones.append(("articulos.art_agrupacion", "LIKE", "'{}'".format(filtros['agrupacion'])))
            if filtros['destino']:
                condiciones.append(("movimientos_egreso.move_destino", "=", filtros['destino']))
            if filtros['tercero']:
                uniones.append(['operarios',
                    "operarios.ope_legajo = egresos.ope_legajo"])
                condiciones.append(("operarios.ope_legajo", "=", filtros['tercero']))

        else:
            return False
        try:
            qr = querier.Querier(tabla = tablas)
            self.informe = qr.traerElementos(campos = campos,
                condiciones = condiciones,
                uniones = uniones)
            print(self.informe)
            self.__acomodarInforme(tipo = filtros['tipo'])
        except:
            # print("ERROR - ", qr.errorcode())
            return False
        self.layoutChanged.emit()

    def __acomodarInforme(self, tipo):
        reinforme = []
        if tipo == 0 or tipo == 2:

            for item in self.informe:
                item = list(item)
                item.append(str(item[2] * item[3]))
                item[0] = str(item[0])
                item[3] = str(item[3])
                reinforme.append(item)
            self.__header = ["Fecha", "Descripcion", "Cantidad", "Costo", "Costo total"]
        elif tipo == 1 or tipo == 3:
            for item in self.informe:
                item = list(item)
                item[0] = str(item[0])
                reinforme.append(item)

            self.__header = ["Fecha", "Descripcion", "Cantidad"]
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
                return self.__header[section]

    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows()
        self.endInsertRows()

    def removeRows():
        self.beginRemoveRows()
        self.endRemoveRows()
