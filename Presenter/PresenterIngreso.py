# ingreso_presenter.py

import Vistas.Ingreso.VistaIngreso as IView
# import Modelos.ModeloIngreso as EModel
import Modelos.ModeloArticulo as AModel
import Modelos.ModeloIngreso as IModel
from PyQt5.QtCore import Qt, QModelIndex, QDate
from PyQt5 import QtWidgets
import datetime

class IngresoPresenter(object):
    def __init__(self):
        # self.model = PModel.ModeloIngreso()
        self.vista = IView.IngresoView(self)
        self.model = IModel.ModeloIngreso()
        self.artModel = AModel.ModeloArticulo(propiedades = ["Codigo", "Descripcion"])
        # self.vistaLista = PLView.ListaIngresosView(self)

        self.vista.tbl_ingresos.setModel(self.model)
        self.model.dataChanged.connect(self.__sumador)
        # self.vistaLista.tbl_ingresos.doubleClicked.connect(self.verDetalles)

        self.vista.tbl_articulos.setModel(self.artModel)
        self.vista.btn_guardar.clicked.connect(self.crearIngreso)
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
        proveedor = self.vista.getProveedor()
        comprobantes = self.vista.getComprobantes()

        resultados = []

        for comprobante in comprobantes:
            resultado = {}
            for componente in comprobante:
                if type(componente) == QtWidgets.QLineEdit:
                    resultado[componente.objectName()] = componente.text()
                if type(componente) == QtWidgets.QComboBox:
                    resultado[componente.objectName()] = componente.currentText()
                if type(componente) == QtWidgets.QDateEdit:
                    resultado[componente.objectName()] = componente.date().toString("yyyy-MM-dd")
            resultados.append(resultado)
        comprobantes = []

        if not proveedor:
            print("ERROR, falta proveedor")
            return (False)

        if not self.model.hayMovimientos():
            print("NO HAY MOVIMIENTOS")
            return False

        if not (resultados[1]['fact_numero'] and resultados[1]['fact_prefijo']):
            resultados.pop(1)
        else:
            comprobantes.append( { 'comp_numero' : resultados[1]['fact_numero'],
                'comp_prefijo' : resultados[1]['fact_tipo'] + resultados[1]['fact_prefijo'],
                'comp_fecha' : resultados[1]['fact_fecha'] })

        if not (resultados[0]['rem_numero'] and resultados[0]['rem_prefijo']):
            resultados.pop(0)
        else:
            comprobantes.append( { 'comp_numero' : resultados[0]['rem_numero'],
                'comp_prefijo' : resultados[0]['rem_tipo'] + resultados[0]['rem_prefijo'],
                'comp_fecha' : resultados[0]['rem_fecha'] })

        if not comprobantes:
            return False

        self.model.crearIngreso(proveedor, comprobantes)

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
            self.artModel.verListaArticulos(condiciones = [("articulos_de_proveedores.proveedor", " = ", provId)],
                campos = ["art_id", "art_descripcion"],
                union = ['articulos_de_proveedores', '`articulos`.`art_id` = `articulos_de_proveedores`.`articulo`'])
            # self.artModel.verListaArticulos(campos = ["art_id", "art_descripcion"], condiciones = [('articulos_de_proveedores.proveedor', ' = ', provId)], union = ['articulos_de_proveedores', '`proveedores`.`prov_id` = `articulos_de_proveedores`.`proveedor`'] )
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
