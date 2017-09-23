# ingreso_presenter.py

import Vistas.Ingreso.VistaIngreso as IView
# import Modelos.ModeloIngreso as EModel
# import Modelos.ModeloArticulo as AModel
from PyQt5.QtCore import Qt, QModelIndex


class IngresoPresenter(object):
    def __init__(self):
        # self.model = PModel.ModeloIngreso()
        self.vistaDetalle = IView.IngresoView(self)
        # self.vistaLista = PLView.ListaIngresosView(self)

        # self.vistaLista.tbl_ingresos.setModel(self.model)
        # self.vistaLista.tbl_ingresos.doubleClicked.connect(self.verDetalles)

        # self.vistaDetalle.btn_nuevo.clicked.connect(self.crearIngreso)
        # self.vistaDetalle.btn_modificar.clicked.connect(self.modificarIngreso)
        # self.vistaDetalle.btn_deshabilitar.clicked.connect(self.deshabilitarIngreso)

        # self.vistaLista.ln_buscar.returnPressed.connect(self.verIngresos)
        # self.vistaLista.btn_buscar.clicked.connect(self.verIngresos)
        # self.vistaLista.btn_nuevo.clicked.connect(self.verNuevo)
        # self.verIngresos(limite = 5)

        # self.vistaDetalle.elem_id.returnPressed.connect(self.__refrescar)

        self.vistaDetalle.show()

        # self.activarBotones()

    def verIngresos(self, campos = None, condiciones = None, limite = None):
        # texto = self.vistaLista.ln_buscar.text()
        texto = "'%{}%'".format(texto)
        condiciones = [('elem_nombre', ' LIKE ', texto)]
        # self.model.verListaIngresos(campos, condiciones, limite)

    def verNuevo(self):
        self.vistaDetalle.resetIngreso()
        self.verDetalles()

    def verDetalles(self, ingreso = None):
        if ingreso:
            # ingreso = self.model.verDetallesIngreso(ingreso)
            self.vistaDetalle.setIngreso(ingreso)
            # self.artModel.verListaArticulos(condiciones = [('elem_id', ' = ', ingreso[0])])

        self.vistaDetalle.show()
        self.vistaDetalle.activateWindow()

    def crearIngreso(self):
        ingreso = self.vistaDetalle.getIngreso()
        ingreso['elem_id'] = None
        # self.model.crearIngreso(ingreso)

    def modificarIngreso(self):
        ingreso = self.vistaDetalle.getIngreso()
        # self.model.modificarIngreso(ingreso)
        self.verIngresos()

    def deshabilitarIngreso(self):
        ingreso = self.vistaDetalle.getIngreso()
        # self.model.toggleIngresoActivo(ingreso)

    def __refrescar(self):
        elemId = self.vistaDetalle.elem_id.text()
        ingreso = {}
        if elemId:
            # ingreso = self.model.verDetallesIngreso(ingreso = QModelIndex(), condiciones = [('elem_id', ' = ', elemId)])
            # self.artModel.verListaArticulos(condiciones = [('elem_id', ' = ', elemId)])
            if ingreso:
                self.vistaDetalle.setIngreso(ingreso)
        if not ingreso:
            self.vistaDetalle.resetIngreso()
