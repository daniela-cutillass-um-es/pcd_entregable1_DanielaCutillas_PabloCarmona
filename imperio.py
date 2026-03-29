from enum import Enum
from abc import ABCMeta, abstractmethod

# Excepciones posibles de nuestro programa

class StockInsuficienteError(Exception):
    '''
    # Excepción lanzada cuando no hay suficiente stock de un repuesto
    '''
    pass

class RepuestoNoEncontradoError(Exception):
    '''Excepción lanzada cuando no se encuentra un repuesto en el almacén'''
    pass

class ExistenciaError(Exception):
	'''Excepción lanzada cuando se va a añadir un repuesto en un almacén en el que ya está'''
	pass

class Repuesto:
    '''
    Repuesto es una clase que representa una pieza de repuesto individual.
    Hemos implementado tres métodos:
        - get_cantidad(): nos permite saber la cantidad que hay de un repuesto concreto
        - modificar_cantidad(): lo usamos para mantener actualizado el método anterior
        - obtenerDatos(): imprimimos toda la información de la clase de forma legible
    '''    
    def __init__(self, nombre, proveedor, cantidad, precio):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad # atributo privado
        self.precio = precio
	
    def get_cantidad(self):
        '''
        Con este método obtenemos la cantidad actual que hay disponible de cada repuesto
        '''
        return self.__cantidad
	
    def modificar_cantidad(self, variacion):
        '''
        Con este método modificamos la cantidad que hay de un repuesto cuando se necesite coger
        '''
        if self.__cantidad + variacion < 0: # si se coge más cantidad de la que hay realmente
            raise StockInsuficienteError(f"No hay suficiente stock para {self.nombre}.") # lanzamos una excepción
        self.__cantidad += variacion # si todo va bien modificamos la cantidad del repuesto
	
    def obtenerDatos(self):
        return "Nombre de la pieza: "+str(self.nombre)+"\nProveedor: "+str(self.proveedor)+"\nCantidad: "+str(self.__cantidad)+"\nPrecio: "+str(self.precio)

class Almacen:
    '''
    Almacén es una clase que gestiona un catálogo de repuestos almacenados en un almacén concreto
    Hemos implementado cuatro métodos:
        - añadir_pieza(): lo usamos para ir añadiendo piezas al catálogo que es una lista
        - buscar_pieza(): verificar si se encuentra una pieza en el catálogo o no
        - adquirir_pieza(): lo usamos para actualizar las cantidades de la pieza de la que se ha adquirido una cantidad concreta
        - obtenerDatos(): imprimimos toda la información de la clase de forma legible
    '''

    def __init__(self, nombre, localizacion):
        self.catalogo_piezas = []
        self.nombre = nombre
        self.localizacion = localizacion

    def añadir_pieza(self,pieza):
        '''
        Con este método añadimos piezas al catálogo del almacén.
        Iremos añadiendo en el catálogo clases Repuesto().
        '''
        for p in self.catalogo_piezas:
            if p.nombre == pieza.nombre: # si ya está en el catálogo esa pieza/repuesto
                raise ExistenciaError(f"Ya se encuentra disponible el repuesto {pieza.nombre} en este almacén") # lanzamos una excepción
        self.catalogo_piezas.append(pieza) # en otro caso añadimos la pieza al catálogo
    
    def buscar_pieza(self, nombre):
        '''
        Con este método podremos verificar si una pieza se encuentra en el catálogo o aún no ha sido añadida.
        '''
        for pieza in self.catalogo_piezas:
            if pieza.nombre == nombre: # buscamos las piezas por su nombre y si se encuentra
                return pieza # devolvemos la clase para ver toda su información
        raise RepuestoNoEncontradoError(f"La pieza {nombre} no está disponible en este almacén") # si no se encuentra lanzamos una excepción
    
    def adquirir_pieza(self, nombre, cantidad):
        '''
        Este método se usa cuando el comandante necesita adquirir una cierta cantidad de una pieza
        '''
        pieza_encontrada = self.buscar_pieza(nombre) # buscamos la pieza en el catálogo
        pieza_encontrada.modificar_cantidad(-cantidad) # modificamos la cantidad con la que hemos indicado
        print(f"Se ha adquirido una cantidad de {cantidad} piezas del repuesto {nombre}")
    
    def obtenerDatos(self):
        nombres_piezas = [p.nombre for p in self.catalogo_piezas]
        return "Nombre: "+str(self.nombre)+"\nLocalización: "+str(self.localizacion)+"\nCatálogo de piezas: "+str(nombres_piezas)

