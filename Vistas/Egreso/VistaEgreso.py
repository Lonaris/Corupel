# VistaEgreso.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal

class EgresoView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(EgresoView, self).__init__(parent)

        self.vista = uic.loadUi("gui/egresos/Egreso.ui", self)
        #Conectamos el evento modificar y guardar con la funcion "operacionCOmpletada"
        self.vista.btn_guardar.clicked.connect(self.operacionCompletada)

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
        destino = self.vista.move_destino.currentIndex()
        sector = self.vista.move_sector.currentText()
        return (destino, sector)

    def resetEgreso(self):
        self.resetOperario()
        self.resetDetalles()

    def resetDetalles(self):
        self.vista.egr_numero.setText("")
        self.vista.move_destino.setCurrentIndex(0)

    def operacionCompletada(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Operacion realizada con éxito")
        msg.setWindowTitle("Mensaje de confirmación")
        retval = msg.exec_()
