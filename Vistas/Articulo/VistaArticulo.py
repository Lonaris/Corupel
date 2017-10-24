# articulo_view.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox, QLabel, QCheckBox, QGridLayout, QMessageBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import pyqtSignal, QRegExp, Qt

#Creamos la clase ArticuloView
class ArticuloView(QtWidgets.QWidget):

    rxArt = QRegExp("art_*")


	#Inicializamos el objeto
    def __init__(self, presenter, parent=None):
        super(ArticuloView, self).__init__(parent)

        #Traemos el archivo .UI "Articulos_detalle"
        self.vistaDetalle = uic.loadUi("vistas/gui/detalles/articulo_detalle.ui", self)

        rxId = QRegExp("[0-9]{0,16}")
        rxBarras = QRegExp(".{0,20}")
        rxDesc = QRegExp(".{0,30}")

        self.agrupacion = ('Insumos', 'Reparacion', 'Inversion')

        self.vistaDetalle.art_id.setValidator(QRegExpValidator(rxId))
        self.vistaDetalle.art_cod_barras.setValidator(QRegExpValidator(rxBarras))
        self.vistaDetalle.art_descripcion.setValidator(QRegExpValidator(rxDesc))

        self.vistaDetalle.art_id.textChanged.connect(self.__activarBotones)

        self.__activarBotones("")

        self.__haCambiado = False

# Las siguientes líneas son para conectar los eventos en los
# que los campos son modificados, en caso de modificarse alguno
# levanto una bandera que me indica que se modificó un campo

        self.vistaDetalle.art_id.textChanged.connect(self.__articuloHaCambiado)
        self.vistaDetalle.art_cod_barras.textChanged.connect(self.__articuloHaCambiado)
        self.vistaDetalle.art_descripcion.textChanged.connect(self.__articuloHaCambiado)
        self.vistaDetalle.art_marca.currentIndexChanged.connect(self.__articuloHaCambiado)
        self.vistaDetalle.art_agrupacion.currentIndexChanged.connect(self.__articuloHaCambiado)
        self.vistaDetalle.art_stock_minimo.textChanged.connect(self.__articuloHaCambiado)

    #Funcion que trae un articulo y modifica la ifnormacion.
    # def getArticulo(self):
    #     rawArticulo = self.vistaDetalle.findChildren((QComboBox, QLineEdit, QLabel), self.rxArt)
    #     articulo = {}
    #     for componente in rawArticulo:
    #         if "art_" not in componente.objectName():
    #             continue
    #         if (type(componente) == QtWidgets.QComboBox):
    #             articulo[componente.objectName()] = componente.currentText()
    #             # print(componente.objectName(), componente.currentText())
    #         else:
    #             articulo[componente.objectName()] = componente.text()
    #             # print(componente.objectName(), componente.text())
    #     print ("\nDEBUG - ARTICULO: ", articulo)
    #     return articulo

    def getArticulo(self):
        rawArticulo = self.vistaDetalle.findChildren((QLineEdit, QCheckBox, QComboBox), self.rxArt)
        articulo = {}
        for componente in rawArticulo:
                if type(componente) == QLineEdit:
                    articulo[componente.objectName()] = componente.text()
                if type(componente) == QComboBox:
                    articulo[componente.objectName()] = componente.currentText()
                if type(componente) == QCheckBox:
                    articulo[componente.objectName()] = componente.isChecked()
                # print(componente.objectName(), componente.text())
        if (articulo['art_id']):
            articulo['art_id'] = int(articulo['art_id'])
        if articulo['art_stock_minimo']:
            articulo['art_stock_minimo'] = int(articulo['art_stock_minimo'])

        # if (articulo['art_activo']):
        #     articulo['art_activo'] = 1
        # else:
        #     articulo['art_activo'] = 0

        return articulo


	#Funcion que carga un articulo en particular dentro de "Detalle del Producto"
    def setArticulo(self, articulo):
        print (articulo)
        self.vistaDetalle.art_id.setText(str(articulo[0]))
        # self.vistaDetalle.prov_nombre.setText(str(articulo[1]))
        self.vistaDetalle.art_cod_barras.setText(articulo[1])
        self.vistaDetalle.art_descripcion.setText(articulo[2])
        self.vistaDetalle.art_marca.setCurrentText(articulo[3])
        self.vistaDetalle.art_agrupacion.setCurrentText(articulo[4])
        self.vistaDetalle.art_stock_minimo.setText(str(articulo[5]))
        # self.vistaDetalle.art_activo.setEnabled()

# Cuando seteo un artículo, la bandera debe ponerse en FALSO
        self.__haCambiado = False

    def resetArticulo(self):
        self.vistaDetalle.art_id.setText("")
        # self.vistaDetalle.prov_nombre.setText("")
        self.vistaDetalle.art_cod_barras.setText("")
        self.vistaDetalle.art_descripcion.setText("")
        self.vistaDetalle.art_marca.setCurrentText("")
        self.vistaDetalle.art_agrupacion.setCurrentText("Insumos")
        self.vistaDetalle.art_stock_minimo.setText("")
        self.vistaDetalle.comp_costo.setText("")
        self.vistaDetalle.comp_stock_actual.setText("")

# Cuando pongo todos los campos en blanco (no es una modificacion
#de usuario), debo poner la bandera en FALSO
        self.__haCambiado = False

    def errorDeCampo(self, descripcion):
        label = QLabel(descripcion)
        layout = self.vistaDetalle.box_articulo.findChild(QGridLayout)
        layout.addWidget(label)

    def setTotales(self, totales):
        if totales:
            self.vistaDetalle.comp_stock_actual.setText(str(totales.pop(0)))
            # self.vistaDetalle.comp_costo.addItems(totales)

    def __activarBotones(self, snl):
        if snl:
            self.vistaDetalle.btn_nuevo.setEnabled(False)
            self.vistaDetalle.btn_modificar.setEnabled(True)
        else:
            self.vistaDetalle.btn_nuevo.setEnabled(True)
            self.vistaDetalle.btn_modificar.setEnabled(False)

    def __articuloHaCambiado(self):
        self.__haCambiado = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

# El evento de cerrar ventana se dispara y verifica
# que no haya sido modificado ningún campo

    def closeEvent(self, event):
        if not self.__haCambiado:
            event.accept()
            return
        resultado = QMessageBox.question(self, "Salir..", "¿Desea cancelar el ingreso del nuevo articulo? No se guardaran los registros", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes: event.accept()
        else: event.ignore()
