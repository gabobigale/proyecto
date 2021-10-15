import psycopg2

class dataconnection(object):

    def __init__(self):
        self.__serverip = str
        self.__port = int
        self.__databasename = str
        self.__tablename = str
        self.__user = str
        self.__password = str

    def setDataConnection(self, serverip, port, databasename, tablename, user, password):
        self.__serverip = serverip
        self.__port = port
        self.__databasename = databasename
        self.__tablename = tablename
        self.__user = user
        self.__password = password

    def conexionbd(self):
        try:
            conn = psycopg2.connect(
                database=self.__databasename,
                user=self.__user,
                password=self.__password,
                host=self.__serverip,
                port=self.__port)
            return conn
        except:
            return "Error"

    def existetabla(self):

        conexion = self.conexionbd()
        if conexion != "Error":
            try:
                cursor = conexion.cursor()
                sql = "select exists(select * from information_schema.tables where table_name='"+self.__tablename+"')"

                cursor.execute(sql)
                result = cursor.fetchone()[0]

                cursor.close()
                conexion.close()

                if result:
                    return result, True
                else:
                    return "Tabla ingresada no existe en la base de datos.", False
            except (Exception, psycopg2.Error) as e:
                return "Error en la busqueda de los registros: " + str(e), False
        else:
            return "Error en la conexion a la base de datos", False

    def buscar(self):

        conexion = self.conexionbd()
        
        if conexion != "Error":
            try:

                cursor = conexion.cursor()

                sql = "SELECT empresa, anio, montoventa, mercado, cantidad FROM public." + self.__tablename + ";"

                cursor.execute(sql)
                result = cursor.fetchall()

                cursor.close()
                conexion.close()
                return "OK", result, True
            except (Exception, psycopg2.Error) as e:
                return "Error en la busqueda de los registros: " + str(e), "", False
        else:
            return "Error en la conexion a la base de datos", "", False

    def insertar(self, datos):

        conexion = self.conexionbd()

        if conexion != "Error":
            try:
                cursor = conexion.cursor()

                sql = "INSERT INTO public." + self.__tablename + \
                """(
                    empresa, anio, montoventa, mercado, cantidad)
                    VALUES (%s, %s, %s, %s, %s);
                """
                cursor.executemany(sql, datos)
                conexion.commit()
                return "Datos ingresados correctamente " + str(cursor.rowcount), True

                cursor.close()
                conexion.close()
            except (Exception, psycopg2.Error) as e:
                return "Error en el ingreso de los registros: " + str(e), False
        else:
            return "Error en la conexion a la base de datos", False