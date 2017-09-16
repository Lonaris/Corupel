# proveedor_presenter.p

import Vistas.Proveedor.VistaProveedor as PView
import Vistas.Proveedor.VistaListaProveedores as PLView
import Modelos.ModeloProveedor as PModel
import Modelos.ModeloArticulo as AModel
from PyQt5.QtCore import Qt, QModelIndex


class ProveedorPresenter(object):
    def __init__(self):
        self.artModel = AModel.ModeloArticulo(propiedades = ["Codigo de Barras", "Descripcion"])
        self.model = PModel.ModeloProveedor()
        self.vistaDetalle = PView.ProveedorView(self)
        self.vistaLista = PLView.ListaProveedoresView(self)

        self.vistaLista.tbl_proveedores.setModel(self.model)
        self.vistaLista.tbl_proveedores.doubleClicked.connect(self.verDetalles)

        self.vistaDetalle.btn_nuevo.clicked.connect(self.crearProveedor)
        self.vistaDetalle.btn_modificar.clicked.connect(self.modificarProveedor)
        # self.vistaDetalle.btn_deshabilitar.clicked.connect(self.deshabilitarProveedor)

        self.vistaLista.ln_buscar.returnPressed.connect(self.verProveedores)
        self.vistaLista.btn_buscar.clicked.connect(self.verProveedores)
        self.vistaLista.btn_nuevo.clicked.connect(self.verNuevo)
        # self.verProveedores(limite = 5)

        self.vistaDetalle.prov_id.returnPressed.connect(self.__refrescar)

        self.vistaDetalle.tbl_articulos.setModel(self.artModel)
        self.selMod = self.vistaDetalle.tbl_articulos.selectionModel()
        self.selMod.selectionChanged.connect(self.activarBotonesArticulos)

        self.vistaLista.show()

        self.activarBotonesArticulos()

    def verProveedores(self, campos = None, condiciones = None, limite = None):
        texto = self.vistaLista.ln_buscar.text()
        texto = "'%{}%'".format(texto)
        condiciones = [('prov_nombre', ' LIKE ', texto)]
        self.model.verListaProveedores(campos, condiciones, limite)

    def verNuevo(self):
        self.vistaDetalle.resetProveedor()
        self.verDetalles()

    def verDetalles(self, proveedor = None):
        if proveedor:
            proveedor = self.model.verDetallesProveedor(proveedor)
            self.vistaDetalle.setProveedor(proveedor)
            self.artModel.verListaArticulos(condiciones = [('prov_id', ' = ', proveedor[0])])

        self.vistaDetalle.show()
        self.vistaDetalle.activateWindow()

    def crearProveedor(self):
        proveedor = self.vistaDetalle.getProveedor()
        proveedor['prov_id'] = None
        self.model.crearProveedor(proveedor)

    def modificarProveedor(self):
        proveedor = self.vistaDetalle.getProveedor()
        self.model.modificarProveedor(proveedor)
        self.verProveedores()

    def deshabilitarProveedor(self):
        proveedor = self.vistaDetalle.getProveedor()
        self.model.toggleProveedorActivo(proveedor)

    def __refrescar(self):
        provId = self.vistaDetalle.prov_id.text()
        proveedor = {}
        if provId:
            proveedor = self.model.verDetallesProveedor(proveedor = QModelIndex(), condiciones = [('prov_id', ' = ', provId)])
            self.artModel.verListaArticulos(condiciones = [('prov_id', ' = ', provId)])
            if proveedor:
                self.vistaDetalle.setProveedor(proveedor)
        if not proveedor:
            self.vistaDetalle.resetProveedor()

    def activarBotonesArticulos(self):
        if self.selMod.hasSelection():
            self.vistaDetalle.btn_deshabilitar_art.setEnabled(True)
        else:
            self.vistaDetalle.btn_deshabilitar_art.setEnabled(False)
