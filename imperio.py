from enum import Enum
from abc import ABCMeta, abstractmethod

# Excepciones posibles de nuestro programa

class StockInsuficienteError(Exception):
    # Excepción lanzada cuando no hay suficiente stock de un repuesto
    pass

class RepuestoNoEncontradoError(Exception):
    # Excepción lanzada cuando no se encuentra un repuesto en el almacén
    pass

class ExistenciaError(Exception):
	# Excepción lanzada cuando se va a añadir un repuesto en un almacén en el que ya está
	pass

class Repuesto:

	def __init__(self, nombre, proveedor, cantidad, precio):
		self.nombre = nombre
		self.proveedor = proveedor
		self.__cantidad = cantidad
		self.precio = precio
	
	# con este método obtenemos la cantidad actual que hay disponible de cada repuesto
	def get_cantidad(self):
		return self.__cantidad
	
	# cuando se necesite cierta cantidad de un repuesto usaremos este método para modificarla
	def modificar_cantidad(self, variacion):
		if self.__cantidad + variacion < 0: # si se coge más cantidad de la que hay realmente
			raise StockInsuficienteError(f"No hay suficiente stock para {self.nombre}.") # lanzamos una excepción
		self.__cantidad += variacion # si todo va bien modificamos la cantidad del repuesto
	
	def obtenerDatos(self):
		return "Nombre de la pieza: "+str(self.nombre)+"\nProveedor: "+str(self.proveedor)+"\nCantidad: "+str(self.__cantidad)+"\nPrecio: "+str(self.precio)

class Almacen:

	def __init__(self, nombre, localizacion):
		self.catalogo_piezas = []
		self.nombre = nombre
		self.localizacion = localizacion

	# usaremos este método para añadir piezas al catálogo del almacén
	def añadir_pieza(self,pieza): # añadiremos clases Pieza()
		for p in self.catalogo_piezas:
			if p.nombre == pieza.nombre: # si ya está en el catálogo esa pieza/repuesto
				raise ExistenciaError(f"Ya se encuentra disponible el repuesto {pieza.nombre} en este almacén") # lanzamos una excepción
		self.catalogo_piezas.append(pieza) # en otro caso añadimos la pieza al catálogo
	
	# usaremos este método para saber si una pieza concreta se encuentra disponible en un almacén concreto
	def buscar_pieza(self, nombre):
		for pieza in self.catalogo_piezas:
			if pieza.nombre == nombre:
				return pieza
		raise RepuestoNoEncontradoError(f"La pieza {nombre} no está disponible en este almacén") # si no se encuentra lanzamos una excepción
	
	# usaremos este método para adquirir una pieza del catálogo de cierta cantidad
	def adquirir_pieza(self, nombre, cantidad):
		pieza_encontrada = self.buscar_pieza(nombre) # buscamos la pieza en el catálogo
		pieza_encontrada.modificar_cantidad(-cantidad) # modificamos la cantidad con la que vamos a coger
		print(f"Se ha adquirido una cantidad de {cantidad} piezas de {nombre}")
	
	def obtenerDatos(self):
		return "Nombre: "+str(self.nombre)+"\nLocalización: "+str(self.localizacion)+"\nCatálogo de piezas: "+str(self.catalogo_piezas)
