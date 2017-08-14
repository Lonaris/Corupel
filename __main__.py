import sys, os
#from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui, QtCore, uic, QtWidgets
import Presenter.PresenterArticulo as APresenter
# import Vistas.VistaPrincipal as VPrincipal

root = os.path.dirname(os.path.abspath(__file__))

def main():
    app = QtWidgets.QApplication(sys.argv)

    mainPresenter = APresenter.ArticuloPresenter()

    # main = VPrincipal.VistaPrincipal(mainPresenter)
    # main.show()
    mainPresenter.vista.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#
#     uic = uic.loadUi("inventory2.ui")
#     uic.show()
#
#     sys.exit(app.exec_())
