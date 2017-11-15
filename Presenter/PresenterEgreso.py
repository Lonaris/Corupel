# egreso_presenter.py

import Vistas.Egreso.VistaEgreso as EView
import Modelos.ModeloArticulo as AModel
import Modelos.ModeloEgreso as EModel
import Modelos.ModeloDestino as DModel
from PyQt5.QtCore import Qt, QModelIndex, QDate
import datetime


class EgresoPresenter(object):
    def __init__(self):
        # self.model = PModel.ModeloEgreso()
        self.vista = EView.EgresoView(self)
        self.model = EModel.ModeloEgreso()
        self.desModel = DModel.ModeloDestino()
        self.artModel = AModel.ModeloArticulo(propiedades = ["Codigo", "Descripcion", "Stock"]) #Agregar Stock
        # self.vistaLista = PLView.ListaEgresosView(self)

        self.vista.tbl_egresos.setModel(self.model)
        self.model.dataChanged.connect(self.__sumador)
        self.vista.move_destino.setModel(self.desModel)
        # self.vistaLista.tbl_egresos.setModel(self.model)
        # self.vistaLista.tbl_egresos.doubleClicked.connect(self.verDetalles)
        self.vista.tbl_articulos.setModel(self.artModel)

        self.vista.btn_buscar.clicked.connect(self.__buscarArticulosDisponibles)
        self.vista.btn_guardar.clicked.connect(self.crearEgreso)

        self.vista.ope_legajo.returnPressed.connect(self.__buscarOperario)
        self.headerPrincipal = self.vista.tbl_egresos.horizontalHeader()
        # hoy = datetime.date.today()
        #
        # self.vista.egr_fecha.setDate(QDate(hoy))
        self.__reiniciarFecha()
        self.vista.show()
        # self.activarBotones()
        self.__redimensionarTablaPrincipal()

    def verEgresos(self, campos = None, condiciones = None, limite = None):
        # texto = self.vistaLista.ln_buscar.text()
        texto = "'%{}%'".format(texto)
        condiciones = [('elem_nombre', ' LIKE ', texto)]
        # self.model.verListaEgresos(campos, condiciones, limite)

    def verNuevo(self):
        self.vista.resetEgreso()
        self.artModel.reiniciarTabla()
        self.verDetalles()

    def verDetalles(self, egreso = None):
        if egreso:
            # egreso = self.model.verDetallesEgreso(egreso)
            self.vista.setEgreso(egreso)
            # self.artModel.verListaArticulos(condiciones = [('elem_id', ' = ', egreso[0])])

        self.vista.show()
        self.vista.activateWindow()

    def crearEgreso(self):
        operario = self.vista.getOperario()
        detalles = self.vista.getDetalles()

        if not operario[1]:
            print("ERROR, falta operario")
            return False
        if not detalles[0]:
            print("ERROR, falta destino")
            return False

        print("CREO EL EGRESO")

        if self.model.crearEgreso(operario[0], detalles):
            self.restarStockAticulos()
            self.reiniciarMenu()

    def modificarEgreso(self):
        egreso = self.vista.getEgreso()
        # self.model.modificarEgreso(egreso)
        self.verEgresos()

    def deshabilitarEgreso(self):
        egreso = self.vista.getEgreso()
        # self.model.toggleEgresoActivo(egreso)

    def restarStockAticulos(self):
        articulos = self.model.getArticulos()
        print (articulos)
        for articulo in articulos:
            stock_actual = self.artModel.verDetallesArticulo(campos = ["art_stock_actual"], condiciones = [("art_id", "=", articulo[0])])
            articulo = {
                "art_id" : articulo[0],
                "art_stock_actual" : stock_actual[0] - articulo[1]
            }
            print("/n/nSTOCK PREVIO A LA RESTA DE STOCK ACTUAL: ", stock_actual[0])
            print("/n/nSTOCK ACTUAL ACTUAL: ", articulo["art_stock_actual"])
            articulo = self.artModel.modificarArticulo(articulo)
            self.__redimensionarTablaBusqueda()
        self.__redimensionarTablaBusqueda()

    def __buscarArticulosDisponibles(self):

        destino = self.vista.move_destino.currentIndex()
        descripcion = self.vista.buscador.text()
        condiciones = [("art_stock_actual", ">", 0), ("art_descripcion", "LIKE", "'%{}%'".format(descripcion))]
        if  destino != 0:
            condiciones.append(("art_destino", "=", destino))
        self.artModel.verListaArticulos(condiciones = condiciones)
        self.__redimensionarTablaBusqueda()

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
            self.artModel.reiniciarTabla()

    def __buscarOperario(self):
        operario = self.vista.getOperario()
        opeLeg = operario[0]
        operario = {}

        if opeLeg:
            operario = self.model.buscarOperario(campos = ("ope_legajo", "ope_nombre"), condiciones = [("ope_legajo", " = ", opeLeg)])
        if operario:
            self.vista.setOperario(operario)
        else:
            self.vista.resetOperario()
        # self.__redimensionarTablaPrincipal()

    def __sumador(self):
        self.__totalArticulos = 0

        movimientos = self.model.getMovimientos()

        for movimiento in movimientos:
            if type(movimiento[2]) == str:
                continue
            self.__totalArticulos += movimiento[2]
        self.vista.setTotal(self.__totalArticulos)

    def reiniciarMenu(self):
        self.vista.resetEgreso()
        self.artModel.reiniciarTabla()
        self.model.reiniciarTablaEgreso()
        self.__reiniciarFecha()

    def __reiniciarFecha(self):
        hoy = datetime.date.today()

        self.vista.egr_fecha.setDate(QDate(hoy))

    def __redimensionarTablaPrincipal(self):
        self.headerPrincipal.resizeSection(0, 50)
        self.headerPrincipal.resizeSection(2, 100)
        self.headerPrincipal.setSectionResizeMode(1, 1)

    def __redimensionarTablaBusqueda(self):
        self.headerBusqueda = self.vista.tbl_articulos.horizontalHeader()

        self.headerBusqueda.resizeSection(0, 50)
        self.headerBusqueda.resizeSection(2, 50)
        self.headerBusqueda.setSectionResizeMode(1, 1)
