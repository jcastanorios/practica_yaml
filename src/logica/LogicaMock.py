'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
from src.logica.FachadaRecetario import FachadaRecetario


class LogicaMock(FachadaRecetario):


    def __init__(self):
        #Este constructor contiene los datos falsos para probar la interfaz
        self.recetas = [{'nombre': 'Ajiaco', 'tiempo': "01:00", 'personas': 6, 'calorias': 200, 'preparacion': 'Poner en una olla el agua, la pechuga de pollo, la cebolla larga (o su equivalente en otras variedades), guascas frescas y el ramillete de cilantro (atado con cuerda para cocinar o con una tira de cáscara de mazorca), los ajos, sal y pimienta (opcional). Dejar hervir por 20 minutos.Sacar la pechuga con un poco del caldo. Desmenuzarla cuando se enfríe. Reservar en un recipiente. Lavar, pelar y cortar las papas en rodajas. Incorporar más guascas frescas y los trozos de mazorcas limpias sin hojas. Poner las papas rojas, sabaneras o las papas amarillas primero por 10 minutos en el caldo hirviendo. Pasados 10 minutos se agrega la papa pastusa.'},
                        {'nombre': 'Berenjenas parmesanas', 'tiempo': "00:30", 'personas': 4, 'calorias': 100, 'preparacion': 'Cortar las berenjenas con cascara de 1/2 cm y colocarlas en un colador haciendo capas intercalando con pizcas de sal entrefina. Dejar escurrir media hora para eliminar un poco su amargor. Secarlas con una servilleta, pasarlas por harina, retirar el exceso y freír en aceite de oliva siempre a fuego bajo, no tienen que quedar crocantes, deben quedar cremosas en su interior. Intercalar en una bandeja para horno la salsa de tomate, berenjenas, mozzarella, salsa, como mínimo 3 capas. Terminar con salsa, mozzarella y queso rallado.'}
                        ]
        
        self.ingredientes = [{'nombre': 'Tomate chonto', 'unidad': 'libra', 'valor': 5000, 'sitioCompra': 'Fruver El mejor'},
                             {'nombre': 'Cebolla larga', 'unidad': 'libra', 'valor': 4000, 'sitioCompra': 'Fruver El mejor'},
                             {'nombre': 'Papa criolla', 'unidad': 'libra', 'valor': 4090, 'sitioCompra': 'Plaza Concordia'},
                             {'nombre': 'Papa pastusa', 'unidad': 'libra', 'valor': 1890, 'sitioCompra': 'Plaza Concordia'},
                             {'nombre': 'Aguacate', 'unidad': 'unidad', 'valor': 5000, 'sitioCompra': 'Plaza Concordia'},
                             {'nombre': 'Berenjenas', 'unidad': 'libra', 'valor': 3800, 'sitioCompra': 'Plaza Concordia'}
                             ]
        
        self.ingredientes_recetas = [{'receta': 'Ajiaco', 'ingrediente': 'Papa pastusa', 'unidad': 'libra', 'cantidad': 2},
                                    {'receta': 'Ajiaco', 'ingrediente': 'Papa criolla', 'unidad': 'libra', 'cantidad': 2},
                                    {'receta': 'Ajiaco', 'ingrediente': 'Aguacate', 'unidad': 'unidad', 'cantidad': 1},
                                    {'receta': 'Berenjenas parmesanas', 'ingrediente': 'Berenjenas', 'unidad': 'libra', 'cantidad': 2},
                                    {'receta': 'Berenjenas parmesanas', 'ingrediente': 'Tomate chonto', 'unidad': 'libra', 'cantidad': 3}
                                    ] 
        self.preparacion = {'receta': 'Ajiaco', 'personas': 8, 'calorias': 750, 'costo': 55650, 'tiempo_preparacion':'4:00:00', 
                            'datos_ingredientes':[{'nombre': 'Cebolla larga', 'unidad': 'libra', 'cantidad': 2,'valor': 8000},
                             {'nombre': 'Papa criolla', 'unidad': 'libra', 'cantidad': 2, 'valor': 8180},
                             {'nombre': 'Papa pastusa', 'unidad': 'libra', 'cantidad': 4, 'valor': 4000},
                             {'nombre': 'Aguacate', 'unidad': 'unidad', 'cantidad': 2,'valor': 10000}]}



    def dar_recetas(self):
        return self.recetas.copy()
    
    def dar_receta(self, id_receta):
        return self.recetas[id_receta].copy()
    
    def validar_crear_editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        return ""
    
    def crear_receta(self, receta, tiempo, personas, calorias, preparacion):
        self.recetas.append({'nombre': receta, 'tiempo': tiempo, 'personas': personas, 'calorias': calorias, 'preparacion': preparacion})

    def editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        self.recetas[id_receta]['nombre'] = receta
        self.recetas[id_receta]['tiempo'] = tiempo
        self.recetas[id_receta]['personas'] = personas
        self.recetas[id_receta]['calorias'] = calorias
        self.recetas[id_receta]['preparacion'] = preparacion

    def eliminar_receta(self, id_receta):
        del self.recetas[id_receta]


    def dar_ingredientes(self):
        return self.ingredientes.copy()
    
    def dar_ingrediente(self, id_ingrediente):
        return self.ingredientes[id_ingrediente].copy()

    def validar_crear_editar_ingrediente(self, nombre, unidad, valor, sitioCompra):
        return ""
		
    def crear_ingrediente(self, nombre, unidad, valor, sitioCompras):
        self.ingredientes.append({'nombre': nombre, 'unidad': unidad, 'valor': valor, 'sitioCompra': sitioCompras})
 

    def editar_ingrediente(self, id_ingrediente, nombre, unidad, valor, sitioCompras):
        self.ingredientes[id_ingrediente]['nombre'] = nombre
        self.ingredientes[id_ingrediente]['unidad'] = unidad
        self.ingredientes[id_ingrediente]['valor'] = valor
        self.ingredientes[id_ingrediente]['sitioCompra'] = sitioCompras


    def eliminar_ingrediente(self, id_ingrediente):
        del self.ingredientes[id_ingrediente]

    def dar_ingredientes_receta(self, id_receta):
        receta = self.dar_receta(id_receta)
        return list(filter(lambda x: x['receta'] == receta['nombre'], self.ingredientes_recetas))
    
    def agregar_ingrediente_receta(self, receta, ingrediente, cantidad):
        self.ingredientes_recetas.append({'receta': receta['nombre'], 'ingrediente': ingrediente['nombre'], 'unidad': ingrediente['unidad'],'cantidad': cantidad})

    def editar_ingrediente_receta(self, id_ingrediente_receta, receta, ingrediente, cantidad):
        ingredientes_receta = list(filter(lambda x: x['receta'] == receta['nombre'], self.ingredientes_recetas))
        ingredientes_receta[id_ingrediente_receta]['ingrediente'] = ingrediente['nombre']
        ingredientes_receta[id_ingrediente_receta]['cantidad'] = cantidad

    def eliminar_ingrediente_receta(self, id_ingrediente_receta, receta):
        indice_en_receta = 0
        iteracion = 0
        for ingrediente_receta in self.ingredientes_recetas:
            if ingrediente_receta['receta'] == receta['nombre']:
                if indice_en_receta == id_ingrediente_receta:
                    del self.ingredientes_recetas[iteracion]
				
                indice_en_receta+=1
			
            iteracion+=1

    def validar_crear_editar_ingReceta(self,receta, ingrediente, cantidad):
        return ""

    def dar_preparacion(self, id_receta,cantidad_personas):
        return self.preparacion

