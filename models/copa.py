from models.producto import Producto

class Copa(Producto):
    def __init__(self, nombre, precio_publico, tipo_vaso, ingredientes):
        """
        Inicializa una Copa con sus atributos.
        """
        self.nombre = nombre
        self.precio_publico = precio_publico
        self.tipo_vaso = tipo_vaso
        self.ingredientes = ingredientes  # Lista de objetos Ingrediente

    def calcular_costo(self):
        """
        Suma los precios de los ingredientes.
        """
        return sum(ingrediente.precio for ingrediente in self.ingredientes)

    def calcular_calorias(self):
        """
        Calcula las calorías del producto (suma calorías y multiplica por 0.95).
        """
        total_calorias = sum(ingrediente.calorias for ingrediente in self.ingredientes)
        return round(total_calorias * 0.95, 2)

    def calcular_costo_produccion(self):
        """
        Alias de calcular_costo para uniformidad.
        """
        return self.calcular_costo()

    def calcular_rentabilidad(self):
        """
        Calcula la rentabilidad del producto.
        """
        costo = self.calcular_costo()
        return self.precio_publico - costo

    # Getters
    def get_nombre(self):
        """
        Retorna el nombre del producto.
        """
        return self.nombre

    def get_tipo_vaso(self):
        """
        Retorna el tipo de vaso.
        """
        return self.tipo_vaso

    def get_precio_publico(self):
        """
        Retorna el precio público del producto.
        """
        return self.precio_publico
