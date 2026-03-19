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

class UnidadCombate(metaclass=ABCMeta):
    def __init__(self, id_combate, clave_cifrada):
        self.id_combate = id_combate
        self.clave_cifrada = clave_cifrada
    
    @abstractmethod
    def obtenerDatos(self):
        return "Identificador de combate: "+str(self.id_combate)+"\nClave cifrada: "+str(self.clave_cifrada)

class Nave(UnidadCombate):
    def __init__(self, id_combate, clave_cifrada, nombre, catalogo_piezas):
        super().__init__(id_combate, clave_cifrada)
        self.nombre = nombre
        self.catalogo_piezas = catalogo_piezas # Lista de nombres de piezas según el diagrama/enunciado
    
    def añadir_piezas_catalogo(self, nombre_repuesto):
        if nombre_repuesto in self.catalogo_piezas:
            print("Esta pieza ya se encuentra en el catálogo")
            return
        self.catalogo_piezas.append(nombre_repuesto)
    
    def obtenerDatos(self):
        return super().obtenerDatos() + "\nNombre: " + str(self.nombre) + "\nCatálogo: " + str(self.catalogo_piezas)

class Ubicacion(Enum):
    ENDOR = 1
    CUMULO_RAIMOS = 2
    NEBULOSA_KALIIDA = 3

class EstacionEspacial(Nave):
    def __init__(self, id_combate, clave_cifrada, nombre, catalogo_piezas, tripulacion, pasaje, ubicacion):
        super().__init__(id_combate, clave_cifrada, nombre, catalogo_piezas)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion
    
    def obtenerDatos(self):
        return super().obtenerDatos()+"\nTripulación: "+str(self.tripulacion)+"\nPasaje: "+str(self.pasaje)+"\nUbicación: "+str(self.ubicacion.name)

class Clase(Enum):
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3

class NaveEstelar(Nave):
    def __init__(self, id_combate, clave_cifrada, nombre, catalogo_piezas, tripulacion, pasaje, clase):
        super().__init__(id_combate, clave_cifrada, nombre, catalogo_piezas)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase
    
    def obtenerDatos(self):
        return super().obtenerDatos()+"\nTripulación: "+str(self.tripulacion)+"\nPasaje: "+str(self.pasaje)+"\nClase: "+str(self.clase.name)

class CazaEstelar(Nave):
    def __init__(self, id_combate, clave_cifrada, nombre, catalogo_piezas, dotacion):
        super().__init__(id_combate, clave_cifrada, nombre, catalogo_piezas)
        self.dotacion = dotacion
    
    def obtenerDatos(self):
        return super().obtenerDatos()+"\nDotación: "+str(self.dotacion)

class Imperio:
    def __init__(self):
        self.flota = []
        self.almacenes = []
    
    def añadir_flota(self, nave):
        for n in self.flota:
            if n.id_combate == nave.id_combate:
                print("Ya se encuentra disponible en la flota")
        self.flota.append(nave)
	
    def añadir_almacen(self, almacen):
        for a in self.almacenes:
            if a.nombre == almacen.nombre:
                print("Ya existe este almacén")
        self.almacenes.append(almacen)
    
    def listar_flota(self):
        cadena = ""
        for f in self.flota:
            cadena = cadena+str(f)+"\n"

    def listar_almacenes(self):
        cadena = ""
        for a in self.almacenes:
            cadena = cadena+str(a)+"\n"