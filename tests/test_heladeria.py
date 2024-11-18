import pytest
from models.base import Base
from models.complemento import Complemento
from models.copa import Copa
from models.malteada import Malteada
from models.heladeria import Heladeria


@pytest.fixture
def heladeria():
    """
    Configuración inicial para las pruebas: una heladería con algunos ingredientes y productos.
    """
    heladeria = Heladeria()

    # Ingredientes base
    heladeria.agregar_ingrediente(Base("Helado de Vainilla", 1000, 150, 10, True, "Vainilla"))
    heladeria.agregar_ingrediente(Base("Helado de Chocolate", 1200, 200, 5, True, "Chocolate"))

    # Complementos
    heladeria.agregar_ingrediente(Complemento("Chispas de Chocolate", 500, 50, 8, True))
    heladeria.agregar_ingrediente(Complemento("Crema Chantilly", 300, 120, 12, True))

    # Productos
    heladeria.agregar_producto(
        Copa("Copa Vainilla", 5000, "Cristal", [heladeria.ingredientes[0], heladeria.ingredientes[2]])
    )
    heladeria.agregar_producto(
        Malteada("Malteada Chocolate", 6000, 500, [heladeria.ingredientes[1], heladeria.ingredientes[3]])
    )

    return heladeria


def test_es_sano():
    """
    Prueba si un ingrediente es sano.
    """
    ingrediente = Base("Helado de Fresa", 900, 100, 15, True, "Fresa")
    assert ingrediente.es_vegetariano is True

    ingrediente_no_sano = Complemento("Jarabe de Chocolate", 300, 300, 10, False)
    assert ingrediente_no_sano.es_vegetariano is False


def test_abastecer_ingrediente(heladeria):
    """
    Prueba el abastecimiento de un ingrediente.
    """
    ingrediente = heladeria.ingredientes[0]
    cantidad_inicial = ingrediente.inventario

    ingrediente.abastecer(5)
    assert ingrediente.inventario == cantidad_inicial + 5


def test_renovar_inventario(heladeria):
    """
    Prueba la renovación del inventario para los complementos.
    """
    complemento = heladeria.ingredientes[2]
    complemento.renovar_inventario()
    assert complemento.inventario == 0  # Verificar si la cantidad se reinició


def test_calcular_calorias(heladeria):
    """
    Prueba el cálculo de las calorías para copas y malteadas.
    """
    copa = heladeria.productos_disponibles[0]
    assert copa.calcular_calorias() == 190  # Ajusta según los valores reales de calorías

    malteada = heladeria.productos_disponibles[1]
    assert malteada.calcular_calorias() == 520  # Ajusta según los valores reales de calorías



def test_calcular_costo_produccion(heladeria):
    """
    Prueba el cálculo del costo de producción de un producto.
    """
    copa = heladeria.productos_disponibles[0]
    assert copa.calcular_costo_produccion() == 1500  # Ajusta según los costos reales

    malteada = heladeria.productos_disponibles[1]
    assert malteada.calcular_costo_produccion() == 2000  # Ajusta según los costos reales



def test_calcular_rentabilidad(heladeria):
    """
    Prueba el cálculo de la rentabilidad de un producto.
    """
    copa = heladeria.productos_disponibles[0]
    assert copa.calcular_rentabilidad() == 3500  # Ajusta según la fórmula correcta

    malteada = heladeria.productos_disponibles[1]
    assert malteada.calcular_rentabilidad() == 4000  # Ajusta según la fórmula correcta



def test_encontrar_producto_mas_rentable(heladeria):
    """
    Prueba para encontrar el producto más rentable.
    """
    producto_rentable = heladeria.encontrar_producto_mas_rentable()
    assert producto_rentable.get_nombre() == "Malteada Chocolate"  # Producto con mayor rentabilidad


def test_vender_producto(heladeria):
    """
    Prueba la venta de un producto.
    """
    producto = heladeria.productos_disponibles[0]
    cantidad_inicial = [ingrediente.inventario for ingrediente in producto.ingredientes]

    vendido = heladeria.vender_producto(producto.get_nombre())
    assert vendido is True

    # Verificar que el inventario de los ingredientes disminuyó
    for i, ingrediente in enumerate(producto.ingredientes):
        assert ingrediente.inventario == cantidad_inicial[i] - (0.2 if isinstance(ingrediente, Base) else 1)

    # Intentar vender cuando no hay inventario suficiente
    for ingrediente in producto.ingredientes:
        ingrediente.inventario = 0  # Dejar sin inventario

    vendido = heladeria.vender_producto(producto.get_nombre())
    assert vendido is False
