
from PyQt5 import QtWidgets
from PyQt5.QtCore import QModelIndex, QAbstractItemModel
from Vistas import VistaPrincipal
from Presenter import PresenterProveedor, PresenterArticulo, PresenterOperario

class PrincipalPresenter(QtWidgets.QWidget):

    def __init__(self):
        super(PrincipalPresenter, self).__init__()

        self.vista = VistaPrincipal.VistaPrincipal(self)

        pp = PresenterProveedor.ProveedorPresenter()
        pa = PresenterArticulo.ArticuloPresenter()
        po = PresenterOperario.OperarioPresenter()
        self.presenters = [ pp, pa, po]

        menu = self.vista.menu_navegacion
        contenido = self.vista.contenido

        menu.selectionModel().currentChanged.connect(self.actualizarContenido)

        for index, pr in enumerate(self.presenters):
            contenido.insertWidget(index, pr.vistaLista)

        self.vista.show()


    def actualizarContenido(self, index):
        index = index.row()
        contenido = self.vista.contenido

        contenido.setCurrentIndex(index)
        contenido.setMinimumSize(contenido.widget(contenido.currentIndex()).size())
