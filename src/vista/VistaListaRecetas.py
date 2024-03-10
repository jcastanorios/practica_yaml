from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial
from .VistaPersonasPreparacion import VistaPersonasPreparacion


class VistaListaRecetas(QWidget):
    #Ventana que muestra la lista de recetas

    def __init__(self, interfaz):
        """
        Constructor de la ventanas
        """
        super().__init__()
        
        self.interfaz = interfaz
       
        #Se establecen las características de la ventana
        self.title = 'Recetario'
        self.width = 875
        self.height = 758
        self.inicializar_GUI()

    def inicializar_GUI(self):
        
        #inicializamos la ventana
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))
         
        self.distribuidor_base = QVBoxLayout(self)

        #Creación del logo de encabezado
        self.logo=QLabel(self)
        self.pixmap = QPixmap("src/recursos/RecetarioLogo.png")
        self.pixmap = self.pixmap.scaled(488,158, Qt.KeepAspectRatio)
        self.logo.setPixmap(self.pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        self.distribuidor_base.addWidget(self.logo,alignment=Qt.AlignCenter)

        #Creación de las etiquetsa con textos de bienvenida
        self.etiqueta_bienvenida=QLabel("!!Bienvenido!!")
        self.etiqueta_bienvenida.setAlignment(Qt.AlignCenter)
        self.distribuidor_base.addWidget(self.etiqueta_bienvenida,Qt.AlignCenter)

        #Creación del espacio de los botones
        self.widget_botones=QWidget()
        self.distribuidor_botones=QGridLayout()
        self.widget_botones.setLayout(self.distribuidor_botones)

        #Creación de los botones
        self.btn_crear_receta=QPushButton("Crear receta",self)
        self.btn_crear_receta.setFixedSize(288,48)
        self.btn_crear_receta.setToolTip("Crear receta")
        self.btn_crear_receta.setIcon(QIcon("src/recursos/006-add.png"))
        self.btn_crear_receta.setIconSize(QSize(120,120))
        self.distribuidor_botones.addWidget(self.btn_crear_receta,0,1,Qt.AlignLeft)
        self.btn_crear_receta.clicked.connect(self.crear_receta)

        self.btn_ver_ingredientes=QPushButton("Ingredientes",self)
        self.btn_ver_ingredientes.setFixedSize(288,48)
        self.btn_ver_ingredientes.setToolTip("Ingredientes")
        self.btn_ver_ingredientes.setIcon(QIcon("src/recursos/010-ingredientes.png"))
        self.btn_ver_ingredientes.setIconSize(QSize(30,30))
        self.distribuidor_botones.addWidget(self.btn_ver_ingredientes,0,2,Qt.AlignRight)
        self.distribuidor_base.addWidget(self.widget_botones,Qt.AlignCenter)
        self.btn_ver_ingredientes.clicked.connect(self.mostrar_ingredientes)

        #Creación del área con la información de las recetas
        self.tabla_recetas = QScrollArea(self)
        self.tabla_recetas.setWidgetResizable(True)
        self.tabla_recetas.setFixedSize(840, 400)
        self.widget_tabla_recetas = QWidget()
        self.distribuidor_tabla_recetas = QGridLayout()
        self.widget_tabla_recetas.setLayout(self.distribuidor_tabla_recetas);
        self.tabla_recetas.setWidget(self.widget_tabla_recetas)
        self.distribuidor_base.addWidget(self.tabla_recetas)

        #Hacemos la ventana visible
        self.show()


    def mostrar_recetas(self, lista_recetas):
        """
        Esta función puebla la tabla con las recetas
        """
        self.recetas = lista_recetas
        numero_fila=0

        self.distribuidor_tabla_recetas.setColumnStretch(0,1)
        self.distribuidor_tabla_recetas.setColumnStretch(1,1)
        self.distribuidor_tabla_recetas.setColumnStretch(2,0)
        self.distribuidor_tabla_recetas.setColumnStretch(3,0)
        self.distribuidor_tabla_recetas.setColumnStretch(4,0)
        self.distribuidor_tabla_recetas.setColumnStretch(5,0)

        #Ciclo para llenar la tabla
        if (self.recetas!= None and len(self.recetas)>0) :
            self.tabla_recetas.setVisible(True)

            #Creación de las etiquetas
            etiqueta_nombre=QLabel("Nombre")
            etiqueta_nombre.setMinimumSize(QSize(0,0))
            etiqueta_nombre.setMaximumSize(QSize(65525,65525))
            etiqueta_nombre.setAlignment(Qt.AlignCenter)
            etiqueta_nombre.setFont(QFont("Times",weight=QFont.Bold)) 
            self.distribuidor_tabla_recetas.addWidget(etiqueta_nombre, 0,0, Qt.AlignLeft)

            etiqueta_acciones=QLabel("Opciones")                      
            etiqueta_acciones.setMinimumSize(QSize(0,0))
            etiqueta_acciones.setMaximumSize(QSize(65525,65525))
            etiqueta_acciones.setAlignment(Qt.AlignCenter)
            etiqueta_acciones.setFont(QFont("Times",weight=QFont.Bold))               
            self.distribuidor_tabla_recetas.addWidget(etiqueta_acciones, 0,2,1,3, Qt.AlignCenter)
       
            for dic_receta in self.recetas:
                numero_fila=numero_fila+1

                etiqueta_nombre=QLabel(dic_receta['nombre'] )
                etiqueta_nombre.setWordWrap(True)
                self.distribuidor_tabla_recetas.addWidget(etiqueta_nombre,numero_fila,0)

                #Creación de los botones asociados a cada acción


                btn_editar_receta=QPushButton("",self)
                btn_editar_receta.setToolTip("Editar")
                btn_editar_receta.setFixedSize(40,40)
                btn_editar_receta.setIcon(QIcon("src/recursos/004-edit-button.png"))
                btn_editar_receta.clicked.connect(partial(self.mostrar_receta,numero_fila-1) )
                self.distribuidor_tabla_recetas.addWidget(btn_editar_receta,numero_fila,2,Qt.AlignCenter)

                btn_eliminar=QPushButton("",self)
                btn_eliminar.setToolTip("Borrar")
                btn_eliminar.setFixedSize(40,40)
                btn_eliminar.setIcon(QIcon("src/recursos/005-delete.png"))
                btn_eliminar.clicked.connect(partial(self.eliminar_receta,numero_fila -1) )
                self.distribuidor_tabla_recetas.addWidget(btn_eliminar,numero_fila,3,Qt.AlignCenter)

                btn_preparar_receta = QPushButton("", self)
                btn_preparar_receta.setToolTip("Preparar")
                btn_preparar_receta.setFixedSize(40, 40)
                btn_preparar_receta.setIcon(QIcon("src/recursos/002-preparar.png"))
                btn_preparar_receta.clicked.connect(
                    partial(self.mostrar_ventana_preparar, numero_fila - 1))
                self.distribuidor_tabla_recetas.addWidget(btn_preparar_receta, numero_fila, 4,
                                                           Qt.AlignCenter)

        else:
                self.tabla_recetas.setVisible(False)

        #persona para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        self.distribuidor_tabla_recetas.layout().setRowStretch(numero_fila+2, 1)

    def crear_receta(self):
        """
        Esta función informa a la interfaz para desplegar la ventana para crear 
        """
        self.hide()
        self.interfaz.crear_receta()
    
    def mostrar_receta(self, id_receta):
        """
        Esta función informa a la interfaz para desplegar la ventana con la información de la receta seleccionada
        """
        self.hide()
        self.interfaz.mostrar_receta(id_receta)

    def eliminar_receta(self, indice):
        """
        Esta función elimina una receta tras solicitar una confirmación
        """
        mensaje_confirmacion = QMessageBox()
        mensaje_confirmacion.setIcon(QMessageBox.Question)
        mensaje_confirmacion.setText(
            "¿Esta seguro de que desea borrar esta receta?\nRecuerde que esta acción es irreversible")
        mensaje_confirmacion.setWindowTitle("¿Desea borrar esta receta?")
        mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))
        mensaje_confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        respuesta = mensaje_confirmacion.exec_()
        if respuesta == QMessageBox.Yes:
            self.interfaz.eliminar_receta(indice)
            self.hide()
            self.interfaz.mostrar_vista_lista_recetas()

    def mostrar_ingredientes(self):
        """
        Esta función informa a la interfaz para desplegar la ventana de lista de ingredientes
        """
        self.hide()
        self.interfaz.mostrar_ingredientes()
 


    def mostrar_ventana_preparar(self,id_receta):
        """
        Esta función informa a la interfaz para desplegar la ventana de preparación de una receta
        """
        self.hide()
        dialogo=VistaPersonasPreparacion(self.interfaz)
        dialogo.exec_()
        if dialogo.cantidad_personas<0:
            mensaje_error=QMessageBox()
            mensaje_error.setIcon(QMessageBox.Warning)
            mensaje_error.setText("La cantidad de personas no es válida")
            respuesta=mensaje_error.exec_()
            self.interfaz.mostrar_vista_lista_recetas()
        elif dialogo.cantidad_personas==0:
            self.interfaz.mostrar_vista_lista_recetas()
        else:
            self.interfaz.mostrar_preparacion(id_receta, dialogo.cantidad_personas)
