# VistaInforme.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate

class InformeView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(InformeView, self).__init__(parent)

        self.vista = uic.loadUi("gui/informes/informes.ui", self)

        self.vista.filtro_principal.currentIndexChanged.connect(self.setFiltros)
        self.setFiltros()

        # self.vista.tbl_informe.setColumnWidth(1, 600)

    def setFechas(self, desde, hasta):
        self.vista.fecha_desde.setDate(QDate(desde))
        self.vista.fecha_hasta.setDate(QDate(hasta))

    def getFiltros(self):
        return (self.vista.filtro_principal.currentIndex(),
            self.vista.buscador.text(),
            self.vista.fecha_desde.date(),
            self.vista.fecha_hasta.date(),
            self.vista.tercero.text())

    def setFiltros(self):
        tercero = self.vista.tercero
        destino = self.vista.filtro_destino
        if self.vista.filtro_principal.currentIndex() == 0:
            tercero.show()
            tercero.setPlaceholderText('Código de Proveedor')
            destino.hide()

        elif self.vista.filtro_principal.currentIndex() == 1:
            tercero.show()
            tercero.setPlaceholderText('Legajo de Operario')
            destino.show()

        else:
            tercero.hide()
            tercero.setText("")
