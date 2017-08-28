# articulo_view.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox, QLabel
from PyQt5.QtCore import pyqtSignal, QRegExp

#Creamos la clase ArticuloView
class ArticuloView(QtWidgets.QWidget):

    senialCrearArticulo = pyqtSignal([dict])
    senialModificarArticulo = pyqtSignal([dict])
    senialDeshabilitarArticulo = pyqtSignal(QComboBox)
    rx = QRegExp("art_*")


	#Inicializamos el objeto
    def __init__(self, presenter, parent=None):
        super(ArticuloView, self).__init__(parent)
        # Todos los Widgets de PyQT deben ser privados,
        # esto se logra NO COLOCANDO 'self.' sino la variable localmente.

        #Traemos el archivo .UI "Articulos_detalle"
        self.vistaDetalle = uic.loadUi("vistas/gui/articulos_detalle.ui", self)
		
		#Utilizamos el evento clicked.connect de los botones del archivo .ui para ejecutar la funciones.
        self.vistaDetalle.btn_modificar.clicked.connect(self.modificarArticulo)
        self.vistaDetalle.btn_nuevo.clicked.connect(self.crearArticulo)
        self.vistaDetalle.btn_deshabilitar.clicked.connect(self.deshabilitarArticulo)


    #Creamos la funcion crear articulo que va a ser llamada al clickear "btn_nuevo"
    def crearArticulo(self):
        articulo = self.getArticulo()
        articulo.pop('art_id', None)
        # Hardcode:Debe ser eliminado por propositos de prueba
        articulo['prov_id'] = 4
        articulo['art_stock_ideal'] = 4
        self.senialCrearArticulo.emit(articulo)


    #Creamos la funcion modificarArticulo que va a ser llamada al clickear "btn_modificar"
    def modificarArticulo(self):
        articulo = self.getArticulo()
        self.senialModificarArticulo.emit(articulo)


    #Creamos la funcion deshabilitarArticulo que va a ser llamada al clickear "btn_deshabilitar"
    def deshabilitarArticulo(self):
        articuloID = self.vistaDetalle.findChild(QLineEdit, name = "art_id")
        self.senialDeshabilitarArticulo.emit(articuloID)

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
