
from PyQt5 import QtWidgets
from PyQt5.QtCore import QModelIndex, QAbstractItemModel, QRegExp
from Vistas import VistaPrincipal
from Presenter import PresenterProveedor, PresenterArticulo, PresenterOperario, PresenterIngreso, PresenterEgreso, PresenterInforme

class PrincipalPresenter(QtWidgets.QWidget):

    def __init__(self):
        super(PrincipalPresenter, self).__init__()

        self.vista = VistaPrincipal.VistaPrincipal(self)

        pp = PresenterProveedor.ProveedorPresenter()
        pa = PresenterArticulo.ArticuloPresenter()
        po = PresenterOperario.OperarioPresenter()
        pi = PresenterIngreso.IngresoPresenter()
        pe = PresenterEgreso.EgresoPresenter()
        pin = PresenterInforme.InformePresenter()

        self.presenters = [ pa, pp, po, pi, pe, pin]

        menu = {}

        self.contenido = self.vista.findChild(QtWidgets.QStackedWidget)

        for index, pr in enumerate(self.presenters):
            if index == 3 or index == 4 or index == 5:
                self.contenido.insertWidget(index, pr.vista)
            else:
                self.contenido.insertWidget(index, pr.vistaLista)

        self.vista.showMaximized()

        rx = QRegExp("btn_main_*")
        botones = self.vista.findChildren(QtWidgets.QPushButton, rx)

        self.vista.btn_main_articulos.clicked.connect(self.mostrarArticulos)
        self.vista.btn_main_proveedores.clicked.connect(self.mostrarProveedores)
        self.vista.btn_main_operarios.clicked.connect(self.mostrarOperarios)
        self.vista.btn_main_ingresos.clicked.connect(self.mostrarIngresos)
        self.vista.btn_main_egresos.clicked.connect(self.mostrarEgresos)
        self.vista.btn_main_informes.clicked.connect(self.mostrarInformes)

        self.vista.btn_main_configuracion.hide()
        self.vista.btn_main_destinos.hide()

        self.contenido.currentChanged.connect(self.limpiarInterfaz)

        statusBar = self.vista.statusBar().showMessage("Barra de mensajes")

        self.mostrarArticulos()

    def mostrarArticulos(self):
        self.contenido.setCurrentIndex(0)

    def mostrarProveedores(self):
        self.contenido.setCurrentIndex(1)

    def mostrarOperarios(self):
        self.contenido.setCurrentIndex(2)

    def mostrarIngresos(self):
        self.contenido.setCurrentIndex(3)

    def mostrarEgresos(self):
        self.contenido.setCurrentIndex(4)

    def mostrarInformes(self):
        self.contenido.setCurrentIndex(5)

    def limpiarInterfaz(self):
        self.presenters[3].reiniciarMenu()
        self.presenters[4].reiniciarMenu()
