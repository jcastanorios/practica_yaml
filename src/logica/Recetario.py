'''
Clase Recetario
'''
import datetime
import locale
from sqlite3 import IntegrityError
from src.logica.FachadaRecetario import FachadaRecetario
from src.modelo.declarative_base import engine, Base, session
from src.modelo.receta import Receta
from src.modelo.ingrediente import Ingrediente, RecetaIngrediente
from datetime import datetime, timedelta

class Recetario(FachadaRecetario):


    def __init__(self):
        Base.metadata.create_all(engine) 

    def dar_recetas(self):
        recetas = session.query(Receta).all()
        recetas_ordenadas = sorted(recetas, key=lambda receta: receta.nombre)

        # Lista para almacenar los resultados
        lista_recetas = []

        # Iterar sobre las recetas y agregar los valores a la lista
        for receta in recetas_ordenadas:
            dict_receta = {
                'nombre': receta.nombre,
                'tiempo': str(receta.tiempo),
                'personas': str(receta.personas),
                'calorias': str(receta.calorias),
                'preparacion': receta.preparacion}
            lista_recetas.append(dict_receta)
            
        # Cerrar la sesión y devolver la lista de recetas
        session.close()
        return lista_recetas
    
    def dar_receta(self, id_receta):
        recetas_ordenadas = session.query(Receta).order_by(Receta.nombre).all()
        posicion = id_receta

        if 0 <= posicion < len(recetas_ordenadas):
            receta_seleccionada = recetas_ordenadas[posicion]
            
            dict_receta = {
                'id':     receta_seleccionada.id,
                'nombre': receta_seleccionada.nombre,
                'tiempo': str(receta_seleccionada.tiempo),
                'personas': str(receta_seleccionada.personas),
                'calorias': str(receta_seleccionada.calorias),
                'preparacion': receta_seleccionada.preparacion
            }
            
            return dict_receta
        else:
            return None
    
    def validar_crear_editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):
        if not receta:
            return "El campo receta no debe estar vacío"
        elif not calorias:
            return "El campo \"Calorías por porción\" no debe estar vacío"
        
        elif not preparacion:
            return "El campo \"Preparación\" no debe estar vacío."
        
        try:
            if not tiempo:
                raise ValueError
            datetime.strptime(tiempo, '%H:%M:%S').time()
        except ValueError:
            return "El campo Tiempo de preparación (horas) no debe estar vacío y debe tener el formato HH:MM:SS"
        
        
        try:
            comensales = int(personas)
            if comensales < 0:
                return "El número de comensales de la receta no puede ser negativo"     
        except ValueError:
            return "El número de comensales de la receta debe ser un número entero"
        
        try:
            calorias = int(calorias)
            if calorias < 0:
                return "El valor de las calorias de la receta debe ser un número entero positivo"     
        except ValueError:
            return "El valor de las calorias de la receta debe ser un número entero positivo"
        
         # Validar si ya existe una receta con el mismo nombre y es una receta nueva
        receta_existente = session.query(Receta).filter_by(nombre=receta.strip()).all()

        if (receta_existente and id_receta == -1) or (len(receta_existente)>1):
            return "Ya existe una receta con el nombre."
        return ""
    
    def crear_receta(self, receta, tiempo, personas, calorias, preparacion):
        nueva_receta = Receta(nombre=receta, 
                                   calorias=int(calorias), 
                                   preparacion=preparacion, 
                                   tiempo=datetime.strptime(tiempo, '%H:%M:%S').time(),
                                   personas=int(personas))
        session.add(nueva_receta)
        try:
            session.commit()
            return "La receta ha sido creada exitósamente."
        except IntegrityError as e:
            session.rollback()
            session.close()        
            return f"Error al crear la receta: {str(e)}, intente nuevamente"

    def editar_receta(self, id_receta, receta, tiempo, personas, calorias, preparacion):    
        try:
            receta_listada= self.dar_receta(id_receta)
            receta_encontrada = session.query(Receta).filter_by(id=receta_listada['id']).first()
            receta_encontrada.nombre=receta.strip()
            receta_encontrada.tiempo = tiempo=datetime.strptime(tiempo, '%H:%M:%S').time()
            receta_encontrada.persona = int(personas)
            receta_encontrada.calorias=int(calorias)
            receta_encontrada.preparacion=preparacion
            session.commit()
            return "La receta ha sido actualizada exitósamente."
        except Exception as e:
            session.rollback()
            session.close()        
            return f"Error al editar la receta, intente nuevamente"
       

    def eliminar_receta(self, id_receta):
        try:
            receta_listada= self.dar_receta(id_receta)
            receta_existente = session.query(Receta).filter_by(id=receta_listada['id']).first()
            relacion_receta = session.query(RecetaIngrediente).filter_by(receta_id=receta_listada['id']).first()
            if relacion_receta is not None:
                session.delete(relacion_receta)
            if receta_existente is not None:
                session.delete(receta_existente)
                session.commit()
                return "La receta ha sido eliminada."
        except Exception as e:
            session.rollback()
            session.close()        
            return f"Error al eliminar la receta, intente nuevamente"



    def dar_ingredientes(self):
        #Se establece configuración regional para el formato de miles
        locale.setlocale(locale.LC_ALL,'')

        ingredientes = session.query(Ingrediente).all()
        ingredientes_ordenados = sorted(ingredientes, key=lambda ingrediente: (ingrediente.nombre,ingrediente.unidad))
        lista_ingredientes = []
        for ingrediente in ingredientes_ordenados:
            valor_formato = locale.format_string("%d",ingrediente.valor,grouping=True)
            dict_ingrediente = {
                'id':ingrediente.id,
                'nombre': ingrediente.nombre,
                'unidad': ingrediente.unidad,
                'valor':  str(f"${valor_formato}"),
                'sitioCompra': ingrediente.sitioCompra}
            lista_ingredientes.append(dict_ingrediente)
        session.close()
        return lista_ingredientes
    
    def dar_ingrediente(self, id_ingrediente):
        return self.ingredientes[id_ingrediente].copy()

    def validar_crear_editar_ingrediente(self, id, nombre, unidad, valor, sitioCompra):

        if len(nombre) > 255:
            return "El nombre del ingrediente no puede superar los 255 caracteres."
        
        elif len(unidad)>255:
            return "La unidad de medida no puede superar los 255 caracteres."
        elif len(sitioCompra)>255:
            return "El sitio de compra no puede superar los 255 caracteres."
        
        #Valida que esten completos todos los campos
        if not nombre or not unidad or not valor or not sitioCompra:
            return "Todos los campos son obligatorios. Por favor, complete todos los campos."
        
        # Validar que el valor por unidad sea un número entero
        try:
            valor_entero = int(valor.replace("$",""))
            if valor_entero < 0:
                return "El valor del ingrediente no puede ser negativo"     
        except ValueError:
            return "El valor del ingrediente debe ser un número entero"
        
        receta_ingrediente = None
        ingrediente_existente = session.query(Ingrediente).filter_by(nombre=nombre.strip(), unidad=unidad).all()
        
        ingrediente_activo = self.dar_ingredientes()[id]

        if id == -1 and len(ingrediente_existente)==1:
            # Validar si ya existe un ingrediente nuevo con el mismo nombre y unidad de medida
            return "Ya existe un ingrediente con el nombre y la unidad de medida."
        elif len(ingrediente_existente)==1 and ingrediente_existente[0].id != ingrediente_activo['id']:
            return "Ya existe un ingrediente con el nombre y la unidad de medida."
        elif len(ingrediente_existente)>1:
            return "Ya existe un ingrediente con el nombre y la unidad de medida." 
        

        #Validar que sea una edición para determinar si existe en alguna receta o permitirle validar 
        #que se cambie el nombre siempre y cuando no exista en otro ingrediente
        if ingrediente_activo:
            receta_ingrediente = session.query(RecetaIngrediente).filter_by(ingrediente_id=ingrediente_activo['id']).first()
        
        if receta_ingrediente is not None:
            return "Este ingrediente ya existe en una receta."
        return ""
        
		
    def crear_ingrediente(self, nombre, unidad, valor, sitioCompras):
        nuevo_ingrediente = Ingrediente(nombre=nombre, unidad=unidad, valor=int(valor), sitioCompra=sitioCompras)
        session.add(nuevo_ingrediente)
        try:
            session.commit()
            return "El ingrediente ha sido creado exitosamente."
        except IntegrityError as e:
            session.rollback()
            return f"Error al crear el ingrediente: {str(e)}, intente nuevamente"
        
        session.close()    
 

    def editar_ingrediente(self, id_ingrediente, nombre, unidad, valor, sitioCompras):
        try:
            ingrediente_listado= self.dar_ingredientes()[id_ingrediente]
            ingrediente_encontrado = session.query(Ingrediente).filter_by(id=ingrediente_listado['id']).first()
            ingrediente_encontrado.nombre=nombre.strip()
            ingrediente_encontrado.unidad = unidad.strip()
            ingrediente_encontrado.valor = int(valor.replace(",","").replace("$","").replace(".",""))
            ingrediente_encontrado.sitioCompra=sitioCompras.strip()
            session.commit()
            return "El ingrediente ha sido actualizado exitósamente."
        except IntegrityError as e:
            session.rollback()
            session.close()        
            return f"Error al editar el ingrediente: {str(e)}, intente nuevamente"


    def eliminar_ingrediente(self, id_ingrediente):
        del self.ingredientes[id_ingrediente]

    def dar_ingredientes_receta(self, id_receta):
        recetaProv = self.dar_receta(id_receta)
        if recetaProv is None:
            return []
        
        receta = session.query(Receta).filter_by(
            nombre = str(recetaProv['nombre']),
            tiempo = datetime.strptime(recetaProv['tiempo'], '%H:%M:%S').time(),
            personas = int(recetaProv['personas']),
            calorias = int(recetaProv['calorias']),
            preparacion = recetaProv['preparacion']).first()

        if receta:
            ingredientes_receta = session.query(Ingrediente.nombre, Ingrediente.unidad, RecetaIngrediente.cantidad) \
                .join(RecetaIngrediente, Ingrediente.id == RecetaIngrediente.ingrediente_id) \
                .filter(RecetaIngrediente.receta_id == receta.id).all()

            if ingredientes_receta:
                lista_ingredientes = []
                for nombre, unidad, cantidad in ingredientes_receta:
                    ingrediente = {
                        "ingrediente": nombre,
                        "unidad": unidad,
                        "cantidad": cantidad
                    }
                    lista_ingredientes.append(ingrediente)
		        
                # Ordenar la lista de ingredientes por nombre y unidad
                lista_ordenada= sorted(lista_ingredientes, key=lambda lista: (lista["ingrediente"], lista["unidad"]))
                return lista_ordenada
            else:
                return []
        else:
            return []
    
    def agregar_ingrediente_receta(self, receta, ingrediente, cantidad):

        recetaSelec = session.query(Receta).filter_by(
            nombre = str(receta['nombre']),
            tiempo = datetime.strptime(receta['tiempo'], '%H:%M:%S').time(),
            personas = int(receta['personas']),
            calorias = int(receta['calorias']),
            preparacion = receta['preparacion']).first()

        valor_sin_simbolo = ingrediente['valor'].replace('$', '')  # Eliminar el símbolo '$'
        valor_sin_punto = valor_sin_simbolo.replace(',', '').replace(".","")
        ingredienteSelec = session.query(Ingrediente).filter_by(
            nombre = str(ingrediente['nombre']),
            unidad = str(ingrediente['unidad']),
            valor = int(valor_sin_punto),
            sitioCompra = str(ingrediente['sitioCompra'])).first()
        
        nuevo_ingrediente = RecetaIngrediente(
            ingrediente_id=ingredienteSelec.id,
            receta_id=recetaSelec.id,
            cantidad=cantidad
        )
        session.add(nuevo_ingrediente)
        try:
            session.commit()
            return "El ingrediente ha sido creado exitosamente."
        except IntegrityError as e:
            session.rollback()
            return f"Error al crear el ingrediente: {str(e)}, intente nuevamente"

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
        
        if not ingrediente or not cantidad:
            return "Los campos 'ingrediente' y 'cantidad' no pueden estar vacíos."

        # Verificar si la cantidad es un número entero y si es negativa
        try:
            valor_entero = int(cantidad)
            if valor_entero < 0:
                return "El valor del ingrediente no puede ser negativo"
        except ValueError:
            return "La cantidad debe ser un número entero."
        
        recetaSelec = session.query(Receta).filter_by(
            nombre = str(receta['nombre']),
            tiempo = datetime.strptime(receta['tiempo'], '%H:%M:%S').time(),
            personas = int(receta['personas']),
            calorias = int(receta['calorias']),
            preparacion = receta['preparacion']).first()

        valor_sin_simbolo = ingrediente['valor'].replace('$', '')  # Eliminar el símbolo '$'
        valor_sin_punto = valor_sin_simbolo.replace(',', '').replace(".","")  # Eliminar puntos
        ingredienteSelec = session.query(Ingrediente).filter_by(
            nombre = str(ingrediente['nombre']),
            unidad = str(ingrediente['unidad']),
            valor = int(valor_sin_punto),
            sitioCompra = str(ingrediente['sitioCompra'])).first()
        
        # Verificar si existe una relación en la tabla Receta_ingrediente
        relacion_existente = session.query(RecetaIngrediente).filter_by(
            receta_id=recetaSelec.id,
            ingrediente_id=ingredienteSelec.id,
        ).first()
        
        # Verificar si la cantidad es diferente a la almacenada en la tabla
        if relacion_existente is not None:
            return "El ingrediente ya se encuentra almacenado."
        return ""

    def dar_preparacion(self, id_receta,cantidad_personas):
        try:
            #Obtengo el id de la receta en la tabla Receta
            receta = self.dar_receta(id_receta)
            if receta is not None:
                #Se realiza el calculo de la preparación
                tiempoReceta = datetime.strptime(receta['tiempo'], '%H:%M:%S').time()
                TR = tiempoReceta.hour * 3600 + tiempoReceta.minute * 60 + tiempoReceta.second
                PB = int(receta['personas'])
            else:
                return {}
                
            if cantidad_personas <= PB:
                TPP = TR - ((PB-cantidad_personas)/(2*PB))*TR
            elif cantidad_personas > PB:
                TPP = (2 * TR)/3

            TP = str(timedelta(seconds=TPP)) #convierto de segundos al formato

            #Obtengo los ingredientes de la receta
            costoTotalReceta = 0
            datos_ingredientes = []  # Lista para almacenar los diccionarios de ingredientes
            lista_ingredientes = self.dar_ingredientes_receta(id_receta)
            for ingrediente in lista_ingredientes:
                ingredienteOriginal = session.query(Ingrediente).filter_by(
                    nombre=ingrediente['ingrediente'],
                    unidad=ingrediente['unidad']
                ).first()
                dict_ingrediente = {
                    'nombre': ingrediente['ingrediente'],
                    'unidad': ingrediente['unidad'],
                    'cantidad': str(ingrediente['cantidad']),
                    'valor': float(ingredienteOriginal.valor)
                }
                costoTotalReceta = ingredienteOriginal.valor + costoTotalReceta
                datos_ingredientes.append(dict_ingrediente)

            #Se retorna un diccionario con la información de la receta    
            dict_receta = {
                    'receta': receta['nombre'],
                    'personas': str(cantidad_personas),
                    'calorias': str(receta['calorias']),
                    'costo' : float(costoTotalReceta),
                    'tiempo_preparacion': str(TP),
                    'datos_ingredientes': datos_ingredientes,
                }
            return dict_receta
        except Exception:
            return "Error al preparar receta"