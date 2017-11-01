# VistaListaArticulos.py

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import pyqtSignal

class ListaArticuloView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(ListaArticuloView, self).__init__(parent)

        self.vistaLista = uic.loadUi("gui/listas/articulos_lista.ui", self)
        tabla = self.vistaLista.tbl_articulos

        tabla.horizontalHeader().setStretchLastSection(True)
        tabla.horizontalHeader().setSectionResizeMode(0)
        tabla.horizontalHeader().setDefaultSectionSize(100)
        #tabla.horizontalHeader().setColumnWidth( 0, 160 )
        #tabla.horizontalHeader().setCascadingSectionResizes(True)
        # tabla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
