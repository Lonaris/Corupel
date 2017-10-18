# VistaInforme.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate

class InformeView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(InformeView, self).__init__(parent)

        self.vista = uic.loadUi("vistas/gui/informes/informes.ui", self)

    def setFechas(self, desde, hasta):
        self.vista.fecha_desde.setDate(QDate(desde))
        self.vista.fecha_hasta.setDate(QDate(hasta))

    def getFiltros(self):
        return (self.vista.filtro.currentIndex(),
            self.vista.buscador.text(),
            self.vista.fecha_desde.date(),
            self.vista.fecha_hasta.date())
