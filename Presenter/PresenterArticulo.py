# articulo_presenter.py

import Vistas.Articulo.VistaArticulo as AView
import Vistas.Articulo.VistaListaArticulos as ALView
import Modelos.ModeloArticulo as AModel
from PyQt5.QtCore import Qt, QModelIndex


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
        self.vistaDetalle.art_id.returnPressed.connect(self.__refrescar)

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

    def crearArticulo(self):
        # print("DEBUG - Tipo de objeto de artículo_ ", type(articulo))
        print("ESTO ANDA")
        articulo = self.vistaDetalle.getArticulo()
        print("DEBUG - Artículo: ", articulo)
        articulo['art_id'] = None
        # error =
        self.model.crearArticulo(articulo)
        self.verArticulos()
        # if error:
        #     self.vistaDetalle.errorDeCampo(error)
        # else:
        #     self.vistaDetalle.articuloGuardado()

    def modificarArticulo(self):
        articulo = self.vistaDetalle.getArticulo()
        self.model.modificarArticulo(articulo)
        self.verArticulos()

    def deshabilitarArticulo(self, articulo):

        articulo = {articulo.objectName() : articulo.text()}
        print(articulo)

        self.model.deshabilitarArticulo(articulo)

    def nuevoArticulo(self):
        self.vistaDetalle.resetArticulo()
        self.vistaDetalle.show()

    def __refrescar(self):
        artId = self.vistaDetalle.art_id.text()
        articulo = {}
        if artId:
            print("DEBUG - ART_ID = ", artId)
            articulo = self.model.verDetallesArticulo(articulo = QModelIndex(), condiciones = [('art_id', ' = ', artId)])
            # self.artModel.verListaProveedores(condiciones = [('art_id', ' = ', artId)])
            if articulo:
                self.vistaDetalle.setArticulo(articulo)
        if not articulo:
            self.vistaDetalle.resetArticulo()
    #
    # def confirmarSalir(self):
    #     # IMPLEMENTAR
    #     pass
    #
    # def confirmarGuardar(self):
    #     # IMPLEMENTAR
    #     pass
