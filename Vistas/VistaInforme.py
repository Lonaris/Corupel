# VistaInforme.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate

class InformeView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(InformeView, self).__init__(parent)

        self.vista = uic.loadUi("vistas/gui/informes/informes.ui", self)

        self.vista.filtro.currentIndexChanged.connect(self.setTercero)
        self.setTercero()

    def setFechas(self, desde, hasta):
        self.vista.fecha_desde.setDate(QDate(desde))
        self.vista.fecha_hasta.setDate(QDate(hasta))

    def getFiltros(self):
        return (self.vista.filtro.currentIndex(),
            self.vista.buscador.text(),
            self.vista.fecha_desde.date(),
            self.vista.fecha_hasta.date(),
            self.vista.tercero.text())

    def setTercero(self):
        tercero = self.vista.tercero
        if self.vista.filtro.currentIndex() == 2:
            tercero.show()
            tercero.setPlaceholderText('Código de Proveedor')

        elif self.vista.filtro.currentIndex() == 3:
            tercero.show()
            tercero.setPlaceholderText('Legajo de Operario')

        else:
            tercero.hide()
            tercero.setText("")
