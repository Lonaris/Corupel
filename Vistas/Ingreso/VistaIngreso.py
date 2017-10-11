# VistaIngreso.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator

class IngresoView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(IngresoView, self).__init__(parent)

        self.vista = uic.loadUi("vistas/gui/ingresos/Ingreso.ui", self)

        self.vista.tbl_articulos.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        rxPref = QRegExp("[0-9]{0,10}")
        rxNum = QRegExp("^[0-9]{0,20}$")
        rxId = QRegExp("^[0-9]{0,16}$")

        self.vista.prov_id.setValidator(QRegExpValidator(rxId))
        self.vista.rem_prefijo.setValidator(QRegExpValidator(rxPref))
        self.vista.rem_numero.setValidator(QRegExpValidator(rxNum))
        self.vista.fact_prefijo.setValidator(QRegExpValidator(rxPref))
        self.vista.fact_numero.setValidator(QRegExpValidator(rxNum))

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

    def getComprobantes(self):
        rxFact = QRegExp("fact_*")
        rxRem = QRegExp("rem_*")
        remito = self.vista.findChildren(QtWidgets.QWidget, rxRem)
        factura = self.vista.findChildren(QtWidgets.QWidget, rxFact)

        return (remito, factura)
