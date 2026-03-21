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

# clase que representa una pieza de repuesto individual y controla su nivel de stock disponible
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

# clase que gestiona un catálogo de repuestos almacenados en un almacén concreto
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
        # convertimos la lista de objetos Repuesto a una lista de nombres para que se imprima de forma legible
        nombres_piezas = [p.nombre for p in self.catalogo_piezas]
        return "Nombre: "+str(self.nombre)+"\nLocalización: "+str(self.localizacion)+"\nCatálogo de piezas: "+str(nombres_piezas)

# clase abstracta base para todas las unidades de combate, no se puede instanciar directamente
class UnidadCombate(metaclass=ABCMeta):
    def __init__(self, id_combate, clave_cifrada):
        self.id_combate = id_combate
        self.clave_cifrada = clave_cifrada
    
    # método abstracto
    @abstractmethod
    def obtenerDatos(self):
        return "Identificador de combate: "+str(self.id_combate)+"\nClave cifrada: "+str(self.clave_cifrada)

# clase que hereda de UnidadCombate, representa una nave genérica
class Nave(UnidadCombate):
    def __init__(self, id_combate, clave_cifrada, nombre, catalogo_piezas):
        super().__init__(id_combate, clave_cifrada)
        self.nombre = nombre
        self.catalogo_piezas = catalogo_piezas
    
    def añadir_piezas_catalogo(self, repuesto):
        for pieza in self.catalogo_piezas:
            if pieza.nombre == repuesto.nombre:
                raise ExistenciaError(f"Ya se encuentra disponible la pieza {repuesto.nombre} en el catálogo de esta nave")
        self.catalogo_piezas.append(repuesto)
    
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
        self.ubicacion = ubicacion # debe ser un tipo Ubicacion (Enum)
    
    def obtenerDatos(self):
        return super().obtenerDatos()+"\nTripulación: "+str(self.tripulacion)+"\nPasaje: "+str(self.pasaje)+"\nUbicación: "+str(self.ubicacion.name)

# enumeracion para limitar los tipos de clase de las naves
class Clase(Enum):
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3

# clase que hereda de Nave, representa una Nave Estelar
class NaveEstelar(Nave):
    def __init__(self, id_combate, clave_cifrada, nombre, catalogo_piezas, tripulacion, pasaje, clase):
        super().__init__(id_combate, clave_cifrada, nombre, catalogo_piezas)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase
    
    def obtenerDatos(self):
        return super().obtenerDatos()+"\nTripulación: "+str(self.tripulacion)+"\nPasaje: "+str(self.pasaje)+"\nClase: "+str(self.clase.name)

# clase que hereda de Nave, representa un Caza Estelar
class CazaEstelar(Nave):
    def __init__(self, id_combate, clave_cifrada, nombre, catalogo_piezas, dotacion):
        super().__init__(id_combate, clave_cifrada, nombre, catalogo_piezas)
        self.dotacion = dotacion
    
    def obtenerDatos(self):
        return super().obtenerDatos()+"\nDotación: "+str(self.dotacion)

# clase principal que actúa como sistema para gestionar flotas y almacenes
class Imperio:
    def __init__(self):
        self.flota = []
        self.almacenes = []
    
    # usamos este método para añadir una nave a la flota, validando que su id de combate no exista previamente
    def añadir_flota(self, nave):
        for n in self.flota:
            if n.id_combate == nave.id_combate:
                raise ExistenciaError(f"La nave {nave.nombre} con id de combate {nave.id_combate} ya se encuentra disponible en la flota")
        self.flota.append(nave)
	
    # método para crear un nuevo almacén, validando que no haya otro con el mismo nombre
    def añadir_almacen(self, almacen):
        for a in self.almacenes:
            if a.nombre == almacen.nombre:
                raise ExistenciaError(f"El almacén {almacen.nombre} ya existe")
        self.almacenes.append(almacen)
    
    # método que devuelve una cadena de texto con toda la información de la flota
    def listar_flota(self):
        cadena = "FLOTA IMPERIAL \n"
        for f in self.flota:
            cadena += f.obtenerDatos() +"\n"
        return cadena  

    # método que devuelve una cadena de texto con toda la información de los almacenes
    def listar_almacenes(self):
        cadena = "ALMACENES IMPERIALES \n"
        for a in self.almacenes:
            cadena += a.obtenerDatos() +"\n"
        return cadena

if __name__ == "__main__":
    print("\nSistema de gestión del Imperio Galáctico\n")
    sistema_imperio = Imperio()

    # creamos e insertamos repuestos en un almacén
    repuesto_motor = Repuesto("Motor básico", "Industrias Espaciales", 7, 50000.0)
    repuesto_laser = Repuesto("Cañón láser", "Armería Imperial", 50, 2000.0)
    
    almacen_principal = Almacen("Almacén Central", "Sector 4")
    almacen_principal.añadir_pieza(repuesto_motor)
    almacen_principal.añadir_pieza(repuesto_laser)
    
    sistema_imperio.añadir_almacen(almacen_principal)

    # creamos diferentes tipos de naves
    estacion_muerte = EstacionEspacial("ID-001", 1111, "Estrella de la Muerte", ["Panel de control", "Batería principal"], 300000, 50000, Ubicacion.ENDOR)
    destructor = NaveEstelar("ID-002", 2222, "Destructor Alpha", ["Motor básico", "Generador de escudos"], 37000, 0, Clase.EJECUTOR)
    caza_tie = CazaEstelar("ID-003", 3333, "Caza TIE genérico", ["Cañón láser", "Cristal de cabina"], 1)

    # añadimos naves a la flota
    sistema_imperio.añadir_flota(estacion_muerte)
    sistema_imperio.añadir_flota(destructor)
    sistema_imperio.añadir_flota(caza_tie)

    # imprimimos los resultados para validar que funciona (polimorfismo en obtenerDatos)
    print(sistema_imperio.listar_almacenes())
    print(sistema_imperio.listar_flota())