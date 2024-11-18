from models.base import Base
from models.complemento import Complemento
from models.copa import Copa
from models.malteada import Malteada


class Heladeria:
    def __init__(self):
        self.productos_disponibles = []  # Lista de productos (máximo 4)
        self.ingredientes = []  # Lista de todos los ingredientes disponibles
        self.ventas_dia = 0  # Contador de las ventas realizadas en el día

    def agregar_ingrediente(self, ingrediente):
        """
        Agrega un ingrediente a la lista de ingredientes disponibles.
        """
        self.ingredientes.append(ingrediente)

    def agregar_producto(self, producto):
        """
        Agrega un producto al catálogo de la heladería.
        Si ya hay 4 productos, no permite agregar más.
        """
        if len(self.productos_disponibles) < 4:
            self.productos_disponibles.append(producto)
        else:
            print("No se pueden agregar más productos. Límite alcanzado.")

    def encontrar_producto_mas_rentable(self):
        """
        Encuentra el producto más rentable entre los productos disponibles.
        """
        if not self.productos_disponibles:
            print("No hay productos disponibles.")
            return None
        return max(self.productos_disponibles, key=lambda p: p.calcular_rentabilidad())

    def vender_producto(self, nombre_producto):
        """
        Vende un producto si hay suficientes ingredientes.
        Actualiza el inventario y suma al contador de ventas del día.
        """
        producto = next((p for p in self.productos_disponibles if p.get_nombre() == nombre_producto), None)
        if not producto:
            print("Producto no encontrado.")
            return False

        # Verificar inventario
        try:
            if not self.verificar_ingredientes(producto):
                raise ValueError("No hay suficientes ingredientes para preparar este producto.")

            # Descontar ingredientes del inventario
            for ingrediente in producto.ingredientes:
                if isinstance(ingrediente, Base):
                    ingrediente.inventario -= 0.2  # Bases requieren 0.2 unidades
                else:
                    ingrediente.inventario -= 1  # Complementos requieren 1 unidad

            # Sumar venta
            self.ventas_dia += producto.get_precio_publico()
            print(f"Producto '{nombre_producto}' vendido exitosamente.")
            return True
        except ValueError as ve:
            print(f"Error: {ve}")
            return False

    def verificar_ingredientes(self, producto):
        """
        Verifica si hay suficientes ingredientes en el inventario para preparar un producto.
        Bases requieren al menos 0.2 unidades, complementos requieren 1 unidad.
        """
        for ingrediente in producto.ingredientes:
            if isinstance(ingrediente, Base) and ingrediente.inventario < 0.2:
                return False
            elif not isinstance(ingrediente, Base) and ingrediente.inventario < 1:
                return False
        return True

    def resumen_ventas(self):
        """
        Imprime un resumen de las ventas del día.
        """
        print(f"Ventas totales del día: ${self.ventas_dia}")

    def renovar_inventario(self):
        """
        Restaura el inventario de todos los ingredientes a un nivel inicial (por ejemplo, 10 unidades para todos).
        """
        for ingrediente in self.ingredientes:
            ingrediente.inventario = 10
            print(f"Inventario de {ingrediente.get_nombre()} renovado a 10 unidades.")
