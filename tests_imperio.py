import pytest
from imperio import Repuesto, Almacen, StockInsuficienteError, ExistenciaError

# test 1. comprobamos que las cantidades se sumen correctamente
def test_modificar_cantidad():
    pieza = Repuesto("Motor", "Kuat", 10, 500.0)
    pieza.modificar_cantidad(5)
    
    assert pieza.get_cantidad() == 15
    
    pieza.modificar_cantidad(-3)
    assert pieza.get_cantidad() == 12

# test 2. comprobamos que salta la excepción al quedarse sin stock
def test_stock_insuficiente():
    pieza = Repuesto("Laser", "Armería", 5, 200.0)
    
    with pytest.raises(StockInsuficienteError):
        pieza.modificar_cantidad(-10)

# test 3. comprobamos que se añade y se busca correctamente en el almacén
def test_añadir_y_buscar_pieza():
    almacen = Almacen("Almacén A", "Endor")
    pieza = Repuesto("Escudo", "Corellia", 20, 1000.0)
    
    almacen.añadir_pieza(pieza)
    pieza_encontrada = almacen.buscar_pieza("Escudo")
    
    assert pieza_encontrada.nombre == "Escudo"
    assert pieza_encontrada.get_cantidad() == 20

# test 4. comprobamos que salta la excepción al añadir una pieza repetida
def test_pieza_duplicada_almacen():
    almacen = Almacen("Almacén B", "Hoth")
    pieza = Repuesto("Antena", "Kuat", 5, 100.0)
    
    almacen.añadir_pieza(pieza)
    
    with pytest.raises(ExistenciaError):
        almacen.añadir_pieza(pieza)