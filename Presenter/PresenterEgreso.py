# egreso_presenter.py

import Vistas.Egreso.VistaEgreso as EView
# import Modelos.ModeloEgreso as EModel
# import Modelos.ModeloArticulo as AModel
from PyQt5.QtCore import Qt, QModelIndex


class EgresoPresenter(object):
    def __init__(self):
        # self.model = PModel.ModeloEgreso()
        self.vistaDetalle = EView.EgresoView(self)
        # self.vistaLista = PLView.ListaEgresosView(self)

        # self.vistaLista.tbl_egresos.setModel(self.model)
        # self.vistaLista.tbl_egresos.doubleClicked.connect(self.verDetalles)

        # self.vistaDetalle.btn_nuevo.clicked.connect(self.crearEgreso)
        # self.vistaDetalle.btn_modificar.clicked.connect(self.modificarEgreso)
        # self.vistaDetalle.btn_deshabilitar.clicked.connect(self.deshabilitarEgreso)

        # self.vistaLista.ln_buscar.returnPressed.connect(self.verEgresos)
        # self.vistaLista.btn_buscar.clicked.connect(self.verEgresos)
        # self.vistaLista.btn_nuevo.clicked.connect(self.verNuevo)
        # self.verEgresos(limite = 5)

        # self.vistaDetalle.elem_id.returnPressed.connect(self.__refrescar)

        self.vistaDetalle.show()

        # self.activarBotones()

    def verEgresos(self, campos = None, condiciones = None, limite = None):
        # texto = self.vistaLista.ln_buscar.text()
        texto = "'%{}%'".format(texto)
        condiciones = [('elem_nombre', ' LIKE ', texto)]
        # self.model.verListaEgresos(campos, condiciones, limite)

    def verNuevo(self):
        self.vistaDetalle.resetEgreso()
        self.verDetalles()

    def verDetalles(self, egreso = None):
        if egreso:
            # egreso = self.model.verDetallesEgreso(egreso)
            self.vistaDetalle.setEgreso(egreso)
            # self.artModel.verListaArticulos(condiciones = [('elem_id', ' = ', egreso[0])])

        self.vistaDetalle.show()
        self.vistaDetalle.activateWindow()

    def crearEgreso(self):
        egreso = self.vistaDetalle.getEgreso()
        egreso['elem_id'] = None
        # self.model.crearEgreso(egreso)

    def modificarEgreso(self):
        egreso = self.vistaDetalle.getEgreso()
        # self.model.modificarEgreso(egreso)
        self.verEgresos()

    def deshabilitarEgreso(self):
        egreso = self.vistaDetalle.getEgreso()
        # self.model.toggleEgresoActivo(egreso)

    def __refrescar(self):
        elemId = self.vistaDetalle.elem_id.text()
        egreso = {}
        if elemId:
            # egreso = self.model.verDetallesEgreso(egreso = QModelIndex(), condiciones = [('elem_id', ' = ', elemId)])
            # self.artModel.verListaArticulos(condiciones = [('elem_id', ' = ', elemId)])
            if egreso:
                self.vistaDetalle.setEgreso(egreso)
        if not egreso:
            self.vistaDetalle.resetEgreso()
