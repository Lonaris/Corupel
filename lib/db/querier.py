# querier.py
import mysql.connector
from mysql.connector import errorcode
# import config

class Querier(object):

    tabla = ""
    prefijo = ""

    def __init__(self, tabla, prefijo = ""):
        self.prefijo = self.prefijo
        self.tabla = tabla

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

    def actualizarElemento(self, elemento):
        if type(elemento) != type({}):
            raise TypeError("Solo se pueden actualizar elementos del tipo diccionario")
            return
        consulta = "UPDATE {} SET ".format(self.tabla)
        donde = "WHERE "
        for index, columna in enumerate(elemento.keys()):
            if "id" in columna.lower():
                print("La columna: " + columna + " fue ignorada")
                if self.prefijo in columna.lower():
                    donde += "{}{} = %({}{})s".format(self.prefijo, columna, self.prefijo, columna)
                continue
            consulta += "{}{} = %({}{})s".format(self.prefijo,columna,self.prefijo,columna)
            if len(elemento)-1 != index:
                consulta += ", "
            else:
                consulta += "\n"
        consulta += donde

        print("\nDEBUG - Consulta actualizar elemento a mysql: ", consulta , "\n")
        self.__consultar(consulta, elemento)

    def __consultar(self, consulta, elemento):
# Debo levantar estos elementos (usr, pword, host, dbase) de un archivo .ini.
# Si el archivo .ini no existe debo crearlo. Estos datos se deben guardar
# de forma encriptada y luego desencriptar al usarlo.
        db = mysql.connector.connect(
            # user = config.usr, password = config.pword,
            # host = config.hst, database = config.dbase
            user = "root", password = "admin1234",
            host = "127.0.0.1", database = "corupel"
            )

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
