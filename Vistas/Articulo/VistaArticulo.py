# articulo_view.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox, QLabel
from PyQt5.QtCore import pyqtSignal, QRegExp

#Creamos la clase ArticuloView
class ArticuloView(QtWidgets.QWidget):

    # senialCrearArticulo = pyqtSignal([dict])
    # senialModificarArticulo = pyqtSignal([dict])
    # senialDeshabilitarArticulo = pyqtSignal(QComboBox)
    rx = QRegExp("art_*")


	#Inicializamos el objeto
    def __init__(self, presenter, parent=None):
        super(ArticuloView, self).__init__(parent)

        #Traemos el archivo .UI "Articulos_detalle"
        self.vistaDetalle = uic.loadUi("vistas/gui/detalles/articulo_detalle.ui", self)

    #Funcion que trae un articulo y modifica la ifnormacion.
    def getArticulo(self):
        rawArticulo = self.vistaDetalle.findChildren((QComboBox, QLineEdit, QLabel), self.rx)
        articulo = {}
        for componente in rawArticulo:
            if "art_" not in componente.objectName():
                continue
            if (type(componente) == QtWidgets.QComboBox):
                articulo[componente.objectName()] = componente.currentText()
                # print(componente.objectName(), componente.currentText())
            else:
                articulo[componente.objectName()] = componente.text()
                # print(componente.objectName(), componente.text())
        print ("\nDEBUG - ARTICULO: ", articulo)
        return articulo

	#Funcion que carga un articulo en particular dentro de "Detalle del Producto"
    def setArticulo(self, articulo):
        print (articulo)
        self.vistaDetalle.art_id.setText(str(articulo[0]))
        self.vistaDetalle.prov_id.setText(str(articulo[1]))
        self.vistaDetalle.art_cod_barras.setText(articulo[2])
        self.vistaDetalle.art_descripcion.setText(articulo[3])
        # self.vistaDetalle.art_marca.setText(articulo[4])
        # self.vistaDetalle.art_agrupacion.setText(articulo[5])

    def resetArticulo(self):
        self.vistaDetalle.art_id.setText("")
        self.vistaDetalle.prov_id.setText("")
        self.vistaDetalle.art_cod_barras.setText("")
        self.vistaDetalle.art_descripcion.setText("")
