# VistaIngreso.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

class IngresoView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(IngresoView, self).__init__(parent)

        self.vistaLista = uic.loadUi("vistas/gui/ingresos/Ingreso.ui", self)
