# VistaEgreso.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

class EgresoView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(EgresoView, self).__init__(parent)

        self.vista = uic.loadUi("vistas/gui/egresos/Egreso.ui", self)

    def setOperario(self, proveedor):
        self.vista.ope_legajo.setText(str(proveedor[0]))
        self.vista.ope_nombre.setText(proveedor[1])

    def getOperario(self):
        return self.vista.ope_legajo.text()

    def resetOperario(self):
        self.vista.ope_legajo.setText("")
        self.vista.ope_nombre.setText("")

    def setTotal(self, totalArticulos):
        self.egr_total_cant.setText(str(totalArticulos))

    def getDetalles(self):
        destino = self.vista.move_destino.text()
        sector = self.vista.move_sector.currentText()

        return (destino, sector)
