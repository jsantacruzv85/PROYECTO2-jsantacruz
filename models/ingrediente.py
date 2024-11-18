from abc import ABC, abstractmethod

class Ingrediente(ABC):
    def __init__(self, nombre, precio, calorias, inventario, es_vegetariano):
        self.nombre = nombre
        self.precio = precio
        self.calorias = calorias
        self.inventario = inventario
        self.es_vegetariano = es_vegetariano

    def es_sano(self):
        """
        Determina si el ingrediente es sano.
        Un ingrediente es sano si tiene menos de 100 calorías o si es vegetariano.
        """
        return self.calorias < 100 or self.es_vegetariano

    @abstractmethod
    def abastecer(self):
        """
        Método abstracto para reabastecer inventario.
        Debe ser implementado por las subclases.
        """
        pass

    # Getters y Setters
    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_precio(self):
        return self.precio

    def set_precio(self, precio):
        self.precio = precio

    def get_calorias(self):
        return self.calorias

    def set_calorias(self, calorias):
        self.calorias = calorias

    def get_inventario(self):
        return self.inventario

    def set_inventario(self, inventario):
        self.inventario = inventario

    def get_es_vegetariano(self):
        return self.es_vegetariano

    def set_es_vegetariano(self, es_vegetariano):
        self.es_vegetariano = es_vegetariano