class UnidadCombate(metaclass=ABCMeta):
    '''
    UnidadCombate es una clase abstracta base para todas las unidades de combate, no se puede instanciar directamente
    Hemos implementado un método:
        - obtenerDatos(): imprimimos toda la información de la clase de forma legible
    '''
    def __init__(self, id_combate, clave_cifrada):
        self.id_combate = id_combate
        self.clave_cifrada = clave_cifrada
    
    # método abstracto
    @abstractmethod
    def obtenerDatos(self):
        return "Identificador de combate: "+str(self.id_combate)+"\nClave cifrada: "+str(self.clave_cifrada)

# clase que hereda de UnidadCombate, representa una nave genérica
class Nave(UnidadCombate):
    '''
    Nave es una clase que hereda de UnidadCombate, representa una nave genérica.
    Esta clase a su vez es una superclase intermedia, ya que centraliza la gestión de el catálogo de piezas de las naves.
    Hemos implementado dos métodos:
        - añadir_piezas_catalogo(): lo usamos para ir añadiendo piezas al catálogo de una nave ya que es una lista
        - obtenerDatos(): imprimimos toda la información de la clase de forma legible
    '''
    def __init__(self, id_combate, clave_cifrada, nombre, catalogo_piezas):
        super().__init__(id_combate, clave_cifrada)
        self.nombre = nombre
        self.catalogo_piezas = catalogo_piezas
    
    def añadir_piezas_catalogo(self, repuesto):
        '''
        Con este método añadimos piezas al catálogo de una nave concreta.
        Añadimos clases Repuesto().
        '''
        for pieza in self.catalogo_piezas:
            if pieza.nombre == repuesto.nombre:
                raise ExistenciaError(f"Ya se encuentra disponible la pieza {repuesto.nombre} en el catálogo de esta nave")
        self.catalogo_piezas.append(repuesto)
    
    def obtenerDatos(self):
        return super().obtenerDatos() + "\nNombre: " + str(self.nombre) + "\nCatálogo: " + str(self.catalogo_piezas)

# enumeración
class Ubicacion(Enum):
    ENDOR = 1
    CUMULO_RAIMOS = 2
    NEBULOSA_KALIIDA = 3

class EstacionEspacial(Nave):
    '''
    EstacionEspacial es una clase que hereda de la clase Nave, pero con ciertos atributos concretos para ésta como la tripulación que hay en ella, el pasaje o la ubicación
    Hemos implementado un método para esta clase:
        - obtenerDatos(): imprimimos toda la información de la clase de forma legible
    '''
    def __init__(self, id_combate, clave_cifrada, nombre, catalogo_piezas, tripulacion, pasaje, ubicacion):
        super().__init__(id_combate, clave_cifrada, nombre, catalogo_piezas)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion # debe ser un tipo Ubicacion (Enum)
    
    def obtenerDatos(self):
        return super().obtenerDatos()+"\nTripulación: "+str(self.tripulacion)+"\nPasaje: "+str(self.pasaje)+"\nUbicación: "+str(self.ubicacion.name)

# enumeracion
class Clase(Enum):
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3

class NaveEstelar(Nave):
    '''
    NaveEstelar es una clase que hereda de la clase Nave, pero con ciertos atributos concretos para ésta como la tripulación, el pasaje o la clase
    Hemos implementado un método para esta clase:
        - obtenerDatos(): imprimimos toda la información de la clase de forma legible
    '''
    def __init__(self, id_combate, clave_cifrada, nombre, catalogo_piezas, tripulacion, pasaje, clase):
        super().__init__(id_combate, clave_cifrada, nombre, catalogo_piezas)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase
    
    def obtenerDatos(self):
        return super().obtenerDatos()+"\nTripulación: "+str(self.tripulacion)+"\nPasaje: "+str(self.pasaje)+"\nClase: "+str(self.clase.name)

