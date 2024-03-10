from datetime import datetime
from PyQt5 import QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class VistaCrearIngReceta(QDialog):
    # Diálogo para crear o editar un ingrediente de una receta

    def __init__(self, ingredienteReceta, interfaz, ingredientes):
        """
        Constructor del diálogo
        """
        super().__init__()

        self.interfaz = interfaz
        self.ingredientes = ingredientes

        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))

        self.resultado = ""

        self.widget_dialogo = QListWidget()

        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila = 0

        # Si se va a crear un nuevo ingrediente de la receta o se va a editar, usamos el mismo diálogo

        titulo = ""
        if (ingredienteReceta == None):
            titulo = "Nuevo ingrediente de receta"
        else:
            titulo = "Editar ingrediente de receeta"

        self.setWindowTitle("Recetario- {}".format(titulo))

        # Creación de las etiquetas y los campos de texto
        etiqueta_ingrediente = QLabel("Ingrediente")
        distribuidor_dialogo.addWidget(etiqueta_ingrediente, numero_fila, 0)

        self.combobox_ingredientes = QComboBox(self)
        for ingrediente in self.ingredientes:
            self.combobox_ingredientes.addItem(ingrediente["nombre"] + "[" + ingrediente["unidad"]+"]")
        self.combobox_ingredientes.setCurrentIndex(0)
        distribuidor_dialogo.addWidget(self.combobox_ingredientes, numero_fila, 1, 1, 2)
        numero_fila = numero_fila + 1

        etiqueta_cantidad = QLabel("Cantidad")
        distribuidor_dialogo.addWidget(etiqueta_cantidad, numero_fila, 0)

        self.texto_cantidad = QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_cantidad, numero_fila, 1)
        numero_fila = numero_fila + 1



        # Creación de los botones para guardar o cancelar
        caja_botones = QGroupBox()
        caja_botones.setLayout(QHBoxLayout())
        caja_botones.setStyleSheet('''
                QGroupBox{border:none}''')

        self.btn_guardar = QPushButton("Guardar ingrediente de receta")
        caja_botones.layout().addWidget(self.btn_guardar)
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        caja_botones.layout().addWidget(self.btn_cancelar)
        self.btn_cancelar.clicked.connect(self.cancelar)

        distribuidor_dialogo.addWidget(caja_botones, numero_fila, 0, 1, 2)

        # Si el diálogo se va a usar para editar, se pone la información correspondiente en los campos de texto
        if (ingredienteReceta != None):
            indice_ingrediente_receta = self.combobox_ingredientes.findText(ingredienteReceta["ingrediente"] + "[" + ingredienteReceta["unidad"]+"]")
            self.combobox_ingredientes.setCurrentIndex(indice_ingrediente_receta)
            self.texto_cantidad.setText(str(ingredienteReceta["cantidad"]))

    def guardar(self):
        """
        Esta función envía la información de la solicitud de guardar los cambios
        """
        self.resultado = 1
        self.close()
        return self.resultado

    def cancelar(self):
        """
        Esta función envía la información de cancelación de la operación
        """
        self.resultado = 0
        self.close()
        return self.resultado
