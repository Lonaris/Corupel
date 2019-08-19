# informe_presenter.py

import Vistas.VistaInforme as InView
import Modelos.ModeloInforme as InModel
import Modelos.ModeloDestino as DModel
import Modelos.ModeloProveedor as PModel
from datetime import date

import csv
import xlwt
from PyQt5.QtWidgets import QFileDialog

class InformePresenter(object):
    def __init__(self):
        self.model = InModel.ModeloInforme()
        self.desModel = DModel.ModeloDestino()
        self.provModel = PModel.ModeloProveedor(propiedades = ["Nombre"])
        self.vista = InView.InformeView(self)
        self.vista.tbl_informe.setModel(self.model)

        self.vista.filtro_destino_av.setModel(self.desModel)
        self.vista.filtro_proveedor_av.setModel(self.provModel)
        self.vista.btn_ejecutar_sp.clicked.connect(self.ejecutarInformeSp)
        self.vista.btn_ejecutar_av.clicked.connect(self.ejecutarInformeAv)
        self.vista.btn_guardar.clicked.connect(self.handleSaveXls)

        self.iniciarFecha()
        self.__verProveedores()

        self.vista.show()

        self.__filtros = {
            'tipo' : '',
            'articulo' : '',
            'desde' : '',
            'hasta' : '',
            'operario' : '',
            'proveedor' : '',
            'destino' : '',
            'agrupacion' : ''
        }

    def iniciarFecha(self):
        hoy = date.today()
        desde = {}
        anio = hoy.year
        mes = hoy.month
        dia = 1

        desde = date(anio, mes, dia)

        self.vista.setFechas(desde, hoy)

    def ejecutarInformeSp(self):
        self.prepararFiltrosSp()
        self.model.traerInforme(self.__filtros)

    def ejecutarInformeAv(self):
        self.prepararFiltrosAv()
        self.model.traerInforme(self.__filtros)

    def prepararFiltrosSp(self):
        filtros = self.vista.getFiltrosSp()
        desde = date(filtros['desde'].year(), filtros['desde'].month(), filtros['desde'].day())
        hasta = date(filtros['hasta'].year(), filtros['hasta'].month(), filtros['hasta'].day())
        filtros['desde'] = desde
        filtros['hasta'] = hasta
        self.__filtros = filtros

    def prepararFiltrosAv(self):
        filtros = self.vista.getFiltrosAv()
        desde = date(filtros['desde'].year(), filtros['desde'].month(), filtros['desde'].day())
        hasta = date(filtros['hasta'].year(), filtros['hasta'].month(), filtros['hasta'].day())
        filtros['desde'] = desde
        filtros['hasta'] = hasta
        self.__filtros = filtros

    def handleSave(self):
        path = QFileDialog.getSaveFileName(
                None, 'Save File', '', 'CSV(*.csv)')
        if path[0]:
            with open(path[0], 'wt') as stream:
                writer = csv.writer(stream)

                #Encabezado
                desde = "Desde {}".format(self.__filtros['desde'])
                hasta = "Hasta {}".format(self.__filtros['hasta'])

                writer.writerow([desde, hasta])
                header = self.model.getHeader()
                writer.writerow(header)

                #Columnas de los datos
                for row in range(self.model.rowCount(None)):
                    rowdata = []
                    for column in range(self.model.columnCount(None)):
                        item = self.model.informe[row][column]
                        teext = str(item).encode('utf-8')
                        rowdata.append(item)
                    writer.writerow(rowdata)

    def handleSaveXls(self):
        path = QFileDialog.getSaveFileName(
                None, 'Save File', '', 'Excel(*.xls)')
        if not path[0]:
            return
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Informe - Corupel')

        desde = "Desde {}".format(self.__filtros['desde'])
        hasta = "Hasta {}".format(self.__filtros['hasta'])

        ws.write(0, 0, desde)
        ws.write(0, 2, hasta)

        header = self.model.getHeader()

        for index, item in enumerate(header):
            ws.write(1, index, item)

        for row in range(self.model.rowCount(None)):
            for column in range(self.model.columnCount(None)):
                item = self.model.informe[row][column]
                ws.write(row+2, column, item)

        wb.save(path[0])

    def __verProveedores(self):
        orden = ("prov_nombre", "ASC")
        self.provModel.verListaProveedores(orden = orden)
        self.provModel.agregarNone()
