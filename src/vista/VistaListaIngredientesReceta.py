from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *

from functools import partial

from .VistaCrearIngReceta import VistaCrearIngReceta


class VistaListaIngredientesReceta(QWidget):
    #Ventana que muestra la lista de ingredientes de una receta

    def __init__(self, interfaz, receta, ingredientes):
        """
        Constructor de la ventana
        """
        super().__init__()

        #Se establecen las características de la ventana
        self.titulo = 'Recetario- Ingredientes receta'
        self.interfaz = interfaz
        self.receta = receta
        self.ingredientes= ingredientes

        self.width =720
        self.height = 560
        self.inicializar_GUI()
        self.show()


    def inicializar_GUI(self):

        # inicializamos la ventana
        self.setWindowTitle(self.titulo)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))
         
        self.distribuidor_base = QVBoxLayout(self)        

        #Creación del grupo de botones
        caja_botones = QGroupBox()
        caja_botones.setLayout(QHBoxLayout())

        #Creación de los botones

        self.btn_agregar_ingredienteReceta=QPushButton("Agregar ingrediente", self)
        self.btn_agregar_ingredienteReceta.setFixedSize(170, 40)
        self.btn_agregar_ingredienteReceta.setToolTip("Agregar ingrediente")
        self.btn_agregar_ingredienteReceta.setIcon(QIcon("src/recursos/006-add.png"))
        self.btn_agregar_ingredienteReceta.clicked.connect(self.mostrar_dialogo_agregar_ingredienteReceta)

        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(170, 40)
        self.btn_volver.setToolTip("Volver")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.btn_volver.clicked.connect(self.volver)

        self.contenedor_tabla = QGroupBox(self)
        self.contenedor_tabla.setLayout(QHBoxLayout())
        self.contenedor_tabla.setTitle('Ingredientes receta')
        self.distribuidor_base.addWidget(self.contenedor_tabla)

        #Creación de la tabla con la lista de ingredientes de una receta
        self.tabla_ingReceta = QScrollArea(self)
        self.tabla_ingReceta.setWidgetResizable(True)
        self.tabla_ingReceta.setStyleSheet('QScrollArea{border:none}')
        self.tabla_ingReceta.setFixedSize(620, 460)
        self.widget_tabla_ingReceta = QWidget()
        self.distribuidor_tabla_ingReceta = QGridLayout(self.widget_tabla_ingReceta)
        self.tabla_ingReceta.setWidget(self.widget_tabla_ingReceta)
        self.contenedor_tabla.layout().addWidget(self.tabla_ingReceta)

        self.distribuidor_tabla_ingReceta.setColumnStretch(0, 0)
        self.distribuidor_tabla_ingReceta.setColumnStretch(1, 0)
        self.distribuidor_tabla_ingReceta.setColumnStretch(2, 0)

        self.distribuidor_tabla_ingReceta.setSpacing(0)

        #Creación de las etiquetas de encabezado
        etiqueta_ingrediente = QLabel("Ingrediente")
        etiqueta_ingrediente.setFont(QFont("Times", weight=QFont.Bold))
        self.distribuidor_tabla_ingReceta.addWidget(etiqueta_ingrediente, 0, 0, Qt.AlignTop)

        etiqueta_unidad = QLabel("Unidad")
        etiqueta_unidad.setFont(QFont("Times", weight=QFont.Bold))
        self.distribuidor_tabla_ingReceta.addWidget(etiqueta_unidad, 0, 1, alignment=Qt.AlignLeft | Qt.AlignTop)

        etiqueta_cantidad = QLabel("Cantiad")
        etiqueta_cantidad.setFont(QFont("Times", weight=QFont.Bold))
        self.distribuidor_tabla_ingReceta.addWidget(etiqueta_cantidad, 0, 2, Qt.AlignLeft | Qt.AlignTop)


        etiqueta_accion = QLabel("Opciones")
        etiqueta_accion.setFont(QFont("Times", weight=QFont.Bold))
        self.distribuidor_tabla_ingReceta.addWidget(etiqueta_accion, 0, 3, 0, 2, alignment=Qt.AlignCenter | Qt.AlignTop)

        #Se añaden los botones a la caja de botones
        caja_botones.layout().addWidget(self.btn_agregar_ingredienteReceta)
        caja_botones.layout().addWidget(self.btn_volver)
        caja_botones.layout().setContentsMargins(0, 0, 0, 0)
        caja_botones.setObjectName("MyBox")
        caja_botones.setStyleSheet("#MyBox{border:3px}")
        self.distribuidor_base.addWidget(caja_botones)

    def mostrar_ing_receta(self, lista_ings_receta):
        """
        Esta función muestra la lista de ingredientes de la receta
        """

        self.contenedor_tabla.setTitle('Ingredientes ' + self.receta['nombre'])
        self.lista_ings_receta = lista_ings_receta
        

        #Ciclo para poblar la tabla
        numero_fila = 0
        for ingredienteReceta in self.lista_ings_receta:

            etiqueta_nombre=QLabel(ingredienteReceta['ingrediente'])
            etiqueta_nombre.setWordWrap(True)
            etiqueta_nombre.setFixedSize(90,40)
            self.distribuidor_tabla_ingReceta.addWidget(etiqueta_nombre, numero_fila + 1, 0, Qt.AlignTop)

            etiqueta_unidad = QLabel(ingredienteReceta['unidad'])
            etiqueta_unidad.setWordWrap(True)
            etiqueta_unidad.setFixedSize(90, 40)
            self.distribuidor_tabla_ingReceta.addWidget(etiqueta_unidad, numero_fila + 1, 1, Qt.AlignTop)

            etiqueta_cantidad = QLabel(str(ingredienteReceta['cantidad']))
            etiqueta_cantidad.setWordWrap(True)
            etiqueta_cantidad.setFixedSize(90, 40)
            self.distribuidor_tabla_ingReceta.addWidget(etiqueta_cantidad, numero_fila + 1, 2, Qt.AlignTop)

            boton_editar=QPushButton("",self)
            boton_editar.setToolTip("Editar")
            boton_editar.setFixedSize(30,30)
            boton_editar.setIcon(QIcon("src/recursos/004-edit-button.png"))
            boton_editar.clicked.connect(partial(self.mostrar_dialogo_editar_ingrediente_receta, numero_fila))
            self.distribuidor_tabla_ingReceta.addWidget(boton_editar, numero_fila + 1, 3, Qt.AlignTop)

            boton_eliminar=QPushButton("",self)
            boton_eliminar.setToolTip("Borrar")
            boton_eliminar.setFixedSize(30,30)
            boton_eliminar.setIcon(QIcon("src/recursos/005-delete.png"))
            boton_eliminar.clicked.connect(partial(self.eliminar_ingrediente_receta, numero_fila))
            self.distribuidor_tabla_ingReceta.addWidget(boton_eliminar, numero_fila + 1, 4, Qt.AlignTop)

            numero_fila=numero_fila+1


        #Elemento para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        self.distribuidor_tabla_ingReceta.layout().setRowStretch(numero_fila + 1, 1)

    def mostrar_dialogo_agregar_ingredienteReceta(self):
        """
        Esta función ejecuta el diálogo para agregar un nuevo ingrediente a una receta
        """
        dialogo=VistaCrearIngReceta(None, self.interfaz, self.ingredientes)
        dialogo.exec_()
        if dialogo.resultado==1:
            self.interfaz.agregar_ingrediente_receta(self.receta,self.ingredientes[dialogo.combobox_ingredientes.currentIndex()],dialogo.texto_cantidad.text())
            self.hide()
            self.interfaz.mostrar_ingredientes_receta(self.receta)
            

    def mostrar_dialogo_editar_ingrediente_receta(self, id_ingrediente_receta):
        """
        Esta función ejecuta el diálogo para editar un ingrediente de una receta
        """    
        dialogo=VistaCrearIngReceta(self.lista_ings_receta[id_ingrediente_receta], self.interfaz, self.ingredientes)
        dialogo.exec_()
        if dialogo.resultado==1:            
            self.interfaz.editar_ingrediente_receta(id_ingrediente_receta,self.receta, self.ingredientes[dialogo.combobox_ingredientes.currentIndex()], dialogo.texto_cantidad.text())
            self.hide()
            self.interfaz.mostrar_ingredientes_receta(self.receta)


    def eliminar_ingrediente_receta(self, id_ingrediente_receta):
        """
        Esta función informa a la interfaz el ingrediente receta a eliminar
        """    
        mensaje_confirmacion=QMessageBox()
        mensaje_confirmacion.setIcon(QMessageBox.Question)
        mensaje_confirmacion.setText("¿Esta seguro de que desea eliminar este ingrediente de la receta?\nRecuerde que esta acción es irreversible")
        mensaje_confirmacion.setWindowTitle("¿Desea borrar este ingrediente de la receeta?")
        mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))
        mensaje_confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No ) 
        respuesta=mensaje_confirmacion.exec_()
        if respuesta == QMessageBox.Yes:
            self.interfaz.eliminar_ingrediente_receta(id_ingrediente_receta, self.receta)
            self.hide()
            self.interfaz.mostrar_ingredientes_receta(self.receta)



    def volver(self):
        """
        Esta función permite volver a la ventana de lista de recetas
        """
        self.hide()
        self.interfaz.mostrar_ventana_receta(self.receta)

    def error(self, error):
            mensaje_error=QMessageBox()
            mensaje_error.setIcon(QMessageBox.Question)
            mensaje_error.setText("Error : " + error)
            mensaje_error.setWindowTitle("Error guardar ingrediente receta")
            mensaje_error.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))
            mensaje_error.setStandardButtons(QMessageBox.Ok ) 
            respuesta=mensaje_error.exec_()

    def closeEvent(self, event):
        self.hide()
        self.interfaz.mostrar_ventana_receta(self.receta)
        event.accept()
