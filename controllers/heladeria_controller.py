from flask import render_template, redirect, url_for, flash
from datetime import datetime
from database import db
from models.db_models import Ingrediente, Producto


class HeladeriaController:
    def __init__(self):
        """
        Inicializa la clase con una lista para registrar las ventas realizadas.
        """
        if not hasattr(HeladeriaController, 'ventas'):
            # Lista compartida entre todas las instancias de HeladeriaController
            HeladeriaController.ventas = []

    def listar_productos(self):
        """
        Obtiene todos los productos disponibles desde la base de datos.
        """
        try:
            productos = Producto.query.options(
                db.joinedload(Producto.ingrediente1),
                db.joinedload(Producto.ingrediente2),
                db.joinedload(Producto.ingrediente3)
            ).all()
            return render_template('index.html', productos=productos)
        except Exception as e:
            flash("Error al listar los productos.", "error")
            print(f"Error en listar_productos: {e}")  # Para depuración
            raise

    def vender_producto(self, producto_id):
        """
        Gestiona la venta de un producto por su ID.
        Retorna:
        - "¡Vendido!" si la venta fue exitosa.
        - ValueError con el nombre del ingrediente si no se cumple la regla de venta.
        """
        producto = Producto.query.get_or_404(producto_id)

        # Verificar disponibilidad de ingredientes
        if producto.ingrediente1.inventario < 1:
            raise ValueError(producto.ingrediente1.nombre)
        if producto.ingrediente2.inventario < 1:
            raise ValueError(producto.ingrediente2.nombre)
        if producto.ingrediente3.inventario < 1:
            raise ValueError(producto.ingrediente3.nombre)

        # Reducir inventarios
        producto.ingrediente1.inventario -= 1
        producto.ingrediente2.inventario -= 1
        producto.ingrediente3.inventario -= 1

        # Registrar la venta en memoria
        HeladeriaController.ventas.append({
            'producto': producto.nombre,
            'precio': producto.precio_publico,
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Guardar los cambios en la base de datos
        db.session.commit()
        return "¡Vendido!"

    def manejar_venta(self, producto_id):
        """
        Maneja el proceso de venta, capturando posibles errores y retornando mensajes apropiados.
        """
        try:
            mensaje = self.vender_producto(producto_id)
            flash(mensaje, "success")
        except ValueError as ve:
            # Si ocurre un ValueError, retorna un mensaje personalizado
            flash(f"¡Oh no! Nos hemos quedado sin {ve}.", "error")
        except Exception as e:
            # Manejo de cualquier otro error
            flash("Ha ocurrido un error inesperado al intentar realizar la venta.", "error")
            print(f"Error en manejar_venta: {e}")
        return redirect(url_for('index'))

    def mostrar_resumen_ventas(self):
        """
        Retorna el resumen de ventas basado en la lista de memoria.
        """
        try:
            return render_template('resumen_ventas.html', ventas=HeladeriaController.ventas)
        except Exception as e:
            flash("Error al mostrar el resumen de ventas.", "error")
            print(f"Error en mostrar_resumen_ventas: {e}")  # Para depuración
            raise

    def producto_mas_rentable(self):
        """
        Encuentra y muestra el producto más rentable.
        """
        try:
            productos = Producto.query.options(
                db.joinedload(Producto.ingrediente1),
                db.joinedload(Producto.ingrediente2),
                db.joinedload(Producto.ingrediente3)
            ).all()

            if not productos:
                raise ValueError("No hay productos disponibles para calcular rentabilidad.")

            # Calcular el producto más rentable
            producto_rentable = max(productos, key=lambda p: p.calcular_rentabilidad())
            rentabilidad = producto_rentable.calcular_rentabilidad()

            return render_template(
                'producto_rentable.html',
                producto=producto_rentable,
                rentabilidad=rentabilidad
            )
        except ValueError as ve:
            flash(str(ve), "error")
            raise
        except Exception as e:
            flash("Error al calcular el producto más rentable.", "error")
            print(f"Error en producto_mas_rentable: {e}")  # Para depuración
            raise

    def mostrar_inventario(self):
        """
        Obtiene el inventario actual de ingredientes.
        """
        try:
            ingredientes = Ingrediente.query.all()
            return render_template('inventario.html', ingredientes=ingredientes)
        except Exception as e:
            flash("Error al mostrar el inventario.", "error")
            print(f"Error en mostrar_inventario: {e}")  # Para depuración
            raise

    def recargar_inventario(self, ingrediente_id, cantidad):
        """
        Recarga el inventario de un ingrediente en específico.
        """
        try:
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")

            ingrediente = Ingrediente.query.get_or_404(ingrediente_id)
            ingrediente.inventario += cantidad
            db.session.commit()
            flash(f"Inventario de '{ingrediente.nombre}' recargado en {cantidad} unidades.", "success")
        except ValueError as ve:
            flash(str(ve), "error")
            raise
        except Exception as e:
            flash("Error al recargar el inventario.", "error")
            print(f"Error en recargar_inventario: {e}")  # Para depuración
            raise
        return redirect(url_for('mostrar_inventario'))

    def verificar_inventario_bajo(self):
        """
        Verifica si hay ingredientes con inventario bajo y muestra alertas.
        """
        try:
            UMBRAL_INVENTARIO_BAJO = 5

            # Obtener los ingredientes con inventario por debajo del umbral
            ingredientes_bajos = Ingrediente.query.filter(Ingrediente.inventario < UMBRAL_INVENTARIO_BAJO).all()

            if ingredientes_bajos:
                for ingrediente in ingredientes_bajos:
                    flash(f"El inventario de '{ingrediente.nombre}' es bajo: {ingrediente.inventario} unidades.", "warning")
            else:
                flash("Todos los ingredientes tienen inventario suficiente.", "success")
        except Exception as e:
            flash("Error al verificar inventario bajo.", "error")
            print(f"Error en verificar_inventario_bajo: {e}")  # Para depuración
            raise
        return redirect(url_for('mostrar_inventario'))
