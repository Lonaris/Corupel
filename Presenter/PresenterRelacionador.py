# PresenterRelacionador.py

import Vistas.VistaRelacionador as RView
import Modelos.ModeloRelacionador as RModel

class RelacionadorPresenter(object):
    def __init__(self, tipo):
        self.model = RModel.ModeloRelacionador()
        self.vista = RView.RelacionadorView(self)
        self.vista.tabla_objetos.setModel(self.model)

        self.vista.buscador.returnPressed.connect(self.buscar)

        self.model.setTipo(tipo)
        self.vista.setTitulo(tipo)

    def buscar(self):
        pass
