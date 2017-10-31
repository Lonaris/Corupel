# operario_view.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal, QRegExp, Qt

#Creamos la clase OperarioView
class OperarioView(QtWidgets.QWidget):
    rxOpe = QRegExp("ope_*")

	#Inicializamos el objeto
    def __init__(self, presenter, parent=None):
        super(OperarioView, self).__init__(parent)

        self.vistaDetalle = uic.loadUi("gui/detalles/operario_detalle.ui", self)
        self.vistaDetalle.btn_deshabilitar.hide()
        self.vistaDetalle.btn_imprimir.hide()


    #Funcion que trae un operario y modifica la ifnormacion.
    def getOperario(self):
        rawOperario = self.vistaDetalle.findChildren((QComboBox, QLineEdit, QLabel), self.rxOpe)
        operario = {}
        for componente in rawOperario:
            if "ope_" not in componente.objectName():
                continue
            if (type(componente) == QtWidgets.QComboBox):
                operario[componente.objectName()] = componente.currentText()
            else:
                operario[componente.objectName()] = componente.text()
        return operario

	#Funcion que carga un operario en particular dentro de "Detalle del Producto"
    def setOperario(self, operario):
        print (operario)
        self.vistaDetalle.ope_legajo.setText(str(operario[1]))
        self.vistaDetalle.ope_nombre.setText(operario[2])
        self.vistaDetalle.ope_apellido.setText(operario[3])
        self.vistaDetalle.ope_puesto.setText(operario[4])

    def resetOperario(self):
        camposAResetear = self.vistaDetalle.findChildren(QLineEdit, self.rxOpe)
        for campo in camposAResetear:
            campo.setText("")
                
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()



    
