# articulo_presenter.py
import Vistas.VistaArticulo as AView
import Modelos.ModeloArticulo as AModel

class ArticuloPresenter(object):
    def __init__(self):
        self.model = AModel.ModeloArticulo({})
        self.vista = AView.ArticuloView(self)
        # self.interactor = interactor

        self.vista.senialCrearArticulo.connect(self.crearArticulo)
        self.vista.senialModificarArticulo.connect(self.modificarArticulo)
        self.vista.senialDeshabilitarArticulo.connect(self.deshabilitarArticulo)


    def fetchArticles(self):
        #self.articulos =
        pass

    def crearArticulo(self, articulo):
        # print("DEBUG - Tipo de objeto de artículo_ ", type(articulo))
        self.model.crearArticulo(articulo)

    def modificarArticulo(self, articulo):
        self.model.modificarArticulo(articulo)

    def deshabilitarArticulo(self, articulo):

        articulo = {articulo.objectName() : articulo.text()}
        print(articulo)

        self.model.deshabilitarArticulo(articulo)
