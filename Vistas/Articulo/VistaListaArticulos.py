# VistaListaArticulos.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox
from PyQt5.QtCore import pyqtSignal

class ListaArticuloView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(ListaArticuloView, self).__init__(parent)

        self.vistaLista = uic.loadUi("vistas/gui/listas/articulos_lista.ui", self)

        # self.vistaLista.btn_buscar.clicked.connect(self.buscarArticulos)

    # def buscarArticulos(self):
    #     self.senialBuscarArticulos.emit()
