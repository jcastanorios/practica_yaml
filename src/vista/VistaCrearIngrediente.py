
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class VistaCrearIngrediente(QDialog):
    # Diálogo para crear o editar un ingrediente

    def __init__(self, ingrediente, interfaz):
        """
        Constructor del diálogo
        """
        super().__init__()

        self.interfaz = interfaz

        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon("src/recursos/RecetarioLogo.png"))

        self.resultado = ""

        self.widget_dialogo = QListWidget()

        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila = 0

        # Si se va a crear un nuevo ingrediente o se va a editar, usamos el mismo diálogo

        titulo = ""
        if (ingrediente == None):
            titulo = "Nuevo ingrediente"
        else:
            titulo = "Editar ingrediente"

        self.setWindowTitle("Recetario - {}".format(titulo))

        # Creación de las etiquetas y los campos de texto
        etiqueta_nombre = QLabel("Nombre")
        distribuidor_dialogo.addWidget(etiqueta_nombre, numero_fila, 0)

        self.texto_nombre = QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_nombre, numero_fila, 1)
        numero_fila = numero_fila + 1

        unidad = QLabel("Unidad")
        distribuidor_dialogo.addWidget(unidad, numero_fila, 0)

        self.texto_unidad = QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_unidad, numero_fila, 1)
        numero_fila = numero_fila + 1

        etiqueta_valor = QLabel("Valor")
        distribuidor_dialogo.addWidget(etiqueta_valor, numero_fila, 0)
        

        self.texto_valor = QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_valor, numero_fila, 1)
        numero_fila = numero_fila + 1
        self.texto_valor.setInputMask("$0000000000000")

        etiqueta_sitioCompra = QLabel("Sitio compra")
        distribuidor_dialogo.addWidget(etiqueta_sitioCompra, numero_fila, 0)

        self.texto_sitioCompra = QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_sitioCompra, numero_fila, 1)
        numero_fila = numero_fila + 1

        # Creación de los botones para guardar o cancelar
        caja_botones = QGroupBox()
        caja_botones.setLayout(QHBoxLayout())
        caja_botones.setStyleSheet('''
                QGroupBox{border:none}''')

        self.btn_guardar = QPushButton("Guardar")
        caja_botones.layout().addWidget(self.btn_guardar)
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        caja_botones.layout().addWidget(self.btn_cancelar)
        self.btn_cancelar.clicked.connect(self.cancelar)

        distribuidor_dialogo.addWidget(caja_botones, numero_fila, 0, 1, 2)

        # Si el diálogo se va a usar para editar, se pone la información correspondiente en los campos de texto
        if (ingrediente != None):
            self.texto_nombre.setText(ingrediente["nombre"])
            self.texto_unidad.setText(ingrediente["unidad"])
            self.texto_valor.setText(str(ingrediente["valor"]))
            self.texto_sitioCompra.setText(ingrediente["sitioCompra"])

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

