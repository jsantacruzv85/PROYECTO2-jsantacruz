from abc import ABC, abstractmethod

class Producto(ABC):
    @abstractmethod
    def calcular_costo(self):
        """
        Calcula el costo del producto.
        Debe ser implementado por las subclases.
        """
        pass

    @abstractmethod
    def calcular_rentabilidad(self):
        """
        Calcula la rentabilidad del producto.
        Debe ser implementado por las subclases.
        """
        pass

    @abstractmethod
    def calcular_calorias(self):
        """
        Calcula las calorías del producto.
        Debe ser implementado por las subclases.
        """
        pass
