import unittest
import random
from faker import Faker
import locale
from datetime import datetime
from src.logica.Recetario import Recetario
from src.modelo.receta import Receta
from src.modelo.ingrediente import Ingrediente, RecetaIngrediente
from src.modelo.declarative_base import Session, engine, Base


class RecetarioTestCase(unittest.TestCase):
    def test_prueba(self):
        self.assertEqual(0, 0)

    def setUp(self):
        #Crea una colección para hacer las pruebas
        self.Recetario = Recetario()

        #Abre la sesión
        self.session = Session()

        # Crear una instancia de Faker
        self.data_factory = Faker()
        Faker.seed(1000)

        # Limpiar la tabla de recetas
        self.session.query(Receta).delete()

        # Limpiar la tabla de ingredientes
        self.session.query(Ingrediente).delete()

        # Limpiar la tabla de recetas-ingredientes
        self.session.query(RecetaIngrediente).delete()

        # Generar y persistir ingredientes
        self.data_ingredientes = self.generate_ingredientes()
        self.persist_ingredientes()

        # Generar y persistir recetas
        self.data_recetas = self.generate_recetas()
        self.persist_recetas()

        self.asociar_ingredientes_recetas()

    def asociar_ingredientes_recetas(self):
        '''Asociar ingredientes aleatorios a las recetas'''
        for receta in self.recetas:
            num_ingredientes = min(3, len(self.ingredientes))
            ingredientes_asociados = random.sample(self.ingredientes, num_ingredientes)

            for ingrediente in ingredientes_asociados:
                cantidad = random.randint(1, 30)
                receta_ingrediente = RecetaIngrediente(
                    ingrediente_id=ingrediente.id,
                    receta_id=receta.id,
                    cantidad=cantidad
                )
                self.session.add(receta_ingrediente)
        self.session.commit()

    def generate_recetas(self):
        '''Generar datos aleatorios para recetas'''
        data_recetas = []
        for _ in range(10):
            tiempo_str = self.data_factory.time(pattern='%H:%M:%S')
            tiempo = datetime.strptime(tiempo_str, '%H:%M:%S').time()
            nombre = self.data_factory.unique.name()[:255]
            preparacion = self.data_factory.text(max_nb_chars=255)

            data_recetas.append((
                nombre,
                tiempo,
                self.data_factory.random_int(1, 10),
                self.data_factory.random_int(100, 1000),
                preparacion
            ))
        return data_recetas

    def generate_ingredientes(self):
        '''Generar datos aleatorios para ingredientes'''
        data_ingredientes = []
        for _ in range(10):
            nombre_ingrediente = self.data_factory.unique.word()
            unidad = self.data_factory.random_element(elements=("kg", "g", "L", "ml", "unidad"))
            valor = self.data_factory.random_int(1000, 100000)
            sitio_compra = self.data_factory.word()

            data_ingredientes.append((
                nombre_ingrediente,
                unidad,
                valor,
                sitio_compra
            ))
        return data_ingredientes

    def persist_recetas(self):
        '''Persistir las recetas generadas'''
        self.recetas = []
        for datos in self.data_recetas:
            receta = Receta(
                nombre=datos[0],
                tiempo=datos[1],
                personas=datos[2],
                calorias=datos[3],
                preparacion=datos[4]
            )
            self.session.add(receta)
            self.recetas.append(receta)
        self.session.commit()

    def persist_ingredientes(self):
        '''Persistir los ingredientes generados'''
        self.ingredientes = []
        for datos in self.data_ingredientes:
            ingrediente = Ingrediente(
                nombre=datos[0],
                unidad=datos[1],
                valor=datos[2],
                sitioCompra=datos[3]
            )
            self.session.add(ingrediente)
            self.ingredientes.append(ingrediente)
        self.session.commit()

    def test_constructor(self):
        '''Verificar que las recetas e ingredientes se crearon correctamente'''
        for receta, datos_receta in zip(self.recetas, self.data_recetas):
            self.assertEqual(receta.nombre, datos_receta[0], "Los nombres de las recetas no coinciden")
            self.assertEqual(receta.tiempo, datos_receta[1], "Los tiempos de las recetas no coinciden")
            self.assertEqual(receta.personas, datos_receta[2], "El número de personas de las recetas no coincide")
            self.assertEqual(receta.calorias, datos_receta[3], "Las calorías de las recetas no coinciden")
            self.assertEqual(receta.preparacion, datos_receta[4], "Las preparaciones de las recetas no coinciden")

        for receta in self.recetas:
            ingredientes_asociados = receta.ingredientes
            self.assertTrue(all(isinstance(ingrediente, Ingrediente) for ingrediente in ingredientes_asociados),
                "No todos los elementos asociados a la receta son instancias de Ingrediente")
            
        for ingrediente, datos_ingrediente in zip(self.ingredientes, self.data_ingredientes):
            self.assertEqual(ingrediente.nombre, datos_ingrediente[0], "Los nombres de los ingredientes no coinciden")
            self.assertEqual(ingrediente.unidad, datos_ingrediente[1], "Las unidades de los ingredientes no coinciden")
            self.assertEqual(ingrediente.valor, datos_ingrediente[2], "Los valores de los ingredientes no coinciden")
            self.assertEqual(ingrediente.sitioCompra, datos_ingrediente[3], "Los sitios de compra de los ingredientes no coinciden")

    def tearDown(self):
        #Abre la sesión
        self.session = Session()
        """
        #Consulta todas las recetas
        busqueda_Receta = self.session.query(Receta).all()
        
        #Borra todas las recetas
        for receta in busqueda_Receta:
            self.session.delete(receta)
        
        #Consulta todos los ingredientes
        busqueda_Ingrediente = self.session.query(Ingrediente).all()

        #Borra todos los ingredientes
        for ingrediente in busqueda_Ingrediente:
            self.session.delete(ingrediente)
        
        #Consulta todas los ingredientes en las recetas
        busqueda_RecetaIngrediente = self.session.query(RecetaIngrediente).all()
        
        #Borra todas las recetas
        for recIng in busqueda_RecetaIngrediente:
            self.session.delete(recIng)
        
        """
        self.session.commit()
        self.session.close()
  
    def test_dar_recetas_sin_datos(self):
        '''Prueba cuando la tabla Recetas está vacía, el método dar_recetas devuelve una lista vacía'''
        # Limpiar la tabla de recetas
        self.session.query(Receta).delete()
        self.session.commit()

        # Obtener lista de recetas
        recetas = self.Recetario.dar_recetas()

        # Verificar que la lista esté vacía
        self.assertEqual(len(recetas), 0,"El listado de recetas debería estar vacío")
        if (len(recetas) == 0):
            print("Prueba dar recetas con tabla vacía: OK")

    def test_dar_mas_recetas(self):
        '''Prueba que el método dar_recetas devuelve una lista de 10 recetas cuando hay  10 recetas en la tabla'''
        # Obtener el listado de recetas
        listado_recetas = self.Recetario.dar_recetas()

        # Obtener las recetas almacenadas en la tabla
        recetas_tabla = self.session.query(Receta).all()

        # Verificar que el número de recetas sea igual en ambos conjuntos de datos
        self.assertEqual(len(listado_recetas), len(recetas_tabla), "El número de recetas no coincide")

        print("Prueba dar recetas con tabla llena: OK")
    
    def test_dar_ingredientes_sin_datos(self):
        '''Prueba cuando la tabla Ingredientes está vacía, el método dar_ingredientes devuelve una lista vacía'''
        # Limpiar la tabla de ingredientes
        self.session.query(Ingrediente).delete()
        self.session.commit()

        # Obtener lista de ingredientes
        ingredientes = self.Recetario.dar_ingredientes()

        # Verificar que la lista esté vacía
        self.assertEqual(len(ingredientes), 0,"El listado de recetas debería estar vacío")
        print("Prueba dar ingredientes con tabla vacía: OK")
    
    def test_dar_mas_ingredientes(self):
        '''Prueba que el método dar_ingrediente devuelve una lista de 10 ingredientes cuando hay  10 ingredientes en la tabla'''
        # Obtener el listado de ingrediente
        listado_ingredientes = Recetario.dar_ingredientes(self.session)

        # Obtener los ingredientes almacenados en la tabla
        ingredientes_tabla = self.session.query(Ingrediente).all()

        # Verificar que el número de ingredientes sea igual en ambos conjuntos de datos
        self.assertEqual(len(listado_ingredientes), len(ingredientes_tabla), "El número de ingredientes no coincide")

        print("Prueba dar ingredientes con tabla llena: OK") 
    
    def test_dar_ingredientes_ordenados_nombre(self):
        '''Prueba que el método dar_ingrediente devuelve una lista ordenada en orden alfabético'''
        # Obtener el listado de ingrediente
        listado_ingredientes = Recetario.dar_ingredientes(self.session) 

        # Extraer los nombres de los ingredientes
        nombres_ingredientes = [ingrediente['nombre'] for ingrediente in listado_ingredientes]

        # Verificar si los nombres están ordenados alfabéticamente
        self.assertEqual(nombres_ingredientes, sorted(nombres_ingredientes), "Los nombres de los ingredientes no están ordenados alfabéticamente")
        print("Prueba dar ingredientes ordenados alfabéticamente por nombre: OK") 

    def test_dar_ingredientes_ordenados_nombre_unidad(self):
        '''Prueba que el método dar_ingrediente devuelve una lista ordenada en orden alfabético el nombre y la unidad'''
        # Repetir otro ingrediente de la tabla cambiando solo el valor de la unidad
        otro_ingrediente = self.data_ingredientes[0]
        otro_ingrediente = (otro_ingrediente[0], "onza", otro_ingrediente[2], otro_ingrediente[3])

        ingrediente_repetido = Ingrediente(
            nombre=otro_ingrediente[0],
            unidad=otro_ingrediente[1],
            valor=otro_ingrediente[2],
            sitioCompra=otro_ingrediente[3]
        )
        self.session.add(ingrediente_repetido)

        # Persistir los objetos
        self.session.commit()

        # Obtener el listado de ingredientes
        listado_ingredientes = Recetario.dar_ingredientes(self.session)

        # Verificar que los ingredientes estén ordenados alfabéticamente por nombre
        nombres_ordenados = [ingrediente['nombre'] for ingrediente in listado_ingredientes]
        self.assertEqual(nombres_ordenados, sorted(nombres_ordenados), "Los ingredientes no están ordenados alfabéticamente por nombre")

        # Verificar que cada nombre de ingrediente esté ordenado por unidad
        for nombre in set(nombres_ordenados): 
            ingredientes_nombre = [ingrediente for ingrediente in listado_ingredientes if ingrediente['nombre'] == nombre]
            unidades_ordenadas = [ingrediente['unidad'] for ingrediente in ingredientes_nombre]
            self.assertEqual(unidades_ordenadas, sorted(unidades_ordenadas), f"Los ingredientes bajo el nombre '{nombre}' no están ordenados alfabéticamente por unidad")
        print("Prueba dar ingredientes ordenados alfabéticamente por nombre y unidad: OK")
    
    def test_formato_valor_ingredientes(self):
        '''Prueba que el metodo dar ingredientes entregue el formato del valor correctamente'''
        # Obtener el listado de ingredientes
        lista_ingredientes = Recetario.dar_ingredientes(self.session)
        # Verificar que el formato del valor de cada ingrediente sea el correcto
        # Verificar el formato de los valores
         # Verificar el formato de los valores
        for ingrediente in lista_ingredientes:
            self.assertTrue(ingrediente['valor'].startswith('$'), "El valor no comienza con el símbolo de dólar")
            # Obtener el valor numérico sin el símbolo de dólar y el punto como separador de miles
            valor_numerico = ingrediente['valor'][1:].replace('.', '', 1)
            # Verificar si el valor numérico restante es un número válido
            self.assertTrue(valor_numerico.replace(',', '').isdigit(), f"El valor '{ingrediente['valor']}' no es un número válido con separador de miles y sin decimales")
        print("Prueba dar ingredientes formato valor: OK ")

    def test_dar_recetas_ordenadas(self):
        '''Prueba dar recetas ordenadas alfabéticamente por nombre'''
        # Obtener el listado de recetas
        listado_recetas = Recetario.dar_recetas(self.session)

        # Extraer los nombres de las recetas en el listado
        nombres_recetas = [receta['nombre'] for receta in listado_recetas]

        # Verificar que las recetas estén ordenadas alfabéticamente
        self.assertEqual(nombres_recetas, sorted(nombres_recetas), "Las recetas no están ordenadas alfabéticamente")
        print("Prueba dar recetas ordenadas alfabéticamente por nombre: OK ")

    def test_nombre_ingrediente_excede_caracteres(self):
        '''Prueba nombre excede 255 caracteres'''
        id=1
        nombre = "a" * 256
        unidad = "kilos"
        valor = "5000"
        sitioCompra = "Alkosto"

        resultado = Recetario.validar_crear_editar_ingrediente(self,id,nombre,unidad,valor,sitioCompra)
        self.assertEqual(resultado,"El nombre del ingrediente no puede superar los 255 caracteres.")
        print("Prueba nombre excede 255 carácteres: OK")

    def test_unidad_ingrediente_excede_caracteres(self):
        '''Prueba unidad excede 255 caracteres'''
        id=1
        nombre = "Papa" 
        unidad = "kilos" * 256
        valor = "5000"
        sitioCompra = "Alkosto"

        resultado = Recetario.validar_crear_editar_ingrediente(self,id, nombre,unidad,valor,sitioCompra)
        self.assertEqual(resultado,"La unidad de medida no puede superar los 255 caracteres.")
        print("Prueba unidad excede 255 carácteres: OK")

    def test_sitioCompra_ingrediente_excede_caracteres(self):
        '''Prueba sitioCompra excede 255 caracteres'''
        nombre = "Papa" 
        unidad = "kilos" 
        valor = "5000"
        sitioCompra = "Alkosto" * 256

        resultado = Recetario.validar_crear_editar_ingrediente(self,1,nombre,unidad,valor,sitioCompra)
        self.assertEqual(resultado,"El sitio de compra no puede superar los 255 caracteres.") 
        print("Prueba sitioCompra excede 255 carácteres: OK")   
   
    def test_valor_ingrediente_menor_a_cero(self):
        '''Prueba valor ingrediente negativo'''
        id=1
        nombre = "Arroz"
        unidad = "Kilo"
        valor = "-1"
        sitioCompra = "Fruver la 23"

        resultado = Recetario.validar_crear_editar_ingrediente(self,id, nombre, unidad, valor, sitioCompra)
        self.assertEqual(resultado, "El valor del ingrediente no puede ser negativo")
        print("Prueba valor ingrediente menor a cero: OK")
    
    def test_valor_ingrediente_decimal(self):
        '''Prueba valor ingrediente decimal'''
        id=-1
        nombre = "Arroz"
        unidad = "Kilo"
        valor = "1000.1"
        sitioCompra = "Fruver la 23"

        resultado = self.Recetario.validar_crear_editar_ingrediente( id, nombre, unidad, valor, sitioCompra)
        self.assertEqual(resultado, "El valor del ingrediente debe ser un número entero")
        print("Prueba valor ingrediente con decimales: OK")
    
    def test_campos_incompletos(self):
        '''Prueba campos incompletos ingrediente'''
        # Prueba cuando todos los campos están vacíos
        resultado = Recetario.validar_crear_editar_ingrediente(self,1,'', '', '', '')
        self.assertEqual(resultado, "Todos los campos son obligatorios. Por favor, complete todos los campos.", "Error al validar campos vacíos")

        # Prueba cuando solo el campo 'nombre' está vacío
        resultado = Recetario.validar_crear_editar_ingrediente(self,1, '', 'unidad', 1, 'sitioCompra')
        self.assertEqual(resultado, "Todos los campos son obligatorios. Por favor, complete todos los campos.", "Error al validar campo 'nombre' vacío")

        # Prueba cuando solo el campo 'unidad' está vacío
        resultado = Recetario.validar_crear_editar_ingrediente(self,1, 'nombre', '', 1, 'sitioCompra')
        self.assertEqual(resultado, "Todos los campos son obligatorios. Por favor, complete todos los campos.", "Error al validar campo 'unidad' vacío")

        # Prueba cuando solo el campo 'valor' está vacío
        resultado = Recetario.validar_crear_editar_ingrediente(self,1,'nombre', 'unidad', '', 'sitioCompra')
        self.assertEqual(resultado, "Todos los campos son obligatorios. Por favor, complete todos los campos.", "Error al validar campo 'valor' vacío")

        # Prueba cuando solo el campo 'sitioCompra' está vacío
        resultado = Recetario.validar_crear_editar_ingrediente(self,1,'nombre', 'unidad', 1, '')
        self.assertEqual(resultado, "Todos los campos son obligatorios. Por favor, complete todos los campos.", "Error al validar campo 'sitioCompra' vacío")
        
        print("Prueba campos ingrediente incompletos: OK")

    def test_ingresar_ingrediente_existente(self):
        '''Prueba ingresar ingrediente existente'''
        otro_ingrediente = self.data_ingredientes[0]
        nombre=otro_ingrediente[0]
        unidad=otro_ingrediente[1]
        valor=otro_ingrediente[2]
        sitioCompra=otro_ingrediente[3]
        
        resultado = self.Recetario.validar_crear_editar_ingrediente(1, nombre, unidad, str(valor), sitioCompra)
        self.assertEqual(resultado,"Ya existe un ingrediente con el nombre y la unidad de medida.")
        print("Prueba ingresar ingrediente existente: OK")
    
    def test_agregar_ingrediente(self):
        '''Prueba agregar ingrediente'''
        nombre="Camarones"
        unidad="Unidad"
        valor="5000"
        sitioCompra="Proveedor X"

        resultado = Recetario.crear_ingrediente(self, nombre, unidad, valor, sitioCompra)
        self.assertEqual(resultado, "El ingrediente ha sido creado exitosamente.", "Error al crear el ingrediente")
        print("Prueba crear ingrediente: OK")

    def test_dar_receta_sin_datos(self):
        '''Prueba cuando la tabla Recetas está vacía, el método dar_receta devuelve un valor vacío'''
        # Limpiar la tabla de recetas
        self.session.query(Receta).delete()
        self.session.commit()

        # Obtener lista de recetas
        receta = self.Recetario.dar_receta(1)

        # Comprobar que la lista de recetas está vacía
        self.assertIsNone(receta, "La lista de recetas debe estar vacía")
        print("Prueba dar receta con tabla recetas vacía: OK")
   
    def test_dar_receta(self):
        '''Prueba método dar_receta, devuelve la receta solicitada'''
        numero_receta = random.randint(1, 5)
        # Obtener receta de la posición 1
        receta = self.Recetario.dar_receta(numero_receta)

        #Obtener lista de recetas ordenadas
        recetas_ordenadas = self.Recetario.dar_recetas()

       # Verificar si la receta devuelta está en la primera posición de las recetas ordenadas        
        self.assertEqual(receta['nombre'], recetas_ordenadas[numero_receta]['nombre'], 
                         "La receta devuelta no está en la primera posición de las recetas ordenadas")

        print("Prueba dar receta especifica: OK")
    
    def test_listar_ingredientes_receta_sin_ingredientes(self):
        '''Prueba dar ingredientes receta con receta sin ingredientes'''

        self.session.query(RecetaIngrediente).delete()
        self.session.commit()

        numero_receta = random.randint(1, 10)
        # Obtener los ingredientes de la receta
        ingredientes = self.Recetario.dar_ingredientes_receta(numero_receta)

        # Verificar que no haya ingredientes asociados
        self.assertEqual(len(ingredientes), 0,"El listado de ingredientes debería estar vacío")

        print("Prueba dar ingredientes receta sin ingredientes: OK")
    
    
    def test_listar_ingredientes_receta_con_ingredientes(self):
        '''Prueba dar ingredientes receta con receta con ingredientes'''

        numero_receta = random.randint(1, 10)
        # Obtener los ingredientes de la receta
        ingredientes = self.Recetario.dar_ingredientes_receta(numero_receta)

        # Verifica si cada elemento de la lista tiene las claves 'nombre', 'unidad' y 'cantidad'
        for ingrediente in ingredientes:
            self.assertIn('ingrediente', ingrediente)
            self.assertIn('unidad', ingrediente)
            self.assertIn('cantidad', ingrediente)


        print("Prueba dar ingredientes receta sin ingredientes: OK")
    
    def test_listar_ingredientes_receta_ordenados(self):
        '''Prueba dar ingredientes receta con receta con ingredientes ordenados alfabeticamente'''

        numero_receta = random.randint(1, 10)
        # Obtener los ingredientes de la receta
        ingredientes = self.Recetario.dar_ingredientes_receta(numero_receta)

        for ingrediente in ingredientes:
            self.assertIn('ingrediente', ingrediente)
            self.assertIn('unidad', ingrediente)
            self.assertIn('cantidad', ingrediente)

        ingredientes_ordenados = sorted(ingredientes, key=lambda x: (x['ingrediente'], x['unidad']))
        self.assertEqual(ingredientes, ingredientes_ordenados)

        print("Prueba dar ingredientes receta con ingredientes ordenados: OK")  
    
    def test_validar_crear_ingReceta_campos_no_vacios(self):
        '''Prueba crear ingrediente en receta con campos vacios'''
        
        listado_recetas = Recetario.dar_recetas(self.session)
        receta_aleatoria = random.choice(listado_recetas)
        
        #listado_ingredientes = Recetario.dar_ingredientes(self.session)
        #ingrediente_aleatorio = random.choice(listado_ingredientes)

        ingrediente_aleatorio = ""
        cantidad = ""

        resultado = self.Recetario.validar_crear_editar_ingReceta(receta_aleatoria,ingrediente_aleatorio,cantidad)

        self.assertEqual(resultado, "Los campos 'ingrediente' y 'cantidad' no pueden estar vacíos.")
    
    def test_validar_crear_ingReceta_campo_cantidad_invalido(self):
        '''Prueba crear ingrediente en receta con campos cantidad invalido'''
        
        listado_recetas = Recetario.dar_recetas(self.session)
        receta_aleatoria = random.choice(listado_recetas)

        listado_ingredientes = Recetario.dar_ingredientes(self.session)
        ingrediente_aleatorio = random.choice(listado_ingredientes)
        
        cantidad = "-50"
        resultado = self.Recetario.validar_crear_editar_ingReceta(receta_aleatoria,ingrediente_aleatorio,cantidad)
        self.assertEqual(resultado, "El valor del ingrediente no puede ser negativo")

        cantidad = "50.2"
        resultado = self.Recetario.validar_crear_editar_ingReceta(receta_aleatoria,ingrediente_aleatorio,cantidad)
        self.assertEqual(resultado, "La cantidad debe ser un número entero.")

        print("Prueba crear ingrediente en receta, cantidad invalida: OK")

    def test_validar_crear_ingReceta_ingrediente_existente(self):
        '''Prueba crear ingrediente en receta ingrediente existente'''
        ingReceta_tabla = self.session.query(RecetaIngrediente).all()
        ingReceta_aleatoria = random.choice(ingReceta_tabla)

        receta = self.session.query(Receta).filter_by(id=ingReceta_aleatoria.receta_id).first()
        recetaSelec = {
            'nombre': receta.nombre,
            'tiempo': str(receta.tiempo),
            'personas': str(receta.personas),
            'calorias': str(receta.calorias), 
            'preparacion': receta.preparacion
        }
        locale.setlocale(locale.LC_ALL,'')
        ingrediente = self.session.query(Ingrediente).filter_by(id=ingReceta_aleatoria.ingrediente_id).first()
        valor_formato = locale.format_string("%d",ingrediente.valor,grouping=True)
        
        ingredienteSelec = dict_ingrediente = {
            'nombre': ingrediente.nombre,
            'unidad': ingrediente.unidad,
            'valor':  str(f"${valor_formato}"),
            'sitioCompra': ingrediente.sitioCompra
        }
        resultado = self.Recetario.validar_crear_editar_ingReceta(recetaSelec, ingredienteSelec, ingReceta_aleatoria.cantidad)

        self.assertEqual(resultado, "El ingrediente ya se encuentra almacenado.")
        print("Prueba ingrediente en receta existente: OK")

    def test_agregar_ingrediente_receta(self):
        '''Prueba agregar ingrediente en receta'''
        # Encuentro un ingrediente
        ingrediente = self.session.query(Ingrediente).first()
        
        # Busco receta que no tenga ese ingrediente
        fila_sin_ingrediente = (
            self.session.query(RecetaIngrediente)
            .filter(RecetaIngrediente.ingrediente_id != ingrediente.id)
            .first()
        )
        print("Relacion: " + str(fila_sin_ingrediente.receta_id) + "y" + str(fila_sin_ingrediente.ingrediente_id))
        receta = self.session.query(Receta).filter_by(id=fila_sin_ingrediente.receta_id).first()
        recetaSelec = {
            'nombre': receta.nombre,
            'tiempo': str(receta.tiempo),
            'personas': str(receta.personas),
            'calorias': str(receta.calorias), 
            'preparacion': receta.preparacion
        }

        locale.setlocale(locale.LC_ALL,'')
        valor_formato = locale.format_string("%d", ingrediente.valor, grouping=True)
        
        ingredienteSelec = {
            'nombre': ingrediente.nombre,
            'unidad': ingrediente.unidad,
            'valor':  f"${valor_formato}",
            'sitioCompra': ingrediente.sitioCompra
        }
        
        #cantidad = random.randint(1, 100)
        cantidad= 159
        resultado = self.Recetario.agregar_ingrediente_receta(recetaSelec, ingredienteSelec, cantidad)
        
        # Verificar que el resultado sea una cadena no vacía
        self.assertTrue(resultado)

    #Prueba # 1 unitaria validación campos de creación de receta - campo nombre de la receta
    def test_agregar_receta_campo_nombre_no_debe_estar_vacio(self):
        '''Prueba agregar_receta_campo_nombre_no_debe_estar_vacio'''
        receta = self.generar_receta("", 
                                     datetime.strptime(self.data_factory.time(pattern='%H:%M:%S'), '%H:%M:%S').time(),
                                     self.data_factory.random_int(100, 1000),
                                     self.data_factory.text(max_nb_chars=255))
        
        resultado = Recetario.validar_crear_editar_receta(self, receta['id'], receta['nombre'], receta['tiempo'], receta['personas'], receta['calorias'], receta['preparacion']) 
        self.assertEqual(resultado, "El campo receta no debe estar vacío")
        print("Prueba agregar_receta_campo_nombre_no_debe_estar_vacio: OK")


    #Prueba # 2 unitaria validación campos de creación de receta - campo tiempo de la receta
    def test_agregar_receta_campo_tiempo_no_debe_estar_vacio_y_corresponde_al_formato(self):
        '''Prueba agregar_receta_campo_tiempo_no_debe_estar_vacio_y_corresponde_al_formato'''
        receta = self.generar_receta("Ajiaco", 
                                     "", 
                                     self.data_factory.random_int(100, 1000),
                                     self.data_factory.text(max_nb_chars=255))
        
        resultado = Recetario.validar_crear_editar_receta(self, receta['id'], receta['nombre'], receta['tiempo'], receta['personas'], receta['calorias'], receta['preparacion']) 
        self.assertEqual(resultado, "El campo Tiempo de preparación (horas) no debe estar vacío y debe tener el formato HH:MM:SS")
        print("Prueba agregar_receta_campo_tiempo_no_debe_estar_vacio_y_corresponde_al_formato: OK")
    
    #Prueba # 3 unitaria validación campos de creación de receta - campo calorias de la receta
    def test_agregar_receta_campo_calorias_por_porcion_no_debe_estar_vacio(self):
        '''Prueba agregar_receta_campo_calorias_no_debe_estar_vacio'''
        receta = self.generar_receta(
                                    "Ajiaco", 
                                    datetime.strptime(self.data_factory.time(pattern='%H:%M:%S'), '%H:%M:%S').time(), 
                                    "",
                                    self.data_factory.text(max_nb_chars=255))
        
        resultado = Recetario.validar_crear_editar_receta(self, receta['id'], receta['nombre'], str(receta['tiempo']), receta['personas'], receta['calorias'], receta['preparacion']) 
        self.assertEqual(resultado, "El campo \"Calorías por porción\" no debe estar vacío")
        print("Prueba agregar_receta_campo_tiempo_no_debe_estar_vacio_y_corresponde_al_formato: OK")

    #Prueba # 4 unitaria validación campos de creación de receta - campo preparación de la receta
    def test_agregar_receta_campo_preparacion_no_debe_estar_vacio(self):
        '''Prueba agregar receta campo preparacion no debe estar vacio'''
        receta = self.generar_receta(
                                    "Ajiaco", 
                                    datetime.strptime(self.data_factory.time(pattern='%H:%M:%S'), '%H:%M:%S').time(), 
                                    self.data_factory.random_int(100, 1000),
                                      "")
        
        resultado = Recetario.validar_crear_editar_receta(self, receta['id'], receta['nombre'], str(receta['tiempo']), receta['personas'], receta['calorias'], receta['preparacion']) 
        self.assertEqual(resultado, "El campo \"Preparación\" no debe estar vacío.")
        print("Prueba agregar receta campo preparacion no debe_estar vacio: OK")    

    #Prueba # 5 unitaria validación campos de creación de receta - campo personas de la receta
    def test_agregar_receta_campo_personas_debe_ser_un_numero_entero_positivo_mayor_a_cero(self):
        '''Prueba agregar_receta_campo_personas_debe_ser_un_numero_entero_positivo_mayor_a_cero'''
        receta = self.generar_receta(
                                    "Ajiaco", 
                                    datetime.strptime(self.data_factory.time(pattern='%H:%M:%S'), '%H:%M:%S').time(), 
                                    self.data_factory.random_int(100, 1000),
                                      self.data_factory.text(max_nb_chars=255))
        receta['personas']=-10
        resultado = Recetario.validar_crear_editar_receta(self, receta['id'], receta['nombre'], str(receta['tiempo']), receta['personas'], receta['calorias'], receta['preparacion']) 
        self.assertEqual(resultado, "El número de comensales de la receta no puede ser negativo")
        print("Prueba agregar receta campo personas debe ser un número_entero positivo mayor a cero: OK")    

    #Prueba # 6 unitaria validación campos de creación de receta - campo personas de la receta
    def test_agregar_receta_campo_personas_debe_ser_un_numero_entero(self):
        '''Prueba agregar_receta_campo_personas_debe_ser_un_numero_entero'''
        receta = self.generar_receta(
                                    "Ajiaco", 
                                    datetime.strptime(self.data_factory.time(pattern='%H:%M:%S'), '%H:%M:%S').time(), 
                                    self.data_factory.random_int(100, 1000),
                                      self.data_factory.text(max_nb_chars=255))
        receta['personas']=""
        try:
             Recetario.validar_crear_editar_receta(self, receta['id'], receta['nombre'], str(receta['tiempo']), receta['personas'], receta['calorias'], receta['preparacion'])
        except ValueError as ex:
            self.assertEquals(ex.args[0], "El número de comensales de la receta debe ser un número entero")
        
        print("Prueba agregar receta campo personas debe ser un número_entero: OK")    
    

    #Prueba # 7 unitaria validación campos de creación de receta - campo calorias de la receta
    def test_agregar_receta_campo_calorias_debe_ser_un_numero_entero(self):
        '''Prueba agregar_receta_campo_calorias_debe_ser_un_numero_entero'''
        receta = self.generar_receta(
                                    "Ajiaco", 
                                    datetime.strptime(self.data_factory.time(pattern='%H:%M:%S'), '%H:%M:%S').time(), 
                                    -1,
                                    self.data_factory.text(max_nb_chars=255))
        resultado=Recetario.validar_crear_editar_receta(self, receta['id'], receta['nombre'], str(receta['tiempo']), 
                                                        receta['personas'], receta['calorias'], receta['preparacion'])
        
        self.assertEqual(resultado,"El valor de las calorias de la receta debe ser un número entero positivo")
        
        print("Prueba agregar receta campo calorias debe ser un número_entero: OK")    
    



    #Método accesorio para creación de la receta
    def generar_receta(self, param_nombre, param_tiempo, param_calorias, param_preparacion):
        dict_receta = {
                'id':self.data_factory.random_int(100, 1000),
                'nombre': param_nombre,
                'tiempo': param_tiempo,
                'personas': self.data_factory.random_int(1, 10),
                'calorias': param_calorias,
                'preparacion': param_preparacion}
        return dict_receta

    #Pruebas preparar receta
    def test_preparar_receta(self):
        '''Prueba preparar receta'''
        recetas = self.session.query(Receta).all()
        recetas_ordenadas = sorted(recetas, key=lambda receta: receta.nombre)
        rango=len(recetas_ordenadas)-1
        if rango<0:
            rango=0

        indice = random.randint(0, rango)
        receta = recetas_ordenadas[indice]
        id_receta = recetas_ordenadas[indice].id
        personas_receta = receta.personas

        # Verificar si hay más de una persona en la receta antes de generar el número aleatorio
        if personas_receta > 1:
            # Generar un número aleatorio entre 1 y personas_receta - 1
            num_personas = random.randint(1, personas_receta - 1)
        else:
            # Si solo hay una persona, establecer num_personas en 1
            num_personas = 1

        
        result = self.Recetario.dar_preparacion(id_receta, num_personas)

        if not result:
            print("No se encontró ninguna receta para la preparación.")
            return

        # Comprobar que el resultado es un diccionario con las propiedades esperadas
        self.assertIsInstance(result, dict)
        self.assertIn('receta', result)
        self.assertIn('personas', result)
        self.assertIn('calorias', result)
        self.assertIn('costo', result)
        self.assertIn('tiempo_preparacion', result)
        self.assertIn('datos_ingredientes', result)


        print("Prueba preparar receta : OK")

    def test_preparar_receta_numero_personas_vacio(self):
        '''Prueba preparar receta'''
        recetas = self.session.query(Receta).all()
        recetas_ordenadas = sorted(recetas, key=lambda receta: receta.nombre)
        rango=len(recetas_ordenadas)-1
        if rango<0:
            rango=0

        indice = random.randint(0, rango)
        id_receta = recetas_ordenadas[indice].id
        resultado=None
    
        try:
         resultado=self.Recetario.dar_preparacion(id_receta, "")
        except Exception:
            self.assertEqual(resultado, "Error al preparar receta") 

    def test_preparar_receta_cantidad_mayor_pb(self):
        '''Prueba preparar receta con cantidad personas mayor cantidad personas base'''
        recetas = self.session.query(Receta).all()
        recetas_ordenadas = sorted(recetas, key=lambda receta: receta.nombre)
        rango=len(recetas_ordenadas)-1
        if rango<0:
            rango=0

        indice = random.randint(0, rango)
        receta = recetas_ordenadas[indice]
        id_receta = recetas_ordenadas[indice].id
        personas_receta = recetas_ordenadas[indice].personas

        # Verificar si hay más de una persona en la receta antes de generar el número aleatorio
        if personas_receta > 1:
            # Generar un número aleatorio entre 1 y personas_receta - 1
            num_personas = random.randint(personas_receta + 1, personas_receta + 10)
        else:
            # Si solo hay una persona, establecer num_personas en 1
            num_personas = 1

        
        result = self.Recetario.dar_preparacion(id_receta, num_personas)

        # Comprobar que el resultado es un diccionario con las propiedades esperadas
        self.assertIsInstance(result, dict)
        self.assertIn('receta', result)
        self.assertIn('personas', result)
        self.assertIn('calorias', result)
        self.assertIn('costo', result)
        self.assertIn('tiempo_preparacion', result)
        self.assertIn('datos_ingredientes', result)

        print("Prueba preparar receta con cantidad personas mayor cantidad personas base: OK")

    #pruebas unitarias eliminar receta
    #eliminar receta
    def test_la_receta_se_elimina_muestra_mensaje_confirmadolo(self):

        #se consultan las recetas
        recetas_tabla = self.session.query(Receta).all()
        cantidad_recetas=len(recetas_tabla)

        receta = recetas_tabla[0]

        mensaje = self.Recetario.eliminar_receta(receta.id)

        cantidad_recetas_posterior=len(self.Recetario.dar_recetas())

        # verificar que se haya eliminado la receta 
        self.assertEqual(mensaje, "La receta ha sido eliminada.")
        self.assertNotEqual(cantidad_recetas,cantidad_recetas_posterior)

        print("Prueba eliminar receta: OK")   
    #eliminar receta error
    def test_la_receta_se_elimina_error_id_vacio(self):
        mensaje = self.Recetario.eliminar_receta("")
        self.assertEqual(mensaje, "Error al eliminar la receta, intente nuevamente")
        print("Prueba error al eliminar receta: OK")   
   
    #pruebas unitarias editar receta
    def test_la_receta_se_edita_muestra_mensaje_confirmadolo(self):

        #se consultan las recetas
        recetas_tabla = self.session.query(Receta).all()
        
        receta = recetas_tabla[0]

        mensaje = self.Recetario.editar_receta(receta.id, receta.nombre,
                                               str(receta.tiempo), receta.personas,
                                               receta.calorias,
                                               receta.preparacion)
        self.assertEqual(mensaje, "La receta ha sido actualizada exitósamente.")
        print("Prueba editar receta: OK")
    #editar receta error
    def test_la_receta_se_edita_error_id_vacio(self):
        #se consultan las recetas
        recetas_tabla = self.session.query(Receta).all()
        
        receta = recetas_tabla[0]
        mensaje = self.Recetario.editar_receta("", receta.nombre,
                                               str(receta.tiempo), receta.personas,
                                               receta.calorias,
                                               receta.preparacion)
        self.assertEqual(mensaje, "Error al editar la receta, intente nuevamente")
        print("Prueba error al editar receta: OK")   

    #pruebas unitarias editar ingrediente
    def test_el_ingrediente_se_edita_muestra_mensaje_confirmadolo(self):

        #se consultan los ingredientes
        ingredientes = self.session.query(Ingrediente).all()
        
        ingrediente = ingredientes[0]

        mensaje = self.Recetario.editar_ingrediente(ingrediente.id, ingrediente.nombre,
                                               ingrediente.unidad, str(ingrediente.valor),
                                               ingrediente.sitioCompra)
        self.assertEqual(mensaje, "El ingrediente ha sido actualizado exitósamente.")
        print("Prueba editar ingrediente: OK")    

        
