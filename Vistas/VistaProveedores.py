# articulo_view.py
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtCore import pyqtSignal

class ArticuloView(QtWidgets.QWidget):

    addClicked = pyqtSignal()

    def __init__(self, presenter, parent=None):
        super(ArticuloView, self).__init__(parent)
        # Todos los Widgets de PyQT deben ser privados,
        # esto se logra NO COLOCANDO 'self.' sino la variable localmente.

        mainWindow = uic.loadUi("Vistas/Articulos/ingresos.ui", self)
        mainWindow.pushButton_25.clicked.connect(presenter.accion)

    def enviarArticulo():
        self.addClicked.emit()
