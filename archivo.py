import csv

# Módulo manipulación de archivo
def leer_archivo(archivopath, separador):
    # define una lista
    lista = []

    # apertura el archivo
    with open(archivopath) as File:
        try:
            # lee el archivo con su delimitador
            reader = csv.reader(File, delimiter=separador)

            # lee linea y se agrega la tupla a la lista
            for row in reader:
                lista.append(tuple(row))

            # se destruye objetos file, reader
            del reader
            File.close()

            return "OK", lista, True
        except Exception as e:
            return "Ha ocurrido un error en la lectura del archivo." + str(e), "", False

def escribir_archivo(archivopath, separador, datos):

    # apertura el archivo
    with open(archivopath, "a", newline="") as File:
        try:
            # escritura de archivo con su delimitador
            writer = csv.writer(File, delimiter=separador)

            # escribe filas en archivo
            writer.writerows(datos)

            # se destruye objetos file, writer
            del writer
            File.close()

            return "Archivo creado correctamente.", True
        except Exception as e:
            return "Ha ocurrido un error en la escritura del archivo." + str(e), False