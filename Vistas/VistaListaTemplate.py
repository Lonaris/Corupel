# VistaListaElementos.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

class ListaElementosView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(ListaElementosView, self).__init__(parent)

        self.vistaLista = uic.loadUi("vistas/gui/listas/elementos_lista.ui", self)
