# informe_presenter.py

import Vistas.VistaInforme as InView
import Modelos.ModeloInforme as InModel
import Modelos.ModeloDestino as DModel
from datetime import date

class InformePresenter(object):
    def __init__(self):
        self.model = InModel.ModeloInforme()
        self.desModel = DModel.ModeloDestino()
        self.vista = InView.InformeView(self)
        self.vista.tbl_informe.setModel(self.model)

        self.vista.filtro_destino.setModel(self.desModel)
        self.vista.buscador.returnPressed.connect(self.ejecutarInforme)
        self.vista.btn_ejecutar.clicked.connect(self.ejecutarInforme)

        self.iniciarFecha()

        self.vista.show()

        self.__filtros = {
            'tipo' : '',
            'busqueda' : '',
            'desde' : '',
            'hasta' : '',
            'tercero' : ''
        }

    def iniciarFecha(self):
        hoy = date.today()
        desde = date(hoy.year, hoy.month-1, hoy.day)
        self.vista.setFechas(desde, hoy)

    def ejecutarInforme(self):
        self.prepararFiltros()
        self.model.traerInforme(self.__filtros)

    def prepararFiltros(self):
        filtros = self.vista.getFiltros()

# Los valores para el filtro 'tipo' son:
# 0 - Ingreso de Artículos
# 1 - Egreso de Artículos
# 2 - Ingreso de Artículos por Proveedor
# 3 - Egreso de Artículos por Operario

        desde = date(filtros[2].year(), filtros[2].month(), filtros[2].day())
        hasta = date(filtros[3].year(), filtros[3].month(), filtros[3].day())
        self.__filtros['tipo'] = filtros[0]
        self.__filtros['busqueda'] = filtros[1]
        self.__filtros['desde'] = desde
        self.__filtros['hasta'] = hasta
        self.__filtros['tercero'] = filtros[4]
