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
        self.vista.btn_ejecutar.clicked.connect(self.ejecutarInforme)

        self.iniciarFecha()

        self.vista.show()

        self.__filtros = {
            'tipo' : '',
            'busqueda' : '',
            'desde' : '',
            'hasta' : '',
            'tercero' : '',
            'destino' : '',
            'agrupacion' : ''
        }

    def iniciarFecha(self):
        hoy = date.today()
        desde = {}
        dia = hoy.day
        for a in range(5):
            try:
                desde = date(hoy.year, hoy.month-1, dia)
                break
            except:
                dia -= 1
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

        desde = date(filtros[5].year(), filtros[5].month(), filtros[5].day())
        hasta = date(filtros[6].year(), filtros[6].month(), filtros[6].day())
        self.__filtros['tipo'] = filtros[0]
        self.__filtros['destino'] = filtros[1]
        if not filtros[2] == 'Agrupacion':
            self.__filtros['agrupacion'] = filtros[2]
        else: self.__filtros['agrupacion'] = None
        self.__filtros['busqueda'] = filtros[4]
        try:
            self.__filtros['tercero'] = int(filtros[3])
        except:
            self.__filtros['tercero'] = None
        self.__filtros['desde'] = desde
        self.__filtros['hasta'] = hasta

        print(self.__filtros)
