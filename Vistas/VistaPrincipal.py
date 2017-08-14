from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QStringListModel
from Vistas import VistaArticulo

class VistaPrincipal(QtWidgets.QMainWindow):

    def __init__(self, proto):
        super(VistaPrincipal, self).__init__()

        data = ["Ingreso de Factura", "Salida de articulos", "Articulos", "Informes", "Operarios", "Configuracion"]
        # data = {"Ingreso de Factura" : 0,
        # "Salida de articulos" : 1,
        # "Articulos" : 2,
        # "Informes" : 3,
        # "Operarios" : 4,
        # "Configuracion" : 5}
        model = QStringListModel(data)

        main = uic.loadUi("Vistas/main.ui", self)
        main.menu_navegacion.setModel(model)


        vistaArticulo = VistaArticulo.ArticuloView(proto)
        print(main.menu_navegacion.currentIndex())
        main.contenido.addWidget(vistaArticulo)
        main.contenido.setCurrentIndex(2)
