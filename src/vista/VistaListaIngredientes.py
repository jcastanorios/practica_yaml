from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *

from functools import partial

from  .VistaCrearIngrediente import VistaCrearIngrediente


class VistaListaIngredientes(QWidget):
    #Ventana que muestra la lista de ingredientes

    def __init__(self, interfaz):
        """
        Constructor de la ventana
        """
        super().__init__()

        #Se establecen las características de la ventana
        self.titulo = 'Recetario - Ingredientes'
        self.interfaz=interfaz

        self.width = 800
        self.height = 500
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
        self.btn_agregar_ingrediente=QPushButton("Agregar ingrediente", self)
        self.btn_agregar_ingrediente.setFixedSize(170, 40)
        self.btn_agregar_ingrediente.setToolTip("Agregar ingrediente")
        self.btn_agregar_ingrediente.setIcon(QIcon("src/recursos/006-add.png"))
        self.btn_agregar_ingrediente.clicked.connect(self.mostrar_dialogo_agregar_ingrediente)

        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(170, 40)
        self.btn_volver.setToolTip("Volver")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.btn_volver.clicked.connect(self.volver)



        self.contenedor_tabla = QGroupBox(self)
        self.contenedor_tabla.setLayout(QHBoxLayout())
        self.contenedor_tabla.setTitle('Ingredientes')
        self.distribuidor_base.addWidget(self.contenedor_tabla)

        #Creación de la tabla con la lista de ingredientes
        self.tabla_ingredientes = QScrollArea(self)
        self.tabla_ingredientes.setWidgetResizable(True)
        self.tabla_ingredientes.setStyleSheet('QScrollArea{border:none}')
        self.tabla_ingredientes.setFixedSize(700, 300)
        self.widget_tabla_ingredientes = QWidget()
        self.distribuidor_tabla_ingredientes = QGridLayout(self.widget_tabla_ingredientes)
        self.tabla_ingredientes.setWidget(self.widget_tabla_ingredientes)
        self.contenedor_tabla.layout().addWidget(self.tabla_ingredientes)

        self.distribuidor_tabla_ingredientes.setColumnStretch(0, 1)
        self.distribuidor_tabla_ingredientes.setColumnStretch(1, 1)
        self.distribuidor_tabla_ingredientes.setColumnStretch(2, 1)
        self.distribuidor_tabla_ingredientes.setColumnStretch(3, 1)
        self.distribuidor_tabla_ingredientes.setColumnStretch(4, 1)
        self.distribuidor_tabla_ingredientes.setColumnStretch(5, 1)

        self.distribuidor_tabla_ingredientes.setSpacing(0)

        #Creación de las etiquetas de encabezado
        etiqueta_nombre = QLabel("Ingrediente")
        etiqueta_nombre.setFixedSize(180,40)
        etiqueta_nombre.setFont(QFont("Times",weight=QFont.Bold)) 
        self.distribuidor_tabla_ingredientes.addWidget(etiqueta_nombre, 0, 0, Qt.AlignTop)

        etiqueta_unidad = QLabel("Unidad")
        etiqueta_unidad.setFixedSize(80,40)
        etiqueta_unidad.setFont(QFont("Times",weight=QFont.Bold)) 
        etiqueta_unidad.setAlignment(Qt.AlignCenter)
        self.distribuidor_tabla_ingredientes.addWidget(etiqueta_unidad, 0, 1, Qt.AlignTop)
        
        etiqueta_valor = QLabel("Valor \n por unidad")
        etiqueta_valor.setFixedSize(100,60)
        etiqueta_valor.setFont(QFont("Times",weight=QFont.Bold)) 
        etiqueta_valor.setAlignment(Qt.AlignCenter)
        self.distribuidor_tabla_ingredientes.addWidget(etiqueta_valor, 0, 2, Qt.AlignTop)

        etiqueta_sitio = QLabel("Sitio \n compra")
        etiqueta_sitio.setFixedSize(180,60)
        etiqueta_sitio.setFont(QFont("Times",weight=QFont.Bold)) 
        etiqueta_sitio.setAlignment(Qt.AlignCenter)
        self.distribuidor_tabla_ingredientes.addWidget(etiqueta_sitio, 0, 3, Qt.AlignTop)



        etiqueta_accion = QLabel("Opciones")
        etiqueta_accion.setFixedSize(60,40)
        etiqueta_accion.setFont(QFont("Times",weight=QFont.Bold)) 
        etiqueta_accion.setAlignment(Qt.AlignCenter)
        self.distribuidor_tabla_ingredientes.addWidget(etiqueta_accion, 0, 4, 0, 2, Qt.AlignTop | Qt.AlignCenter)

        #Se añaden los botones a la caja de botones
        caja_botones.layout().addWidget(self.btn_agregar_ingrediente)
        caja_botones.layout().addWidget(self.btn_volver)
        caja_botones.layout().setContentsMargins(0, 0, 0, 0)
        caja_botones.setObjectName("MyBox")
        caja_botones.setStyleSheet("#MyBox{border:3px}")
        self.distribuidor_base.addWidget(caja_botones)

    def mostrar_ingredientes(self, lista_ingredientes):
        """
        Esta función muestra la lista de ingredientes
        """
        self.ingredientes = lista_ingredientes

        #Ciclo para poblar la tabla
        numero_fila = 0
        for ingrediente in self.ingredientes:

            etiqueta_nombre=QLabel(ingrediente["nombre"])
            etiqueta_nombre.setWordWrap(True)
            etiqueta_nombre.setFixedSize(180,40)
            self.distribuidor_tabla_ingredientes.addWidget(etiqueta_nombre, numero_fila + 1, 0, Qt.AlignTop)

            etiqueta_unidad=QLabel(ingrediente["unidad"])
            etiqueta_unidad.setWordWrap(True)
            etiqueta_unidad.setFixedSize(80,40)
            etiqueta_unidad.setAlignment(Qt.AlignCenter)
            self.distribuidor_tabla_ingredientes.addWidget(etiqueta_unidad, numero_fila + 1, 1, Qt.AlignTop)

            etiqueta_valor=QLabel(str(ingrediente["valor"]))
            etiqueta_valor.setWordWrap(True)
            etiqueta_valor.setFixedSize(120,40)
            etiqueta_valor.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.distribuidor_tabla_ingredientes.addWidget(etiqueta_valor, numero_fila + 1, 2, Qt.AlignHCenter)

            etiqueta_sitioCompras=QLabel(ingrediente["sitioCompra"])
            etiqueta_sitioCompras.setWordWrap(True)
            etiqueta_sitioCompras.setFixedSize(180,40)
            etiqueta_sitioCompras.setAlignment(Qt.AlignCenter)
            self.distribuidor_tabla_ingredientes.addWidget(etiqueta_sitioCompras, numero_fila + 1, 3, Qt.AlignTop)

            boton_editar=QPushButton("",self)
            boton_editar.setToolTip("Editar")
            boton_editar.setFixedSize(40,40)
            boton_editar.setIcon(QIcon("src/recursos/004-edit-button.png"))
            boton_editar.clicked.connect(partial(self.mostrar_dialogo_editar_ingrediente, numero_fila))
            self.distribuidor_tabla_ingredientes.addWidget(boton_editar, numero_fila + 1, 4, Qt.AlignTop)

            etiqueta_eliminar=QPushButton("",self)
            etiqueta_eliminar.setToolTip("Borrar")
            etiqueta_eliminar.setFixedSize(40,40)
            etiqueta_eliminar.setIcon(QIcon("src/recursos/005-delete.png"))
            etiqueta_eliminar.clicked.connect(partial(self.eliminar_ingrediente, numero_fila))
            self.distribuidor_tabla_ingredientes.addWidget(etiqueta_eliminar, numero_fila + 1, 5, Qt.AlignTop)

            numero_fila=numero_fila+1

            #para ajustar la forma de la tabla (y evitar que queden muy espaciados)
            self.distribuidor_tabla_ingredientes.layout().setRowStretch(numero_fila + 1, 1)

    def mostrar_dialogo_agregar_ingrediente(self):
        """
        Esta función ejecuta el diálogo para crear un nuevo ingrediente
        """
        dialogo=VistaCrearIngrediente(None, self.interfaz)
        dialogo.exec_()
        if dialogo.resultado==1:
            self.interfaz.crear_ingrediente(dialogo.texto_nombre.text(), dialogo.texto_unidad.text(), dialogo.texto_valor.text(),
                                          dialogo.texto_sitioCompra.text())

    def mostrar_dialogo_editar_ingrediente(self, id_ingrediente):
        """
        Esta función ejecuta el diálogo para editar un ingrediente
        """    
        dialogo=VistaCrearIngrediente(self.ingredientes[id_ingrediente], self.interfaz)
        dialogo.exec_()
        if dialogo.resultado==1:  
            self.interfaz.editar_ingrediente(id_ingrediente, dialogo.texto_nombre.text(), dialogo.texto_unidad.text(),dialogo.texto_valor.text(), dialogo.texto_sitioCompra.text())
            self.hide()
            self.interfaz.mostrar_ingredientes()

    def eliminar_ingrediente(self, indice_ingrediente):
        """
        Esta función informa a la interfaz el ingrediente a eliminar
        """    
        mensaje_confirmacion=QMessageBox()
        mensaje_confirmacion.setIcon(QMessageBox.Question)
        mensaje_confirmacion.setText("¿Esta seguro de que desea eliminar este ingrediente?\nRecuerde que esta acción es irreversible")
        mensaje_confirmacion.setWindowTitle("¿Desea borrar este ingrediente?")
        mensaje_confirmacion.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))
        mensaje_confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No ) 
        respuesta=mensaje_confirmacion.exec_()
        if respuesta == QMessageBox.Yes:
            self.interfaz.eliminar_ingrediente(indice_ingrediente)
            self.hide()
            self.interfaz.mostrar_ingredientes()

    def volver(self):
        """
        Esta función permite volver a la ventana de la lista de recetas
        """
        self.hide()
        self.interfaz.mostrar_vista_lista_recetas()

    def error(self, error):
            mensaje_error=QMessageBox()
            mensaje_error.setIcon(QMessageBox.Question)
            mensaje_error.setText("Error : " + error)
            mensaje_error.setWindowTitle("Error al guardar ingrediente")
            mensaje_error.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))
            mensaje_error.setStandardButtons(QMessageBox.Ok ) 
            respuesta=mensaje_error.exec_()

    def closeEvent(self, event):
        self.hide()
        self.interfaz.mostrar_vista_lista_recetas()
        event.accept()
