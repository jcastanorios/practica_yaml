from PyQt5.QtWidgets import QApplication
from .VistaListaRecetas import VistaListaRecetas
from .VistaReceta import VistaReceta
from .VistaListaIngredientes import VistaListaIngredientes
from .VistaListaRecetas import VistaListaRecetas
#from .VistaPersonasPreparacion import VistaPersonasPreparacion
from .VistaPreparacion import VistaPreparacion
from .VistaListaIngredientesReceta import VistaListaIngredientesReceta


class App_Recetario(QApplication):
    """
    Clase principal de la interfaz que coordina las diferentes vistas/ventanas de la aplicación
    """

    def __init__(self, sys_argv, logica):
        """
        Constructor de la interfaz. Debe recibir la lógica e iniciar la aplicación en la ventana principal.
        """
        super(App_Recetario, self).__init__(sys_argv)

        self.logica = logica
        self.mostrar_vista_lista_recetas()

    def mostrar_vista_lista_recetas(self):
        """
        Esta función inicializa la ventana de lista de recetas
        """
        self.vista_lista_recetas = VistaListaRecetas(self)
        self.vista_lista_recetas.mostrar_recetas(self.logica.dar_recetas())

    def crear_receta(self):
        """
        Esta función muestra la ventana para crear una receta
        """
        self.mostrar_receta()

    def mostrar_receta(self, id_receta=-1):
        """
        Esta función muestra la información de una receta
        """
        self.receta_actual = id_receta
        if id_receta != -1:
            self.mostrar_ventana_receta(self.logica.dar_receta(self.receta_actual))
        else:
            self.mostrar_ventana_receta(None)
    
    def eliminar_receta(self, indice):
        """
        Esta función permite eliminar una receta
        """
        self.logica.eliminar_receta(indice)
        self.vista_lista_recetas.mostrar_recetas(self.logica.dar_recetas())
		
    def mostrar_ventana_receta(self, receta):
        """
        Esta función muestra la ventana con la información de una receta
        """
        self.vistaReceta = VistaReceta(self)
        self.vistaReceta.mostrar_receta(receta)


    def guardar_receta(self, receta, tiempo, personas, calorias, preparacion):
        """
        Esta función permite crear una nueva receta o los cambios sobre una existente
        """
        validacion = self.logica.validar_crear_editar_receta(self.receta_actual, receta, tiempo, personas, calorias, preparacion)
        if validacion == "":
            if self.receta_actual == -1:
                self.logica.crear_receta(receta, tiempo, personas, calorias, preparacion)
            else:
                self.logica.editar_receta(self.receta_actual, receta, tiempo, personas, calorias, preparacion)
            self.vista_lista_recetas.mostrar_recetas(self.logica.dar_recetas())
        return validacion
    
    def mostrar_ingredientes(self):
        """
        Esta función muestra la ventana con la lista de ingredientes
        """
        self.vista_lista_ingredientes=VistaListaIngredientes(self)
        self.vista_lista_ingredientes.mostrar_ingredientes(self.logica.dar_ingredientes())

    def crear_ingrediente(self, nombre, unidad, valor, sitioCompra):
        """
        Esta función permite crear un nuevo ingrediente
        """
        id_creacion = -1
        validacion = self.logica.validar_crear_editar_ingrediente(id_creacion, nombre, unidad, valor, sitioCompra)
        if validacion == "":
            self.logica.crear_ingrediente(nombre, unidad, valor, sitioCompra)
        else:
            self.vista_lista_ingredientes.error(validacion)
        self.vista_lista_ingredientes.mostrar_ingredientes(self.logica.dar_ingredientes())
        return validacion

    def editar_ingrediente(self, id, nombre, unidad, valor, sitioCompra):
        """
        Esta función permite editar un ingrediente
        """
        validacion = self.logica.validar_crear_editar_ingrediente(id, nombre, unidad, valor, sitioCompra)
        if validacion == "":
            self.logica.editar_ingrediente(id, nombre, unidad, valor, sitioCompra)
        else:
            self.vista_lista_ingredientes.error(validacion)

    def eliminar_ingrediente(self, indice):
        """
        Esta función permite eliminar un ingrediente
        """
        self.logica.eliminar_ingrediente(indice)
        self.vista_lista_ingredientes.mostrar_ingredientes(self.logica.dar_ingredientes())


    def agregar_ingrediente_receta(self, receta, ingrediente, cantidad):
        """
        Esta función permite registrar un ingrediente a una receta especifica
        """

        validacion = self.logica.validar_crear_editar_ingReceta(receta, ingrediente, cantidad)
        if validacion == "":
            self.logica.agregar_ingrediente_receta(receta, ingrediente, cantidad)
        else:
            self.vista_lista_ingReceta.error(validacion)


    
    def editar_ingrediente_receta(self, id_ingrediente_receta,receta, ingrediente, cantidad):
        """
        Esta función permite registrar un ingrediente de una receta especifica
        """
        validacion = self.logica.validar_crear_editar_ingReceta(receta, ingrediente, cantidad)
        if validacion == "":
            self.logica.editar_ingrediente_receta(id_ingrediente_receta,receta, ingrediente, cantidad)
        else:
            self.vista_lista_ingReceta.error(validacion)

			
    def eliminar_ingrediente_receta(self, indice, receta):
        """
        Esta función permite eliminar un ingrediente de una receta especifica
        """
        self.logica.eliminar_ingrediente_receta(indice, receta)
		

    def mostrar_ingredientes_receta(self, receta):
        """
        Esta función muestra la ventana con la lista de ingredientes de una receta
        """
        ingredientes = self.logica.dar_ingredientes()
        self.vista_lista_ingReceta = VistaListaIngredientesReceta(self, receta, ingredientes)
        self.vista_lista_ingReceta.mostrar_ing_receta(self.logica.dar_ingredientes_receta(self.receta_actual))


    def mostrar_preparacion(self, id_receta, cantidad_personas):
        """
        Esta función muestra la preparacieon de una receta para un número de personas
        """
        self.datos_preparacion = self.logica.dar_preparacion(id_receta, cantidad_personas)
        self.vista_reporte = VistaPreparacion( self, self.datos_preparacion['receta'])
        self.vista_reporte.mostrar_datos(self.datos_preparacion)

