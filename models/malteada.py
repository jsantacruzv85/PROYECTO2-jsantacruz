from models.producto import Producto

class Malteada(Producto):
    def __init__(self, nombre, precio_publico, volumen, ingredientes):
        """
        Inicializa una Malteada con sus atributos.
        """
        self.nombre = nombre
        self.precio_publico = precio_publico
        self.volumen = volumen
        self.ingredientes = ingredientes  # Lista de objetos Ingrediente

    def calcular_costo(self):
        """
        Suma los precios de los ingredientes más $500 por el vaso plástico.
        """
        return sum(ingrediente.precio for ingrediente in self.ingredientes) + 500

    def calcular_calorias(self):
        """
        Calcula las calorías del producto (suma calorías y agrega 200).
        """
        total_calorias = sum(ingrediente.calorias for ingrediente in self.ingredientes)
        return total_calorias + 200

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

    def get_volumen(self):
        """
        Retorna el volumen de la malteada.
        """
        return self.volumen

    def get_precio_publico(self):
        """
        Retorna el precio público del producto.
        """
        return self.precio_publico
