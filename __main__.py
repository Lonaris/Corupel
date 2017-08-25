import sys, os
from PyQt5 import QtGui, QtCore, uic, QtWidgets
import Presenter.PresenterArticulo as APresenter

root = os.path.dirname(os.path.abspath(__file__))

#Creamos una funcion denominada "main" que ejecuta la aplicacion.
def main():
    app = QtWidgets.QApplication(sys.argv)

    mainPresenter = APresenter.ArticuloPresenter()

    # main = VPrincipal.VistaPrincipal(mainPresenter)
    # main.show()
    # mainPresenter.vistaDetalle.show()
    # mainPresenter.vistaLista.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
