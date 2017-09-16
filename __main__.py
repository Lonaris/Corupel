#__main__.py

import sys, os
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from Presenter import PresenterArticulo, PresenterProveedor, PresenterPrincipal

root = os.path.dirname(os.path.abspath(__file__))

def main():
	#Instancia para iniciar una aplicación
    app = QtWidgets.QApplication(sys.argv)

	#Instancia para iniciar una aplicación
    mainPresenter = PresenterPrincipal.PrincipalPresenter()
    # mainPresenter = Presenter.ArticuloPresenter()
    # mainPresenter = PresenterProveedor.ProveedorPresenter()



	#Ejecutar la aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
