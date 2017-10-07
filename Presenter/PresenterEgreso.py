# egreso_presenter.py

import Vistas.Egreso.VistaEgreso as EView
import Modelos.ModeloArticulo as AModel
import Modelos.ModeloEgreso as EModel
from PyQt5.QtCore import Qt, QModelIndex, QDate
import datetime


class EgresoPresenter(object):
    def __init__(self):
        # self.model = PModel.ModeloEgreso()
        self.vista = EView.EgresoView(self)
        self.model = EModel.ModeloEgreso()
        # self.vistaLista = PLView.ListaEgresosView(self)

        self.vista.tbl_egresos.setModel(self.model)
        self.vista.tbl_egresos.horizontalHeader().resizeSection(1, 300)
        self.model.dataChanged.connect(self.__sumador)
        # self.vistaLista.tbl_egresos.setModel(self.model)
        # self.vistaLista.tbl_egresos.doubleClicked.connect(self.verDetalles)

        # self.vista.btn_nuevo.clicked.connect(self.crearEgreso)
        # self.vista.btn_modificar.clicked.connect(self.modificarEgreso)
        # self.vista.btn_deshabilitar.clicked.connect(self.deshabilitarEgreso)

        # self.vistaLista.ln_buscar.returnPressed.connect(self.verEgresos)
        # self.vistaLista.btn_buscar.clicked.connect(self.verEgresos)
        # self.vistaLista.btn_nuevo.clicked.connect(self.verNuevo)
        # self.verEgresos(limite = 5)

        # self.vista.elem_id.returnPressed.connect(self.__refrescar)

        self.vista.ope_legajo.returnPressed.connect(self.__buscarOperario)

        hoy = datetime.date.today()

        self.vista.egr_fecha.setDate(QDate(hoy))
        self.vista.show()
        # self.activarBotones()

    def verEgresos(self, campos = None, condiciones = None, limite = None):
        # texto = self.vistaLista.ln_buscar.text()
        texto = "'%{}%'".format(texto)
        condiciones = [('elem_nombre', ' LIKE ', texto)]
        # self.model.verListaEgresos(campos, condiciones, limite)

    def verNuevo(self):
        self.vista.resetEgreso()
        self.verDetalles()

    def verDetalles(self, egreso = None):
        if egreso:
            # egreso = self.model.verDetallesEgreso(egreso)
            self.vista.setEgreso(egreso)
            # self.artModel.verListaArticulos(condiciones = [('elem_id', ' = ', egreso[0])])

        self.vista.show()
        self.vista.activateWindow()

    def crearEgreso(self):
        egreso = self.vista.getEgreso()
        egreso['elem_id'] = None
        # self.model.crearEgreso(egreso)

    def modificarEgreso(self):
        egreso = self.vista.getEgreso()
        # self.model.modificarEgreso(egreso)
        self.verEgresos()

    def deshabilitarEgreso(self):
        egreso = self.vista.getEgreso()
        # self.model.toggleEgresoActivo(egreso)

    def __refrescar(self):
        elemId = self.vista.elem_id.text()
        egreso = {}
        if elemId:
            # egreso = self.model.verDetallesEgreso(egreso = QModelIndex(), condiciones = [('elem_id', ' = ', elemId)])
            # self.artModel.verListaArticulos(condiciones = [('elem_id', ' = ', elemId)])
            if egreso:
                self.vista.setEgreso(egreso)
        if not egreso:
            self.vista.resetEgreso()

    def __buscarOperario(self):
        opeLeg = self.vista.getOperario()
        operario = {}

        if opeLeg:
            operario = self.model.buscarOperario(campos = ("ope_legajo", "ope_nombre"), condiciones = [("ope_legajo", " = ", opeLeg)])
        if operario:
            self.vista.setOperario(operario)
        else:
            self.vista.resetOperario()

    def __sumador(self):
        self.__totalArticulos = 0

        movimientos = self.model.getMovimientos()

        for movimiento in movimientos:
            if type(movimiento[2]) == str:
                continue
            self.__totalArticulos += movimiento[2]
        self.vista.setTotal(self.__totalArticulos)
