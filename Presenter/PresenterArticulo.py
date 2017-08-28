# articulo_presenter.py


import Vistas.VistaArticulo as AView
import Vistas.VistaListaArticulos as ALView
import Modelos.ModeloArticulo as AModel
from PyQt5.QtCore import Qt


class ArticuloPresenter(object):
    def __init__(self):
        self.model = AModel.ModeloArticulo()
        self.vistaDetalle = AView.ArticuloView(self)
        self.vistaLista = ALView.ListaArticuloView(self)
        # self.interactor = interactor

        self.vistaLista.tbl_articulos.setModel(self.model)
        self.vistaLista.tbl_articulos.doubleClicked.connect(self.verDetalles)

        self.vistaDetalle.senialCrearArticulo.connect(self.crearArticulo)
        self.vistaDetalle.senialModificarArticulo.connect(self.modificarArticulo)
        self.vistaDetalle.senialDeshabilitarArticulo.connect(self.deshabilitarArticulo)

        self.vistaLista.senialBuscarArticulo.connect(self.verArticulos)

        # self.verArticulos(limite = 5)

        self.vistaLista.show()

    def verArticulos(self, campos = None, condiciones = None, limite = None):
        texto = self.vistaLista.ln_buscar.text()
        texto = "'%{}%'".format(texto)
        condiciones = [('art_descripcion', ' LIKE ', texto)]
        self.model.verListaArticulos(campos, condiciones, limite)


    def verDetalles(self, articulo):

        articulo = self.model.verDetallesArticulo(articulo)
        # self.vistaLista.tbl_articulos.setEnabled(False)
        self.vistaDetalle.setArticulo(articulo)
        self.vistaDetalle.show()
        self.vistaDetalle.activateWindow()

    def crearArticulo(self, articulo):
        # print("DEBUG - Tipo de objeto de artículo_ ", type(articulo))
        self.model.crearArticulo(articulo)

    def modificarArticulo(self, articulo):
        self.model.modificarArticulo(articulo)

    def deshabilitarArticulo(self, articulo):

        articulo = {articulo.objectName() : articulo.text()}
        print(articulo)

        self.model.deshabilitarArticulo(articulo)
