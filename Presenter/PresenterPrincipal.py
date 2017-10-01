
from PyQt5 import QtWidgets
# from PyQt5.QtGui import
from PyQt5.QtCore import QModelIndex, QAbstractItemModel, QRegExp
from Vistas import VistaPrincipal
from Presenter import PresenterProveedor, PresenterArticulo, PresenterOperario, PresenterIngreso, PresenterEgreso

class PrincipalPresenter(QtWidgets.QWidget):

    def __init__(self):
        super(PrincipalPresenter, self).__init__()

        self.vista = VistaPrincipal.VistaPrincipal(self)

        pp = PresenterProveedor.ProveedorPresenter()
        pa = PresenterArticulo.ArticuloPresenter()
        po = PresenterOperario.OperarioPresenter()
        pi = PresenterIngreso.IngresoPresenter()
        pe = PresenterEgreso.EgresoPresenter()

        self.presenters = [ pa, pp, po, pi, pe]

        menu = {}

        self.contenido = self.vista.findChild(QtWidgets.QStackedWidget)

        # menu.selectionModel().currentChanged.connect(self.actualizarContenido)


        for index, pr in enumerate(self.presenters):
            if index == 3 or index == 4:
                self.contenido.insertWidget(index, pr.vistaDetalle)
            else:
                self.contenido.insertWidget(index, pr.vistaLista)



        self.vista.show()

        rx = QRegExp("btn_main_*")
        botones = self.vista.findChildren(QtWidgets.QPushButton, rx)

        # print("\n\nLA LISTA DE BOTONES ES LA SIGUIENTE: ")
        #
        # for boton in botones:
        #     texto = boton.text()
        #     boton.clicked.connect(self.actualizarContenido(texto))
        #     print("\n", boton.text())

        self.vista.btn_main_articulos.clicked.connect(self.mostrarArticulos)
        self.vista.btn_main_proveedores.clicked.connect(self.mostrarProveedores)
        self.vista.btn_main_operarios.clicked.connect(self.mostrarOperarios)
        self.vista.btn_main_ingresos.clicked.connect(self.mostrarIngresos)
        self.vista.btn_main_egresos.clicked.connect(self.mostrarEgresos)


    # def actualizarContenido(self, index):
    #     index = index.row()
    #     self.contenido = self.vista.self.contenido
    #
    #     self.contenido.setCurrentIndex(index)
    #     self.contenido.setMinimumSize(self.contenido.widget(self.contenido.currentIndex()).size())

        self.mostrarArticulos()

    def mostrarArticulos(self):
        self.contenido.setCurrentIndex(0) # Para DEBUG. Eliminar mas tarde

    def mostrarProveedores(self):
        self.contenido.setCurrentIndex(1) # Para DEBUG. Eliminar mas tarde

    def mostrarOperarios(self):
        self.contenido.setCurrentIndex(2) # Para DEBUG. Eliminar mas tarde

    def mostrarIngresos(self):
        self.contenido.setCurrentIndex(3) # Para DEBUG. Eliminar mas tarde

    def mostrarEgresos(self):
        self.contenido.setCurrentIndex(4) # Para DEBUG. Eliminar mas tarde
