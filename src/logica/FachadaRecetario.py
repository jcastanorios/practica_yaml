'''
Esta clase es la fachada con los métodos a implementar en la lógica
'''
class FachadaRecetario:

    def dar_recetas(self):
        ''' Retorna la lista de recetas registradas en el sistema
        Retorna:
            (list): La lista con los objetos de recetas
        '''
        raise NotImplementedError("Método no implementado")
    
    def dar_receta(self, id_receta):
        ''' Retorna una receta a partir de su identificador
        Parámetros:
            id_receta (int): El identificador de la receta a retornar
        Retorna:
            (dict): La receta identificada con el id_receta recibido como parámetro
        '''
        raise NotImplementedError("Método no implementado")
    

    def validar_crear_editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        ''' Valida que una receta se pueda crear o editar
        Parámetros:
            receta (string): El nombre de la receta
            tiempo (string): El tiempo de preparación de la receta
            personas (string): La cantidad de personas de la receta
            calorias (string): Calorías por porción
            preparación (string): Proceso de preparación de la receta
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        raise NotImplementedError("Método no implementado")
    
    def crear_receta(self,receta, tiempo, personas, calorias, preparacion):
        ''' Crea una nueva receta
        Parámetros:
            receta (string): El nombre de la receta
            tiempo (string): El tiempo de preparación de la receta
            personas (string): La cantidad de personas de la receta
            calorias (string): Calorías por porción
            preparación (string): Proceso de preparación de la receta
        '''
        raise NotImplementedError("Método no implementado")

    def editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        ''' Edita los datos de una receta
        Parámetros:
            receta (string): El nombre de la receta
            tiempo (string): El tiempo de preparación de la receta
            personas (string): La cantidad de personas de la receta
            calorias (string): Calorías por porción
            preparación (string): Proceso de preparación de la receta
        '''
        raise NotImplementedError("Método no implementado")

    def eliminar_receta(self, id_receta):
        ''' Elimina una receta de la lista de recetas
        Parámetros:
            id_receta (int): El identificador de la receta que se desea eliminar
        '''
        raise NotImplementedError("Método no implementado")
    

    def dar_ingredientes(self):
        ''' Retorna la lista de ingredientes
        Retorna:
            (list): La lista con los dict o los objetos de los ingredientes
        '''
        raise NotImplementedError("Método no implementado")
    
    def dar_ingrediente(self, id_ingrediente):
        ''' Retorna un ingrediente dado su id
        Retorna:
            (dict): el ingrediente identificado con el id_ingrediente recibido como parámetro
        '''
        raise NotImplementedError("Método no implementado")

    def validar_crear_editar_ingrediente(self, nombre, unidad, valor, sitioCompra):
        ''' Valida que un ingrediente se pueda crear o editar
        Parámetros:
            nombre (string): El nombre del ingrediente
            unidad (string): Unidad
            valor (string): Valor del ingrediente para la unidad
            sitioCompra (string): lugar en el que se compra el ingrediente
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        raise NotImplementedError("Método no implementado")
    def crear_ingrediente(self, nombre, unidad, valor, sitioCompra):
        ''' Valida que un ingrediente se pueda crear o editar
        Parámetros:
            nombre (string): El nombre del ingrediente
            unidad (string): Unidad
            valor (string): Valor del ingrediente para la unidad
            sitioCompra (string): lugar en el que se compra el ingrediente
        Retorna:
            (string): El mensaje de error generado al presentarse errores en la
            validación o una cadena de caracteres vacía si no hay errores.
        '''
        raise NotImplementedError("Método no implementado")


    def editar_ingrediente(self, id_ingrediente, nombre, unidad, valor, sitioCompras):
        ''' Edita un ingrediente
        Parámetros:
            id_ingrediente(int): El identificador del ingrediente que se va a editar
            nombre (string): El nombre del ingrediente
            unidad (string): Unidad
            valor (string): Valor del ingrediente para la unidad
            sitioCompra (string): lugar en el que se compra el ingrediente
        '''
        raise NotImplementedError("Método no implementado")

    def eliminar_ingrediente(self, id_ingrediente):
        ''' Elimina un ingrediente de la lista de ingredientes
        Parámetros:
            id_ingrediente (int): El identificador del ingrediente que se desea eliminar
        '''
        raise NotImplementedError("Método no implementado")
    
    def dar_ingredientes_receta(self, id_receta):
        ''' Retorna el listado de ingredientes de una receta dado si id
        Parámetros:
            id_receta (int): El identificador de la receta 
        Retorna:
            (list) : listado de ingredientes de la receta
        '''
        raise NotImplementedError("Método no implementado")
    
    def agregar_ingrediente_receta(self, receta, ingrediente, cantidad):
        ''' agregar el ingrediente a la recceta con la cantidad 
        Parámetros:
            receta  : La receta
            ingrediente: El ingrediente que se va a agregar a la recita
            cantidad: cantidad del ingredeite para la receta

        '''
   
    def editar_ingrediente_receta(self, id_ingrediente_receta, receta, ingrediente, cantidad):
        ''' Edita los datos de un ingrediente
        Parámetros:
            id_ingrediente_receta identificador de la receta
            receta:receta a la que pertene
            ingrediente: ingrediente de la receeta
            cantidad: cantidad del ingrendiente para la receta
        
        '''

    def validar_crear_editar_ingReceta(self,receta, ingrediente, cantidad):
        ''' Valida si se puede crear o editar un ingrediente de una recieta
        Parámetros:
            receta:receta a la que pertenece
            ingrediente: ingrediente de la receeta
            cantidad: cantidad del ingrendiente para la receta
        '''

    def eliminar_ingrediente_receta(self, id_ingrediente_receta, receta):
        ''' Elimina un ingrediente de una receta de su lista de ingredientes
        Parámetros:
            id_ingrediente_receta (int): El identificador del ingrediente de la receta que se desea eliminar
            receta:receta a la que pertenece
        '''
        raise NotImplementedError("Método no implementado")
		
    def dar_preparacion(self, id_receta,cantidad_personas):
        ''' retorna los datos de preparación de una receta para cantidad de personas que entra como parametro
        Parámetros:
            id_receta: identificador de la receta que se va a preparar
            cantidad_personas: cantidad personas para las que se va a preparar la receta
        Retorna:
            (dic) diccionario con los datos de preparacion de la receta: nombre, cantidad peronas, calorias, costo, tiempo de preparacion},
                  (list) ingredientes de la receta 
        '''
