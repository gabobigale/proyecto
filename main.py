import conexiondb
import archivo
from tkinter import Tk, Label, Entry, Button, Toplevel, Scrollbar, CENTER, VERTICAL, HORIZONTAL, END
from tkinter.ttk import Progressbar, Treeview
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.messagebox import showinfo, showerror

class Interfaz:

    def __init__(self, ventana):

        # Inicializacion de controles en pantalla
        self.ventana = ventana
        self.ventana.title("Importar datos a tabla desde archivo")
        self.ventana.geometry("600x360")
        self.ventana.configure(background="SkyBlue4")
        self.ventana.resizable(0, 0)

        self.fileNamePath = None
        self.serverIp = str
        self.serverPort = int
        self.dbName = str
        self.tableName = str
        self.user = str
        self.password = str
        self.delimeter = str

        self.mensajeConexion = str

        self.fuenteTitles=('console', 14, 'bold')
        self.fuenteLabels=('courier', 12)
        self.fuenteButton=('courier', 12, 'bold')
        self.fuenteEntry=('courier', 12, 'bold')

        self.lblInfo1 = Label(
            ventana,
            text='SUBIR INFORMACION DE ARCHIVO A UNA BASE DE DATOS',
            bg='#0f4b6e',
            fg='white',
            font=self.fuenteTitles
        )

        self.lblInfo1.grid(row=0, columnspan=2)

        self.lblInfo2 = Label(
            ventana,
            text='INFORMACION DEL SERVIDOR Y DB',
            bg='#0f4b6e',
            fg='white',
            font=self.fuenteTitles
        )
        self.lblInfo2.grid(row=1, columnspan=2)

        self.lblServerIp = Label(
            ventana,
            text='Direccion del Servidor',
            bg='#0f4b6e',
            fg='white',
            font=self.fuenteLabels
        )
        self.txtServerIp = Entry(ventana, justify=CENTER, font=self.fuenteEntry)

        self.lblServerIp.grid(row=2, column=0, sticky="w")
        self.txtServerIp.grid(row=2, column=1, sticky="w")

        self.lblServerPort = Label(
            ventana,
            text='Puerto',
            bg='#0f4b6e',
            fg='white',
            font=self.fuenteLabels
        )
        self.txtServerPort = Entry(ventana, justify=CENTER, font=self.fuenteEntry)

        self.lblServerPort.grid(row=3, column=0, sticky="w")
        self.txtServerPort.grid(row=3, column=1, sticky="w")

        self.lblDbName = Label(
            ventana,
            text='Nombre de la Base de Datos',
            bg='#0f4b6e',
            fg='white',
            font=self.fuenteLabels
        )
        self.txtDbName = Entry(ventana, justify=CENTER, font=self.fuenteEntry)

        self.lblDbName.grid(row=4, column=0, sticky="w")
        self.txtDbName.grid(row=4, column=1, sticky="w")

        self.lblTableName = Label(
            ventana,
            text='Nombre de la Tabla',
            bg='#0f4b6e',
            fg='white',
            font=self.fuenteLabels
        )
        self.txtTableName = Entry(ventana, justify=CENTER, font=self.fuenteEntry)

        self.lblTableName.grid(row=5, column=0, sticky="w")
        self.txtTableName.grid(row=5, column=1, sticky="w")

        self.lblUser = Label(
            ventana,
            text='Usuario',
            bg='#0f4b6e',
            fg='white',
            font=self.fuenteLabels
        )
        self.txtUser = Entry(ventana, justify=CENTER, font=self.fuenteEntry)

        self.lblUser.grid(row=6, column=0, sticky="w")
        self.txtUser.grid(row=6, column=1, sticky="w")

        self.lblPass = Label(
            ventana,
            text='Contrasena',
            bg='#0f4b6e',
            fg='white',
            font=self.fuenteLabels
        )
        self.txtPass = Entry(ventana, show="*", justify=CENTER, font=self.fuenteEntry)

        self.lblPass.grid(row=7, column=0, sticky="w")
        self.txtPass.grid(row=7, column=1, sticky="w")

        self.lblDelimeter = Label(
            ventana,
            text='Caracter de Separacion/Delimitador',
            bg='#0f4b6e',
            fg='white',
            font=self.fuenteLabels
        )
        self.txtDelimenter = Entry(ventana, justify=CENTER, font=self.fuenteEntry)

        self.lblDelimeter.grid(row=8, column=0, sticky="w")
        self.txtDelimenter.grid(row=8, column=1, sticky="w")

        self.lblSelectFile = Label(
            ventana,
            text='Seleccionar archivo a subir',
            bg='#0f4b6e',
            fg='white',
            font=self.fuenteLabels
        )

        self.bSelectFile = Button(self.ventana,
                                  text="Seleccionar",
                                  font=self.fuenteButton,
                                  command=lambda: self.click("SelectOpenFile"))

        self.lblSelectFile.grid(row=9, column=0, sticky="w")
        self.bSelectFile.grid(row=9, column=1, sticky="w")

        self.lblSelectFilePath = Label(
            ventana,
            text='Ruta de Archivo: ',
            bg='#0f4b6e',
            fg='white',
            anchor="e",
            font=self.fuenteLabels
        )
        self.lblSelectFilePath.grid(row=10, column=0, columnspan=2, sticky="w")

        self.progressbar = Progressbar(
            self.ventana,
            orient=HORIZONTAL,
            length=100,
            mode='determinate'
        )
        self.progressbar.grid(row=11, column=0, sticky="e")

        self.lblprogress = Label(
            self.ventana,
            text='0%',
            bg='#345',
            fg='#fff',
            font=self.fuenteLabels
        )
        self.lblprogress.grid(row=11, column=1, sticky="w")

        self.bSelectFileSave = Button(self.ventana,
                                      text="Subir",
                                      height=2,
                                      width=10,
                                      font=self.fuenteButton,
                                      command=lambda: self.click("SelectFileSave"))
        self.bSelectFileSave.grid(row=12, column=0, sticky="w")

        self.bDownloadFile = Button(self.ventana,
                                    text="Descargar",
                                    height=2,
                                    width=10,
                                    font=self.fuenteButton,
                                    command=lambda: self.click("DownloadFile"))
        self.bDownloadFile.grid(row=12, column=1, sticky="w")

    def click(self, operacion):

        if (operacion == "SelectOpenFile"):
            self.updateProgressBar(0)
            self.open_file()
            if self.fileNamePath is not None:
                self.lblSelectFilePath.configure(text="Ruta de Archivo: " + self.fileNamePath.name)
            else:
                self.lblSelectFilePath.configure(text="Ruta de Archivo: No se ha seleccionado el archivo. ")

        elif (operacion == "SelectFileSave"):

            if self.fileNamePath is not None:
                self.updateProgressBar(20)
                if self.validaEntry():
                    self.updateProgressBar(40)
                    self.mensajeConexion, baseautos, boolLectura = archivo.leer_archivo(self.fileNamePath.name,
                                                                                        self.txtDelimenter.get())
                    if boolLectura:

                        self.updateProgressBar(60)

                        db = conexiondb.dataconnection()
                        db.setDataConnection(
                            self.txtServerIp.get(),
                            self.txtServerPort.get(),
                            self.txtDbName.get(),
                            self.txtTableName.get(),
                            self.txtUser.get(),
                            self.txtPass.get()
                        )

                        self.mensajeConexion, boolExisteTabla = db.existetabla()

                        if boolExisteTabla:
                            self.updateProgressBar(80)

                            datosValidos, datosError = self.validaDatosSubir(baseautos)
                            self.mensajeConexion, boolInserta = db.insertar(datosValidos)

                            self.updateProgressBar(100)

                            showinfo(title="Mensaje", message=self.mensajeConexion)
                        else:
                            showerror(title="Error", message=self.mensajeConexion)
                    else:
                        showerror(title="Error", message=self.mensajeConexion)
            else:
                showerror(title="Error", message="No se ha seleccionado el archivo. ")

        elif (operacion == "DownloadFile"):
            self.updateProgressBar(0)

            db = conexiondb.dataconnection()
            db.setDataConnection(
                self.txtServerIp.get(),
                self.txtServerPort.get(),
                self.txtDbName.get(),
                self.txtTableName.get(),
                self.txtUser.get(),
                self.txtPass.get()
            )

            self.mensajeConexion, boolExisteTabla = db.existetabla()

            if boolExisteTabla:

                self.mensajeConexion, datosBusqueda, boolBusqueda = db.buscar()

                if boolBusqueda:
                    self.openNewWindow(datosBusqueda)
                else:
                    showerror(title="Error", message="Error: " + self.mensajeConexion)
            else:
                showerror(title="Error", message=self.mensajeConexion)

    def validaEntry(self):
        if len(self.txtServerIp.get()) == 0 \
                or len(self.txtServerPort.get()) == 0 \
                or len(self.txtDbName.get()) == 0 \
                or len(self.txtTableName.get()) == 0 \
                or len(self.txtUser.get()) == 0 \
                or len(self.txtPass.get()) == 0 \
                or len(self.txtDelimenter.get()) == 0:

            showerror(title="Error", message="Error: Todos los datos deben ser ingresados.")
            return False
        else:
            try:
                self.serverIp = str(self.txtServerIp.get())
                self.serverPort = int(self.txtServerPort.get())  # verificar isdigit isnumeric
                self.dbName = str(self.txtDbName.get())
                self.tableName = str(self.txtTableName.get())
                self.user = str(self.txtUser.get())
                self.password = str(self.txtPass.get())
                self.delimeter = str(self.txtDelimenter.get())
                return True
            except Exception as e:
                showerror(title="Error", message="Error en el ingreso de los datos: " + str(e))
                return False

    def validaDatosSubir(self, datos):
        datosValidos = []
        datosError = []

        for row in datos:
            try:
                empresa = str(row[0])
                anio = int(row[1])
                montoventa = float(row[2])
                mercado = int(row[3])
                cantidad = int(row[4])

                listrow = [empresa, anio, montoventa, mercado, cantidad]

                datosValidos.append(tuple(listrow))
            except:
                datosError.append(row)

        return datosValidos, datosError

    def open_file(self):
        self.fileNamePath = askopenfile(mode='r', filetypes=[('CSV Files', '*csv')])

        if self.fileNamePath is not None:
            pass

    def updateProgressBar(self, progress):
        self.progressbar['value'] = progress
        self.lblprogress['text'] = self.progressbar['value'], '%'

    def openNewWindow(self, mostrardatos):

        self.ventana.newwindow = Toplevel(ventana)
        self.ventana.newwindow.title("Informacion Ingresada en tabla")
        self.ventana.newwindow.geometry("1050x350")
        self.ventana.newwindow.configure(background="SkyBlue4")
        self.ventana.newwindow.resizable(0, 0)

        lblInfo1 = Label(
            self.ventana.newwindow,
            text='INFORMACION DE TABLA',
            bg='#0f4b6e',
            fg='white',
            justify="left",
            anchor="e",
            font=self.fuenteTitles
        )

        lblInfo1.grid(row=0, columnspan=3)

        # Generacion de Grid
        columns = ('#1', '#2', '#3', '#4', '5')
        tree = Treeview(self.ventana.newwindow , columns=columns, show='headings')

        tree.heading('#1', text='Empresa')
        tree.heading('#2', text='Anio')
        tree.heading('#3', text='Monto Venta')
        tree.heading('#4', text='Mercado')
        tree.heading('#5', text='Cantidad')

        tree.grid(row=2, columnspan=3, sticky='nsew')

        scrollbar = Scrollbar(self.ventana.newwindow , orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=4, sticky='ns')

        totalRegistros = 0
        for row in mostrardatos:
            totalRegistros+=1
            tree.insert('', END, values=row)

        lblInfo2 = Label(
            self.ventana.newwindow ,
            text='Total Registros: ' + str(totalRegistros),
            bg='#0f4b6e',
            fg='white',
            justify="left",
            anchor="e",
            font=self.fuenteLabels
        )

        lblInfo2.grid(row=3)

        bSaveFile = Button(self.ventana.newwindow ,
                           text="Guardar CSV",
                           height=2,
                           width=12,
                           font=self.fuenteButton,
                           command=lambda: click("SaveFile"))
        bSaveFile.grid(row=4, sticky="e")


        def click(opcion):
            if opcion == "SaveFile":
                file_save()

        def file_save():
            saveFileNamePath = asksaveasfile(mode='w', filetypes=[('CSV Files', '*csv')])
            if saveFileNamePath is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                return

            mensaje, boolEscritura = archivo.escribir_archivo(saveFileNamePath.name,
                                                              self.txtDelimenter.get(),
                                                              mostrardatos)

            if boolEscritura:
                showinfo(title="Mensaje", message="Archivo creado en la ruta: " + saveFileNamePath.name)
            else:
                showerror(title="Error", message="Error: " + mensaje)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ventana = Tk()                          # Asginación del módulo Tk
    condatabasewindow = Interfaz(ventana)   # Inicializacion de la interfaz
    ventana.mainloop()                      # abre la interfaz gráfica y mantiene la ejecución
