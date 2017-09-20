# proveedor.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from lib.db import querier
import cerberus
# from lib import Validator


# Cambios para github solamente de prueba.

class ModeloProveedor(QtCore.QAbstractTableModel):
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloProveedor, self).__init__()
        self.__querier = querier.Querier( tabla = "proveedores", prefijo = "prov_")

        self.__scProveedor = {
            'prov_id' : {'type' : 'integer', 'nullable' : True },
            'prov_nombre' : {'type' : 'string', 'required' : True },
            'prov_razon_social' : {'type' : 'string', 'maxlength' : 20 },
            'prov_cuit' : {'type' : 'string', 'maxlength' : 20},
            'prov_direccion' : {'type' : 'string', 'maxlength' : 20},
            'prov_telefono' : {'type' : 'string', 'maxlength' : 20 },
            'prov_telefono_dos' : {'type' : 'string', 'maxlength' : 20 },
            'prov_email' : {'type' : 'string', 'empty' : True , 'required' : False },
            'prov_activo' : {'type' : 'integer', 'allowed' : [0, 1]}
        }

        self.__propiedades = [
            'Codigo',
            'Nombre',
            'Razon Social',
            'Cuit',
            'Direccion',
            'Teléfono',
            'Teléfono secundario',
            'Email'
        ]

        if propiedades:
            self.__propiedades = propiedades

        self.relacion = {
            'Codigo' : 'prov_id',
            'Nombre' : 'prov_nombre',
            'Razon Social' : 'prov_razon_social',
            'Cuit' : 'prov_cuit',
            'Direccion' : 'prov_direccion',
            'Teléfono' : 'prov_telefono',
            'Teléfono secundario' : 'prov_telefono_dos',
            'Email' : 'prov_email'
        }

        self.__busqueda = []

        for propiedad in self.__propiedades:
            self.__busqueda.append(self.relacion[propiedad])

        self.proveedores = self.__querier.traerElementos(self.__busqueda)
        self.proveedor = {}

    def crearProveedor(self, proveedorNuevo):
        v = self.__v.validate(proveedorNuevo, self.__scProveedor)
        if v:

            self.__querier.insertarElemento(proveedorNuevo)
        else:
            print("ERRORES: ",self.__v.errors)
        return v

    def verListaProveedores(self, campos = None, condiciones = None, limite = None):
        if not campos:
            campos = self.__busqueda

        self.proveedores = self.__querier.traerElementos(campos, condiciones, limite)
        self.layoutChanged.emit()

    def verDetallesProveedor(self, proveedor, condiciones = None, campos = None):
        # condiciones = ()
        print (proveedor)
        print (proveedor.row())
        if proveedor.row() >= 0:
            proveedor = self.proveedores[proveedor.row()]
        if not condiciones:
            condiciones = [('prov_id', '=', proveedor[0])]
        resultado = self.__querier.traerElementos(campos, condiciones, 1)
        if resultado:
            self.proveedor = resultado[0]
        else:
            return None
        # print(self.proveedor)
        return self.proveedor


    def modificarProveedor(self, proveedor):
        v = self.__v.validate(proveedor, self.__scProveedor)
        if v:
            self.__querier.actualizarElemento(proveedor)
        else:
            print("ERRORES: ",self.__v.errors)
        return v


    # def asociarProveedor(self, proveedor = { 'prov_nombre' : 'Indeterminado' }):
    #     # El ID de proveedor por defecto no debe ser 0000, sino el que sea creado para el proveedor con nombre "Indeterminado"
    #
    #     prov_id = proveedor.fetchID()
    #     art_id = self.fetchID()
    #
    #     if prov_id:
    #         QUERY = "UPDATE proveedores SET prov_ID = " + prov_id
    #         + " WHERE proveedores.art_ID = " + art_id
    #     else:
    #         print("El proveedor no existe")

    def toggleProveedorActivo(self, proveedor):
        if proveedor['prov_activo']:
            proveedor['prov_activo'] = 0
        else:
            proveedor['prov_activo'] = 1
        self.__querier.actualizarElemento(proveedor)

# ===============================================================
# Funciones para Modelo de tabla para PyQt
# ===============================================================
    def rowCount(self, parent):
        return len(self.proveedores)

    def columnCount(self, parent):
        if len(self.proveedores):
            return len(self.proveedores[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.proveedores[row][column]

            return value

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

            value = self.proveedores[row][column]

            return value

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                return self.__propiedades[section]
