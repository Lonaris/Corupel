# articulo_view.py

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

        self.vistaDetalle = uic.loadUi("vistas/gui/articulos_detalle.ui", self)

        self.vistaDetalle.btn_modificar.clicked.connect(self.modificarArticulo)
        self.vistaDetalle.btn_nuevo.clicked.connect(self.crearArticulo)
        self.vistaDetalle.btn_deshabilitar.clicked.connect(self.deshabilitarArticulo)

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
        articuloID = self.vistaDetalle.findChild(QLineEdit, name = "art_id")
        self.senialDeshabilitarArticulo.emit(articuloID)

    def getArticulo(self):
        rawArticulo = self.vistaDetalle.findChildren(QComboBox)
        rawArticulo += (self.vistaDetalle.findChildren(QLineEdit))

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

    def setArticulo(self, articulo):
        print (articulo)
        self.vistaDetalle.art_id.setText(str(articulo[0]))
        self.vistaDetalle.prov_id.setText(str(articulo[1]))
        self.vistaDetalle.art_cod_barras.setText(articulo[2])
        self.vistaDetalle.art_descripcion.setText(articulo[3])
        # self.vistaDetalle.art_marca.setText(articulo[4])
        # self.vistaDetalle.art_agrupacion.setText(articulo[5])
