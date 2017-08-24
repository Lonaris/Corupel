# VistaListaArticulos.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox
from PyQt5.QtCore import pyqtSignal

class ListaArticuloView(QtWidgets.QWidget):
    senialBuscarArticulo = pyqtSignal()

    def __init__(self, presenter, parent=None):
        super(ListaArticuloView, self).__init__(parent)

        self.vistaLista = uic.loadUi("vistas/gui/articulos_lista.ui", self)

        self.vistaLista.btn_buscar.clicked.connect(self.buscarArticulos)


    def buscarArticulos(self):
        self.senialBuscarArticulo.emit()
