from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base


class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    unidad = Column(String)
    valor = Column(Integer)
    sitioCompra = Column(String)
    recetas = relationship('Receta', secondary='receta_ingrediente')

class RecetaIngrediente(Base):
    __tablename__='receta_ingrediente'

    ingrediente_id = Column(
        Integer,
        ForeignKey('ingrediente.id'),
        primary_key=True)
    
    receta_id = Column(
        Integer,
        ForeignKey('receta.id'),
        primary_key=True)
    
    cantidad = Column(Integer)