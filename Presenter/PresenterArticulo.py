# articulo_presenter.py

import Vistas.Articulo.VistaArticulo as AView
import Vistas.Articulo.VistaListaArticulos as ALView
import Modelos.ModeloArticulo as AModel
import Modelos.ModeloProveedor as PModel
import Modelos.ModeloDestino as DModel
import Presenter.PresenterRelacionador as RPresenter
from PyQt5.QtCore import Qt, QModelIndex


class ArticuloPresenter(object):
    def __init__(self):
        self.provModel = PModel.ModeloProveedor(propiedades = ["Codigo", "Nombre", "Teléfono"])
        self.model = AModel.ModeloArticulo(propiedades = ["Codigo", "Descripcion", "Marca"])
        self.desModel = DModel.ModeloDestino()

        self.vistaDetalle = AView.ArticuloView(self)
        self.vistaLista = ALView.ListaArticuloView(self)

        self.relacionador = RPresenter.RelacionadorPresenter("proveedores", self)

        self.vistaLista.tbl_articulos.setModel(self.model)
        self.vistaLista.tbl_articulos.doubleClicked.connect(self.verDetalles)

        self.vistaDetalle.btn_nuevo.clicked.connect(self.crearArticulo)
        self.vistaDetalle.btn_modificar.clicked.connect(self.modificarArticulo)
        self.vistaDetalle.btn_deshabilitar.clicked.connect(self.deshabilitarArticulo)
        self.vistaDetalle.art_id.returnPressed.connect(self.refrescar)
        self.vistaDetalle.tbl_proveedores.setModel(self.provModel)
        self.vistaDetalle.opcion_costo.currentIndexChanged.connect(self.__actualizarCostos)
        self.vistaDetalle.art_destino.setModel(self.desModel)

        self.vistaDetalle.btn_nuevo_prov.clicked.connect(self.__asociar)

        self.vistaLista.btn_nuevo.clicked.connect(self.nuevoArticulo)
        self.vistaLista.ln_buscar.returnPressed.connect(self.verArticulos)
        self.vistaLista.btn_buscar.clicked.connect(self.verArticulos)

        self.model.verListaArticulos()

        self.vistaLista.show()

    def verArticulos(self, campos = None, condiciones = None, limite = None):
        texto = self.vistaLista.ln_buscar.text()
        texto = "'%{}%'".format(texto)
        condiciones = [('art_descripcion', ' LIKE ', texto)]
        self.model.verListaArticulos(campos, condiciones, limite)

    def verDetalles(self, articulo):
        if articulo:
            articulo = self.model.verDetallesArticulo(articulo)
            cantidades = self.model.verCantidadesArticulo(condiciones = [('movimientos_ingreso.art_id', ' = ', articulo[0]), ('movimientos_ingreso.movi_restante', ' > ', 0)])
            totales = []
            if cantidades:
                totales = self.__calcularTotales(cantidades)

            self.vistaDetalle.setArticulo(articulo)
            self.vistaDetalle.setTotales(totales)
            self.__actualizarCostos()
            self.provModel.verListaProveedores(condiciones = [("articulos_de_proveedores.articulo", " = ", articulo[0])], campos = ["prov_id", "prov_nombre", "prov_telefono"], uniones = [['articulos_de_proveedores', '`proveedores`.`prov_id` = `articulos_de_proveedores`.`proveedor`']])

        self.vistaDetalle.show()
        self.vistaDetalle.activateWindow()

    def crearArticulo(self):
        # print("DEBUG - Tipo de objeto de artículo_ ", type(articulo))
        print("ESTO ANDA")
        articulo = self.vistaDetalle.getArticulo()
        print("DEBUG - Artículo: ", articulo)
        articulo['art_id'] = None
        # error =
        if self.model.crearArticulo(articulo):
            self.verArticulos()
            #Crear la funcion resetCambios que pone el estado de cambios en False
            self.vistaDetalle.resetCambios()
            #Cierra la Ventana
            self.vistaDetalle.close()
        # if error:
        #     self.vistaDetalle.errorDeCampo(error)
        # else:
        #     self.vistaDetalle.articuloGuardado()

    def modificarArticulo(self):
        articulo = self.vistaDetalle.getArticulo()
        if self.model.modificarArticulo(articulo):
            self.verArticulos()
            self.vistaDetalle.resetCambios()
            self.vistaDetalle.close()

    def deshabilitarArticulo(self, articulo):

        articulo = {articulo.objectName() : articulo.text()}
        print(articulo)

        self.model.deshabilitarArticulo(articulo)

    def nuevoArticulo(self):
        self.vistaDetalle.resetArticulo()
        self.vistaDetalle.show()

    def refrescar(self):
        artId = self.vistaDetalle.art_id.text()
        articulo = {}
        if artId:
            print("DEBUG - ART_ID = ", artId)
            articulo = self.model.verDetallesArticulo(condiciones = [('art_id', ' = ', artId)])
            cantidades = self.model.verCantidadesArticulo(condiciones = [('movimientos_ingreso.art_id', ' = ', artId)])
            totales = {}
            if cantidades:
                totales = self.__calcularTotales(cantidades)

            self.provModel.verListaProveedores(condiciones = [("articulos_de_proveedores.articulo", " = ", artId)],
                campos = ["prov_id", "prov_nombre", "prov_telefono"],
                uniones = [['articulos_de_proveedores', '`proveedores`.`prov_id` = `articulos_de_proveedores`.`proveedor`']])
            if articulo:
                self.vistaDetalle.setArticulo(articulo)
                if totales:
                    self.vistaDetalle.setTotales(totales)
        if not articulo:
            self.vistaDetalle.resetArticulo()

    def __calcularTotales(self, cantidades):
        totalCantidad = 0
        promedioCosto = 0
        ultimo = len(cantidades) - 1

        for cantidad in cantidades:
            totalCantidad += cantidad[0]
            promedioCosto += cantidad[1]

        promedioCosto /= len(cantidades)
        primerCosto = cantidades[0][1]
        ultimoCosto = cantidades[ultimo][1]

        return [totalCantidad, primerCosto, promedioCosto, ultimoCosto]

    def __actualizarCostos(self):
        index = self.vistaDetalle.opcion_costo.currentIndex()
        if index == 0:
            self.vistaDetalle.comp_costo.setText(self.model.primerCosto())
        elif index == 1:
            self.vistaDetalle.comp_costo.setText(self.model.ultimoCosto())
        elif index == 2:
            self.vistaDetalle.comp_costo.setText(self.model.CostoPromedio())

    def __asociar(self):
        idArticulo = self.model.getId()
        print("idArticulo contiene lo siguiente: ", idArticulo)
        self.relacionador.activar(idArticulo)
    #
    # def confirmarSalir(self):
    #     # IMPLEMENTAR
    #     pass
    #
    # def confirmarGuardar(self):
    #     # IMPLEMENTAR
    #     pass
