# querier.py
import mysql.connector
from mysql.connector import errorcode
# import config

class Querier(object):

    tabla = ""
    prefijo = ""

    conexion = {}

    def __init__(self, tabla, prefijo = ""):
        self.prefijo = self.prefijo
        self.tabla = tabla

        self.user = "root"
        self.password = "admin1234"
        self.host = "127.0.0.1"
        self.database = "corupel"


# Esta funcion recibe un diccionario donde key = columna y value = valor
    def insertarElemento(self, elemento):
        # if type(elemento) != type({}) or type(elemento) != type([]):
        #     raise TypeError("El elemento a insertar debe ser un diccionario o lista")
        #     return
        consulta = "INSERT INTO {} (".format(self.tabla)
        valores = "VALUES ("
        for index, columna in enumerate(elemento.keys()):
            consulta += self.prefijo + columna
            valores += "%({})s".format(columna)
            if len(elemento) - 1 != index:
                consulta += ", "
                valores += ", "
        valores += ")"
        consulta += ") " + valores

        print("\nDEBUG - Consulta de insertar elemento:\n", consulta, "\n\n", elemento, "\n")
        self.__consultar(consulta, elemento)

    def actualizarElemento(self, elemento, condiciones = None):
        if type(elemento) != type({}):
            raise TypeError("Solo se pueden actualizar elementos del tipo diccionario")
            return
        if condiciones == None:
            raise TypeError("No se puede actualizar un elemento sin proporcionar su id")
            return

        consulta = "UPDATE {} SET ".format(self.tabla)

        donde = ""

        total = len(elemento)

        for index, columna in enumerate(elemento.keys()):
            if (self.prefijo + "id") in columna.lower():
                # print("La columna: " + columna + " fue ignorada")
                total -= 1
                donde = self.agregarFiltros(columna, " = ", columna)
                # donde += "{}{} = %({}{})s".format(self.prefijo, columna, self.prefijo, columna)
                continue
            consulta += "{}{} = %({}{})s".format(self.prefijo,columna,self.prefijo,columna)
            if index < total-1:
                consulta += ", "
            else:
                consulta += "\n"

        # if condiciones:
        #     donde = self.__agregarFiltros(condiciones)
        # else:
        #     donde = self.__agregarFiltros()
        consulta += donde

        print("\nDEBUG - Consulta actualizar elemento a mysql: ", consulta , "\n")
        self.__consultar(consulta, elemento)

    def existeElemento(self, elemento):
        # consulta =
        pass


    def traerElementos(self, campos = None, condiciones = None, limite = None):
        donde = ""
        consulta = "SELECT "


        # totalCondiciones = len(condiciones)

        if not campos:
            consulta += "* "
        else:
            totalCampos = len(campos)
            for index, campo in enumerate(campos):
                consulta += "{}".format(campo)

                if index != totalCampos -1:
                    consulta += ", "

        consulta += " FROM {} ".format(self.tabla)

        if condiciones:
            donde = self.__agregarFiltros(condiciones)
        consulta += donde

        if limite:
            consulta += " LIMIT {}".format(limite)

        print("DEBUG - CONSULTA PARA VER ELEMENTOS: ", consulta)

        db = self.__conectar()
        cursor = db.cursor()

        cursor.execute(consulta)
        respuesta = cursor.fetchall()

        # print (respuesta)

        cursor.close()
        db.close()

        # listaRespuesta = [[]]
        # for index, cosa in enumerate(respuesta):
        #     listaRespuesta.append([])
        #     for cosita in cosa:
        #         listaRespuesta[index].append(cosita)
        #
        # print (respuesta)
        # return listaRespuesta
        return respuesta

    def __agregarFiltros(self, filtros):
        donde = "\nWHERE "

        totalFiltros = len(filtros)

        for index, filtro in enumerate(filtros):
            campo, condicion, valor = filtro
            donde += "{} {} {}".format(campo, condicion, valor)
            # campo + condicion + valor
            if index < totalFiltros-1:
                donde += ", "
        # donde += campo + condicion + "%({})s".campo

        return donde

    def __conectar(self):
        con = mysql.connector.connect(
            user = self.user, password = self.password,
            host = self.host, database = self.database)
        return con

    def __consultar(self, consulta, elemento):
        db = self.__conectar()
        cursor = db.cursor()
        try:
            if (type(elemento) != type({})):
                cursor.executeMany(consulta, elemento)
            else:
                cursor.execute(consulta, elemento)
            db.commit()
        except mysql.connector.Error as error:
            print("No se logro insertar el registro: ", error)
            db.rollback()
        cursor.close()
        db.close()
