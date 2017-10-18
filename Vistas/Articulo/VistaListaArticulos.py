# VistaListaArticulos.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

class ListaArticuloView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(ListaArticuloView, self).__init__(parent)

        self.vistaLista = uic.loadUi("vistas/gui/listas/articulos_lista.ui", self)
        tabla = self.vistaLista.tbl_articulos

        tabla.horizontalHeader().setStretchLastSection(True)

        # tabla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
