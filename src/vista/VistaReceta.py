from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class VistaReceta(QWidget):
    #Ventana de receta

    def __init__(self,interfaz):
        """
        Constructor de la ventana
        """   
        super().__init__()

        self.titulo = 'Recetario- Receta'
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.interfaz=interfaz
        self.receta = None
        self.ingredientes_receta = None

        self.width = 500
        self.height = 450
        self.inicializar_GUI()
        self.show()
       

    def inicializar_GUI(self):

        # inicializamos la ventana
        self.setWindowTitle(self.titulo)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))

        self.distribuidor_base = QVBoxLayout(self)

        self.widget_id = QWidget()
        self.distribuidor_receta = QGridLayout()
        self.widget_id.setLayout(self.distribuidor_receta)
        self.distribuidor_base.addWidget(self.widget_id, Qt.AlignTop)
        numero_fila = 0

        etiqueta_nombre_receta=QLabel("Receta")
        self.distribuidor_receta.addWidget(etiqueta_nombre_receta, numero_fila, 0)

        self.texto_nombre_receta=QLineEdit(self)
        self.distribuidor_receta.addWidget(self.texto_nombre_receta, numero_fila, 1)
        numero_fila=numero_fila+1

        etiqueta_tiempo_preparacion=QLabel("Tiempo preparación(hh:mm:ss)")
        self.distribuidor_receta.addWidget(etiqueta_tiempo_preparacion, numero_fila, 0)

        self.texto_tiempo_preparacion=QLineEdit(self)
        self.distribuidor_receta.addWidget(self.texto_tiempo_preparacion, numero_fila, 1)
        numero_fila=numero_fila+1

        etiqueta_personas = QLabel("Número personas")
        self.distribuidor_receta.addWidget(etiqueta_personas, numero_fila, 0)

        self.texto_personas = QLineEdit(self)
        self.distribuidor_receta.addWidget(self.texto_personas, numero_fila, 1)
        numero_fila = numero_fila + 1

        etiqueta_calorias = QLabel("Calorías por porción")
        self.distribuidor_receta.addWidget(etiqueta_calorias, numero_fila, 0)

        self.texto_calorias = QLineEdit(self)
        self.distribuidor_receta.addWidget(self.texto_calorias, numero_fila, 1)
        numero_fila=numero_fila+1

        etiqueta_Preparacion = QLabel("Preparación")
        self.distribuidor_receta.addWidget(etiqueta_Preparacion, numero_fila, 0)

        self.texto_preparacion = QTextEdit(self)
        self.texto_preparacion.setMinimumHeight(180)
        self.distribuidor_receta.addWidget(self.texto_preparacion, numero_fila, 1)
        numero_fila = numero_fila + 1


        #Creación de la caja con los botones
        self.widget_botones = QWidget()
        self.distribuidor_botones = QGridLayout()
        self.widget_botones.setLayout(self.distribuidor_botones)
        self.distribuidor_base.addWidget(self.widget_botones, Qt.AlignTop)

       #Creación de los botones con las diferentes operaciones
        
        self.btn_ingredientes_receta = QPushButton("Ingredientes", self)
        self.btn_ingredientes_receta.setFixedSize(130, 40)
        self.btn_ingredientes_receta.setToolTip("Ingredientes")
        self.btn_ingredientes_receta.setIcon(QIcon("src/recursos/010-ingredientes.png"))
        self.btn_ingredientes_receta.setDisabled(True)
        self.distribuidor_botones.addWidget(self.btn_ingredientes_receta, 0, 0, Qt.AlignCenter)
        self.btn_ingredientes_receta.clicked.connect(self.mostrar_ventana_ingredientes_receta)
        
        self.btn_guardar_receta = QPushButton("Guardar receta", self)
        self.btn_guardar_receta.setFixedSize(130, 40)
        self.btn_guardar_receta.setToolTip("Guardar receta")
        self.btn_guardar_receta.setIcon(QIcon("src/recursos/floppy-disk.png"))
        self.distribuidor_botones.addWidget(self.btn_guardar_receta, 0, 1, Qt.AlignCenter)
        self.btn_guardar_receta.clicked.connect(self.guardar_cambios)


        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(130, 40)
        self.btn_volver.setToolTip("Volver")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.distribuidor_botones.addWidget(self.btn_volver, 0, 2, Qt.AlignCenter)
        self.btn_volver.clicked.connect(self.volver)


    def mostrar_receta(self, receta):
        self.receta=receta
        if (self.receta!=None):
            self.texto_nombre_receta.setText(self.receta["nombre"])
            self.texto_tiempo_preparacion.setText(str(self.receta["tiempo"]))
            self.texto_personas.setText(str(self.receta["personas"]))
            self.texto_calorias.setText(str(self.receta["calorias"]))
            self.texto_preparacion.setText(self.receta["preparacion"])
            self.btn_ingredientes_receta.setEnabled(True)
        


    def guardar_cambios(self):
        """
        Esta función guarda los cambios de una receta
        """
        resultado = self.interfaz.guardar_receta(self.texto_nombre_receta.text(), self.texto_tiempo_preparacion.text(),
                                                  self.texto_personas.text(), self.texto_calorias.text(),
                                                  self.texto_preparacion.toPlainText())
        if resultado == "":
            self.hide()
            self.interfaz.mostrar_vista_lista_recetas()
        else:
            self.error_id(resultado)

    def mostrar_ventana_ingredientes_receta(self):
        """
        Esta función informa a la interfaz para desplegar la ventana de lista de ingredientes de la receta
        """     
        self.hide()
        self.interfaz.mostrar_ingredientes_receta(self.receta)  

    def volver(self):
        """
        Esta función permite volver a la lista de recetas
        """    
        self.hide()
        self.interfaz.mostrar_vista_lista_recetas()

    def error_id(self, error):
        mensaje_error=QMessageBox()
        mensaje_error.setIcon(QMessageBox.Question)
        mensaje_error.setText("Error: " + error)
        mensaje_error.setWindowTitle("Error al guardar receta")
        mensaje_error.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))
        mensaje_error.setStandardButtons(QMessageBox.Ok ) 
        respuesta=mensaje_error.exec_()

    def recetaGuardada(self):
        mensaje=QMessageBox()
        mensaje.setIcon(QMessageBox.Question)
        mensaje.setText("Receta guardada ")
        mensaje.setWindowTitle("Receta guradada")
        mensaje.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))
        mensaje.setStandardButtons(QMessageBox.Ok ) 
        respuesta=mensaje.exec_()

    def closeEvent(self, event):
        self.hide()
        self.interfaz.mostrar_vista_lista_recetas()
        event.accept()
