# VistaIngreso.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

class IngresoView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(IngresoView, self).__init__(parent)

        self.vista = uic.loadUi("vistas/gui/ingresos/Ingreso.ui", self)

    def setProveedor(self, proveedor):
        self.vista.prov_id.setText(str(proveedor[0]))
        self.vista.prov_nombre.setText(proveedor[1])

    def getProveedor(self):
        return self.vista.prov_id.text()

    def resetProveedor(self):
        self.vista.prov_id.setText("")
        self.vista.prov_nombre.setText("")

    def setTotales(self, totalArticulos, totalCosto):
        self.tot_cant.setText(str(totalArticulos))
        self.tot_cost.setText(str(totalCosto))
