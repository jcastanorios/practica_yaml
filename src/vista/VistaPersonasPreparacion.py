from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class VistaPersonasPreparacion(QDialog):
    # Diálogo para crear o editar un ingrediente

    def __init__(self, interfaz):
        """
        Constructor del diálogo
        """
        super().__init__()

        self.interfaz = interfaz
        self.cantidad_personas = 0

        self.setFixedSize(300, 150)
        self.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))

        self.resultado = ""

        self.widget_dialogo = QListWidget()

        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila = 0

        # Si se va a crear un nuevo ingrediente o se va a editar, usamos el mismo diálogo

        titulo = "Personas para la receta"

        self.setWindowTitle("Recetario - {}".format(titulo))

        # Creación de las etiquetas y los campos de texto
        etiqueta_personas = QLabel("Número de personas para la receta")
        distribuidor_dialogo.addWidget(etiqueta_personas, numero_fila, 0)

        self.texto_personas = QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_personas, numero_fila, 1)
        numero_fila = numero_fila + 1


        # Creación de los botones para aceptar o cancelar
        caja_botones = QGroupBox()
        caja_botones.setLayout(QHBoxLayout())
        caja_botones.setStyleSheet('''
                QGroupBox{border:none}''')

        self.btn_guardar = QPushButton("Preparar")
        caja_botones.layout().addWidget(self.btn_guardar)
        self.btn_guardar.clicked.connect(self.preparar)

        self.btn_cancelar = QPushButton("Volver")
        caja_botones.layout().addWidget(self.btn_cancelar)
        self.btn_cancelar.clicked.connect(self.cancelar)

        distribuidor_dialogo.addWidget(caja_botones, numero_fila, 0, 1, 2)


    def preparar(self):
        """
        Esta función envía la cantiad de personas para preparar la receta
        """
        try:
            self.cantidad_personas = int(self.texto_personas.text())
        except ValueError:
            self.cantidad_personas = -1
			
        self.close()
        return self.resultado

    def cancelar(self):
        """
        Esta función envía la información de cancelación de la operación
        """
        self.cantidad_personas = 0
        self.close()
        return self.resultado

