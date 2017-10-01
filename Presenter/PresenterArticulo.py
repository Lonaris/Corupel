# articulo_presenter.py


import Vistas.Articulo.VistaArticulo as AView
import Vistas.Articulo.VistaListaArticulos as ALView
import Modelos.ModeloArticulo as AModel
from PyQt5.QtCore import Qt


class ArticuloPresenter(object):
    def __init__(self):
        self.model = AModel.ModeloArticulo()
        self.vistaDetalle = AView.ArticuloView(self)
        self.vistaLista = ALView.ListaArticuloView(self)

        self.vistaLista.tbl_articulos.setModel(self.model)
        self.vistaLista.tbl_articulos.doubleClicked.connect(self.verDetalles)

        self.vistaDetalle.btn_nuevo.clicked.connect(self.crearArticulo)
        self.vistaDetalle.btn_modificar.clicked.connect(self.modificarArticulo)
        self.vistaDetalle.btn_deshabilitar.clicked.connect(self.deshabilitarArticulo)

        self.vistaLista.btn_nuevo.clicked.connect(self.nuevoArticulo)
        self.vistaLista.ln_buscar.returnPressed.connect(self.verArticulos)
        self.vistaLista.btn_buscar.clicked.connect(self.verArticulos)

        self.vistaLista.show()

    def verArticulos(self, campos = None, condiciones = None, limite = None):
        texto = self.vistaLista.ln_buscar.text()
        texto = "'%{}%'".format(texto)
        condiciones = [('art_descripcion', ' LIKE ', texto)]
        self.model.verListaArticulos(campos, condiciones, limite)


    def verDetalles(self, articulo):

        articulo = self.model.verDetallesArticulo(articulo)
        self.vistaDetalle.setArticulo(articulo)
        self.vistaDetalle.show()
        self.vistaDetalle.activateWindow()

    def crearArticulo(self, articulo):
        # print("DEBUG - Tipo de objeto de artículo_ ", type(articulo))
        articulo['art_id'] = None
        self.model.crearArticulo(articulo)

    def modificarArticulo(self, articulo):
        self.model.modificarArticulo(articulo)

    def deshabilitarArticulo(self, articulo):

        articulo = {articulo.objectName() : articulo.text()}
        print(articulo)

        self.model.deshabilitarArticulo(articulo)

    def nuevoArticulo(self):
        self.vistaDetalle.resetArticulo()
        self.vistaDetalle.show()
