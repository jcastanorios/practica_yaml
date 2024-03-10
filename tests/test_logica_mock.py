import unittest

from src.logica.LogicaMock import LogicaMock

class LogicaMockTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = LogicaMock()
        
    def tearDown(self):
        self.logica = None
        
    def test_dar_receta(self):
        receta = self.logica.recetas[0]
        self.assertEqual(receta["nombre"], "Ajiaco")


