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
            self.vista.filtro_destino.currentIndex(),
            self.vista.filtro_agrupacion.currentText(),
            self.vista.filtro_tercero.text(),
            self.vista.buscador.text(),
            self.vista.fecha_desde.date(),
            self.vista.fecha_hasta.date())

    def setFiltros(self):
        tercero = self.vista.filtro_tercero
        destino = self.vista.filtro_destino
        agrupacion = self.vista.filtro_agrupacion
        buscador = self.vista.buscador

        if self.vista.filtro_principal.currentIndex() == 0:
            tercero.setPlaceholderText('Código de Proveedor')
            destino.hide()

        elif self.vista.filtro_principal.currentIndex() == 1:
            tercero.setPlaceholderText('Legajo de Operario')
            destino.show()

        destino.setCurrentIndex(0)
        agrupacion.setCurrentIndex(0)
        buscador.setText("")
        tercero.setText("")
