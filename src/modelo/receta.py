from sqlalchemy import Column, Integer, String, Time, Float
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Receta(Base):
    __tablename__ = 'receta'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tiempo = Column(Time)
    personas = Column(Integer)
    calorias = Column(Integer)
    preparacion = Column(String)
    ingredientes = relationship('Ingrediente', secondary='receta_ingrediente', back_populates='recetas')
    

