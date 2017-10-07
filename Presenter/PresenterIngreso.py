# ingreso_presenter.py

import Vistas.Ingreso.VistaIngreso as IView
# import Modelos.ModeloIngreso as EModel
import Modelos.ModeloArticulo as AModel
import Modelos.ModeloIngreso as IModel
from PyQt5.QtCore import Qt, QModelIndex, QDate
import datetime

class IngresoPresenter(object):
    def __init__(self):
        # self.model = PModel.ModeloIngreso()
        self.vista = IView.IngresoView(self)
        self.model = IModel.ModeloIngreso()
        # self.vistaLista = PLView.ListaIngresosView(self)

        self.vista.tbl_ingresos.setModel(self.model)
        self.vista.tbl_ingresos.horizontalHeader().resizeSection(1, 300)
        self.model.dataChanged.connect(self.__sumador)
        # self.vistaLista.tbl_ingresos.doubleClicked.connect(self.verDetalles)

        # self.vista.btn_nuevo.clicked.connect(self.crearIngreso)
        # self.vista.btn_modificar.clicked.connect(self.modificarIngreso)
        # self.vista.btn_deshabilitar.clicked.connect(self.deshabilitarIngreso)

        # self.vistaLista.btn_buscar.clicked.connect(self.verIngresos)
        # self.vistaLista.btn_nuevo.clicked.connect(self.verNuevo)
        # self.verIngresos(limite = 5)

        # self.vista.elem_id.returnPressed.connect(self.__refrescar)

        self.vista.prov_id.returnPressed.connect(self.__buscarProveedor)

        hoy = datetime.date.today()

        self.vista.rem_fecha.setDate(QDate(hoy))
        self.vista.fact_fecha.setDate(QDate(hoy))
        # print(self.vista.rem_fecha.date())
        # self.activarBotones()

        self.vista.show()

    def verIngresos(self, campos = None, condiciones = None, limite = None):
        # texto = self.vistaLista.ln_buscar.text()
        texto = "'%{}%'".format(texto)
        condiciones = [('elem_nombre', ' LIKE ', texto)]
        # self.model.verListaIngresos(campos, condiciones, limite)

    def verNuevo(self):
        self.vista.resetIngreso()
        self.verDetalles()

    def verDetalles(self, ingreso = None):
        if ingreso:
            # ingreso = self.model.verDetallesIngreso(ingreso)
            self.vista.setIngreso(ingreso)
            # self.artModel.verListaArticulos(condiciones = [('elem_id', ' = ', ingreso[0])])

        self.vista.show()
        self.vista.activateWindow()

    def crearIngreso(self):
        ingreso = self.vista.getIngreso()
        ingreso['elem_id'] = None
        # self.model.crearIngreso(ingreso)

    def modificarIngreso(self):
        ingreso = self.vista.getIngreso()
        # self.model.modificarIngreso(ingreso)

    def __buscarProveedor(self):
        provId = self.vista.getProveedor()
        proveedor = {}

        if provId:
            proveedor = self.model.buscarProveedor(campos = ("prov_id", "prov_nombre"), condiciones = [("prov_id", " = ", provId)])
        if proveedor:
            self.vista.setProveedor(proveedor)
        else:
            self.vista.resetProveedor()

    def __refrescar(self):
        elemId = self.vista.elem_id.text()
        ingreso = {}
        if elemId:
            # ingreso = self.model.verDetallesIngreso(ingreso = QModelIndex(), condiciones = [('elem_id', ' = ', elemId)])
            # self.artModel.verListaArticulos(condiciones = [('elem_id', ' = ', elemId)])
            if ingreso:
                self.vista.setIngreso(ingreso)
        if not ingreso:
            self.vista.resetIngreso()

    def __sumador(self):
        self.__totalArticulos = 0
        self.__totalCosto = 0

        movimientos = self.model.getMovimientos()

        for movimiento in movimientos:
            if type(movimiento[2]) == str:
                continue
            self.__totalArticulos += movimiento[2]
            self.__totalCosto += movimiento[2] * movimiento[3]
        self.vista.setTotales(self.__totalArticulos, self.__totalCosto)
