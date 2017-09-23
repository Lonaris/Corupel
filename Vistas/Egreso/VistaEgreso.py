# VistaEgreso.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

class EgresoView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(EgresoView, self).__init__(parent)

        self.vistaLista = uic.loadUi("vistas/gui/egresos/Egreso.ui", self)
