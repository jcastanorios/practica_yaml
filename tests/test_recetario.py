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