class CazaEstelar(Nave):
    '''
    CazaEstelar es una clase que hereda de la clase Nave, pero con un atributo concreto para ésta, dotación
    Hemos implementado un método para esta clase:
        - obtenerDatos(): imprimimos toda la información de la clase de forma legible
    '''
    def __init__(self, id_combate, clave_cifrada, nombre, catalogo_piezas, dotacion):
        super().__init__(id_combate, clave_cifrada, nombre, catalogo_piezas)
        self.dotacion = dotacion
    
    def obtenerDatos(self):
        return super().obtenerDatos()+"\nDotación: "+str(self.dotacion)

class Imperio:
    '''
    Imperio es la clase principal, que actúa como sistema para gestionar las flotas y los almacenes
    Hemos implementado cuatro métodos:
        - añadir_flota(): lo usamos para añadir una nueva nave a la flota del imperio
        - añadir_almacen(): lo usamos para añadir un nuevo almacen al imperio
        - listar_flota(): lo usamos para saber cuáles son las naves y la información sobre ellas
        - listar_almacenes(): lo usamos para saber cuáles son los almacenes y la información sobre ellos
    '''
    def __init__(self):
        self.flota = []
        self.almacenes = []
    
    def añadir_flota(self, nave):
        '''
        Este método va añadiendo una nave a la flota del imperio, validando que su id de combate no exista previamente
        '''
        for n in self.flota:
            if n.id_combate == nave.id_combate:
                raise ExistenciaError(f"La nave {nave.nombre} con id de combate {nave.id_combate} ya se encuentra disponible en la flota")
        self.flota.append(nave)
	
    def añadir_almacen(self, almacen):
        '''
        Este método crea un nuevo almacén del imperio, validando que no hay otro con el mismo nombre
        '''
        for a in self.almacenes:
            if a.nombre == almacen.nombre:
                raise ExistenciaError(f"El almacén {almacen.nombre} ya existe")
        self.almacenes.append(almacen)
    
    def listar_flota(self):
        '''
        Este método devuelve una cadena de texto con toda la información de la flota del imperio
        '''
        cadena = "FLOTA IMPERIAL \n"
        for f in self.flota:
            cadena += f.obtenerDatos() +"\n"
        return cadena  

    def listar_almacenes(self):
        '''
        Este método devuelve una cadena de texto con toda la información de los almacenes del imperio
        '''
        cadena = "ALMACENES IMPERIALES \n"
        for a in self.almacenes:
            cadena += a.obtenerDatos() +"\n"
        return cadena

if __name__ == "__main__":
    print("SISTEMA DE GESTIÓN DEL IMPERIO GALÁCTICO")
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

    # --- PRUEBAS DE GESTIÓN DE EXCEPCIONES (Requisito de la práctica) ---
    print("PRUEBAS DE GESTIÓN DE EXCEPCIONES")

    # Con try..except capturamos la excepción que debería de saltar e imprimimos el mensaje explicativo
    # del error, pero el programa continúa su ejecución normal, de esta forma no se detiene

    # Intento añadir una pieza que ya existe en el almacén
    print("Prueba 1: Añadimos una pieza duplicada al almacén principal")
    try:
        pieza_repetida = Repuesto("Motor básico", "Otro Proveedor", 1, 10.0)
        almacen_principal.añadir_pieza(pieza_repetida)
    except ExistenciaError as e:
        print(f"Excepción esperada: {e}\n")

    # Intento adquirir más piezas de las que hay en stock
    print("Prueba 2: Adquirir piezas sin stock suficiente")
    try:
        # El motor básico tiene 7 unidades, intentamos pedir 20
        almacen_principal.adquirir_pieza("Motor básico", 20)
    except StockInsuficienteError as e:
        print(f"Excepción esperada: {e}\n")

    # Intento buscar una pieza que no existe en el catálogo del almacén
    print("Prueba 3: Buscar una pieza inexistente en el almacén")
    try:
        almacen_principal.buscar_pieza("Hiperimpulsor Halcón")
    except RepuestoNoEncontradoError as e:
        print(f"Excepción esperada: {e}\n")

    # Intento añadir una nave con un ID que ya está en la flota
    print("Prueba 4: Añadir nave con ID existente")
    try:
        nave_clon = CazaEstelar("ID-001", 9999, "Caza Clonado", [], 1) # ID-001 ya la tiene la Estrella de la Muerte
        sistema_imperio.añadir_flota(nave_clon)
    except ExistenciaError as e:
        print(f"Excepción esperada: {e}\n")