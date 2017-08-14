# articulo_view.py
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox
from PyQt5.QtCore import pyqtSignal

class ArticuloView(QtWidgets.QWidget):

    senialCrearArticulo = pyqtSignal([dict])
    senialModificarArticulo = pyqtSignal([dict])
    senialDeshabilitarArticulo = pyqtSignal(QComboBox)

    def __init__(self, presenter, parent=None):
        super(ArticuloView, self).__init__(parent)
        # Todos los Widgets de PyQT deben ser privados,
        # esto se logra NO COLOCANDO 'self.' sino la variable localmente.

        self.vista = uic.loadUi("vistas/gui/articulos.ui", self)

        self.vista.btn_modificar.clicked.connect(self.modificarArticulo)
        self.vista.btn_nuevo.clicked.connect(self.crearArticulo)
        self.vista.btn_deshabilitar.clicked.connect(self.deshabilitarArticulo)

    def crearArticulo(self):
        articulo = self.getArticulo()
        articulo.pop('art_id', None)

# HARDCODED: DEBE SER ELIMINADO POR PROPOSITOS DE PRUEBA
        articulo['prov_id'] = 4
        articulo['art_stock_ideal'] = 4

        self.senialCrearArticulo.emit(articulo)

    def modificarArticulo(self):
        articulo = self.getArticulo()
        self.senialModificarArticulo.emit(articulo)

    def deshabilitarArticulo(self):
        articuloID = self.vista.findChild(QLineEdit, name = "art_id")

        self.senialDeshabilitarArticulo.emit(articuloID)

    def buscarArticulos(self):
        pass

    def getArticulo(self):
        rawArticulo = self.vista.findChildren(QComboBox)
        rawArticulo += (self.vista.findChildren(QLineEdit))

        articulo = {}

        for componente in rawArticulo:
            if "art_" not in componente.objectName():
                continue
            if (type(componente) == QtWidgets.QLineEdit):
                articulo[componente.objectName()] = componente.text()
                # print(componente.objectName(), componente.text())

            else:
                articulo[componente.objectName()] = componente.currentText()
                # print(componente.objectName(), componente.currentText())
        print (articulo)
        return articulo
