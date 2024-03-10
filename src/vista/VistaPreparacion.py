from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget


class VistaPreparacion(QWidget):
    #Ventana que muestra la preparación de una receta

    def __init__(self, interfaz, nombreReceta):
        """
        Constructor de la ventana
        """
        super().__init__()

        # Se establecen las características de la ventana
        self.titulo = "Recetario - Preparación receta  " + nombreReceta
        self.left = 80
        self.top = 80
        self.width = 800
        self.height = 560
        self.interfaz = interfaz
    

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.inicializar_GUI()
        self.show()

    def inicializar_GUI(self):

        # inicializamos la ventana
        self.setWindowTitle(self.titulo)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))

        self.distribuidor_base = QVBoxLayout(self)

        # Creación de la tabla datos de cantidad de elementos
        self.tabla_reporte = QScrollArea(self)
        self.tabla_reporte.setWidgetResizable(True)
        self.widget_tabla_reporte = QWidget()
        self.distribuidor_tabla_reporte = QGridLayout(self.widget_tabla_reporte)
        self.tabla_reporte.setWidget(self.widget_tabla_reporte)

        self.distribuidor_tabla_reporte.setColumnStretch(0, 0)
        self.distribuidor_tabla_reporte.setColumnStretch(1, 0)

        self.contenedor_tabla_reporte = QGroupBox(self)
        self.contenedor_tabla_reporte.setLayout(QHBoxLayout())
        self.contenedor_tabla_reporte.setTitle('Información preparación')
        self.distribuidor_base.addWidget(self.contenedor_tabla_reporte)

        self.contenedor_tabla_reporte.layout().addWidget(self.tabla_reporte)
        self.tabla_reporte.setStyleSheet('QScrollArea{border:none}')

        # Creación de las etiquetas con los encabezados
        etiqueta_talla = QLabel("Cantidad personas")
        etiqueta_talla.setFont(QFont("Times",weight=QFont.Bold))
        self.distribuidor_tabla_reporte.addWidget(etiqueta_talla, 0, 0, Qt.AlignTop)

        etiqueta_calorias = QLabel("Calorias por porción")
        etiqueta_calorias.setFont(QFont("Times",weight=QFont.Bold))
        self.distribuidor_tabla_reporte.addWidget(etiqueta_calorias, 1, 0, Qt.AlignTop)

        etiqueta_costo = QLabel("Costo aproximado de preparación")
        etiqueta_costo.setFont(QFont("Times", weight=QFont.Bold))
        self.distribuidor_tabla_reporte.addWidget(etiqueta_costo, 2, 0, Qt.AlignTop)

        etiqueta_clasificacion = QLabel("Tiempo aproximado de preparación")
        etiqueta_clasificacion.setFont(QFont("Times", weight=QFont.Bold))
        self.distribuidor_tabla_reporte.addWidget(etiqueta_clasificacion, 3, 0, Qt.AlignTop)

        # Creación de la tabla con el detalle de los ingredientes

        self.tabla_costo_ingredientes = QScrollArea(self)
        self.tabla_costo_ingredientes.setWidgetResizable(True)
        self.widget_tabla_costos = QWidget()
        self.distribuidor_tabla = QGridLayout(self.widget_tabla_costos)
        self.tabla_costo_ingredientes.setWidget(self.widget_tabla_costos)

        self.distribuidor_tabla.setColumnStretch(0, 0)
        self.distribuidor_tabla.setColumnStretch(1, 0)

        self.contenedor_tabla_costos = QGroupBox(self)
        self.contenedor_tabla_costos.setLayout(QHBoxLayout())
        self.contenedor_tabla_costos.setTitle('Detalle de costos')
        self.distribuidor_base.addWidget(self.contenedor_tabla_costos)

        self.contenedor_tabla_costos.layout().addWidget(self.tabla_costo_ingredientes)
        self.tabla_costo_ingredientes.setStyleSheet('QScrollArea{border:none}')

        # Creación de las etiquetas con los encabezados
        etiqueta_ingrediente= QLabel("Ingrediente")
        etiqueta_ingrediente.setFont(QFont("Times", weight=QFont.Bold))
        self.distribuidor_tabla.addWidget(etiqueta_ingrediente, 0, 0, Qt.AlignTop)

        etiqueta_unidad = QLabel("Unidad")
        etiqueta_unidad.setFont(QFont("Times", weight=QFont.Bold))
        self.distribuidor_tabla.addWidget(etiqueta_unidad, 0, 1, Qt.AlignTop)

        etiqueta_cantidad = QLabel("Cantidad")
        etiqueta_cantidad.setFont(QFont("Times", weight=QFont.Bold))
        etiqueta_cantidad.setAlignment(Qt.AlignHCenter)
        self.distribuidor_tabla.addWidget(etiqueta_cantidad, 0, 2, Qt.AlignTop)

        etiqueta_valor = QLabel("Valor")
        etiqueta_valor.setFont(QFont("Times", weight=QFont.Bold))
        etiqueta_valor.setAlignment(Qt.AlignCenter)
        self.distribuidor_tabla.addWidget(etiqueta_valor, 0, 3, Qt.AlignTop)

        #Creación de los botones de funciones de la ventana
        self.btn_volver = QPushButton("Volver", self)
        self.btn_volver.setFixedSize(200, 40)
        self.btn_volver.setToolTip("Volver")
        self.btn_volver.setIcon(QIcon("src/recursos/007-back-button.png"))
        self.btn_volver.setIconSize(QSize(120, 120))
        self.btn_volver.clicked.connect(self.volver)
        self.distribuidor_base.addWidget(self.btn_volver)
        self.distribuidor_base.setAlignment(self.btn_volver, Qt.AlignCenter)

    def mostrar_datos(self, datos_preparacion):
        """
        Esta función pobla el reporte con la información
        """
      
        #Mostrar información básica
        etiqueta_detalle = QLabel(str(datos_preparacion['personas']))
        etiqueta_detalle.setWordWrap(True)
        self.distribuidor_tabla_reporte.addWidget(etiqueta_detalle, 0, 1, Qt.AlignTop)

        etiqueta_detalle = QLabel(str(datos_preparacion['calorias']))
        etiqueta_detalle.setWordWrap(True)
        self.distribuidor_tabla_reporte.addWidget(etiqueta_detalle, 1, 1, Qt.AlignTop)

        etiqueta_detalle = QLabel("${:,.2f}".format(datos_preparacion['costo']))
        etiqueta_detalle.setWordWrap(True)
        self.distribuidor_tabla_reporte.addWidget(etiqueta_detalle, 2, 1, Qt.AlignTop)

        etiqueta_detalle = QLabel(str(datos_preparacion['tiempo_preparacion']))
        etiqueta_detalle.setWordWrap(True)
        self.distribuidor_tabla_reporte.addWidget(etiqueta_detalle, 3, 1, Qt.AlignTop)

        # Elemento para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        self.distribuidor_tabla_reporte.layout().setRowStretch(0, 1)
        self.distribuidor_tabla_reporte.layout().setRowStretch(1, 1)
        self.distribuidor_tabla_reporte.layout().setRowStretch(2, 1)
        self.distribuidor_tabla_reporte.layout().setRowStretch(3, 1)

        #Mostrar detalle de ingredientes
        numero_fila = 2
        for ingrediente in datos_preparacion['datos_ingredientes']:
            etiqueta_nombre = QLabel(ingrediente['nombre'])
            etiqueta_nombre.setWordWrap(True)
            etiqueta_nombre.setFixedSize(90, 40)
            self.distribuidor_tabla.addWidget(etiqueta_nombre, numero_fila + 1, 0, Qt.AlignTop)

            etiqueta_unidad = QLabel(str(ingrediente['unidad']))
            etiqueta_unidad.setWordWrap(True)
            etiqueta_unidad.setFixedSize(90, 40)
            self.distribuidor_tabla.addWidget(etiqueta_unidad, numero_fila + 1, 1, Qt.AlignTop)

            etiqueta_cantidad = QLabel(str(ingrediente['cantidad']))
            etiqueta_cantidad.setWordWrap(True)
            etiqueta_cantidad.setFixedSize(90, 40)
            etiqueta_cantidad.setAlignment(Qt.AlignCenter)
            self.distribuidor_tabla.addWidget(etiqueta_cantidad, numero_fila + 1, 2, Qt.AlignTop)

            etiqueta_valor = QLabel("${:,.2f}".format(ingrediente['valor']))
            etiqueta_valor.setWordWrap(True)
            etiqueta_valor.setFixedSize(90, 40)
            etiqueta_valor.setAlignment(Qt.AlignRight)
            self.distribuidor_tabla.addWidget(etiqueta_valor, numero_fila + 1, 3, Qt.AlignTop)
            numero_fila = numero_fila + 1


        etiqueta_total = QLabel("${:,.2f}".format(datos_preparacion['costo']))
        etiqueta_total.setWordWrap(True)
        etiqueta_total.setFixedSize(90, 40)
        etiqueta_total.setFont(QFont("Times", weight=QFont.Bold))
        etiqueta_total.setAlignment(Qt.AlignRight)
        self.distribuidor_tabla.addWidget(etiqueta_total, numero_fila + 1, 3, Qt.AlignTop)

        # Elemento para ajustar la forma de la tabla (y evitar que queden muy espaciados)
        self.distribuidor_tabla.layout().setRowStretch(numero_fila + 1, 1)
        
    def volver(self):
        """
        Esta función permite volver a la ventana de lista de recetas 
        """   
        self.hide()
        self.interfaz.mostrar_vista_lista_recetas()

    def closeEvent(self, event):
        self.hide()
        self.interfaz.mostrar_vista_lista_recetas()
        event.accept()
