import os
from flask import Flask, request, render_template, redirect, url_for, flash
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from database import db  # Importar la instancia de la base de datos
from models.db_models import Ingrediente, Producto
from controllers.heladeria_controller import HeladeriaController  # Importar el controlador

# Cargar las variables de entorno
load_dotenv()

# Configuración de Flask
app = Flask(__name__, template_folder="views")
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')  # Cargar la clave secreta desde el .env

# Inicializar SQLAlchemy con la aplicación
db.init_app(app)


def crear_base_de_datos():
    """
    Crea la base de datos si no existe.
    """
    connection_string = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    engine = create_engine(connection_string)

    try:
        # Crear la base de datos si no existe
        with engine.execution_options(isolation_level="AUTOCOMMIT").connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}"))
        print(f"Base de datos '{os.getenv('DB_NAME')}' creada o ya existente.")
    except Exception as e:
        print(f"Error al crear la base de datos: {e}")


def poblar_base_datos():
    """
    Pobla la base de datos con datos iniciales si está vacía.
    """
    with app.app_context():
        try:
            # Crear las tablas si no existen
            db.create_all()

            # Verificar si ya hay datos en la base de datos
            if Ingrediente.query.first() or Producto.query.first():
                print("La base de datos ya contiene datos. No se realizará la carga inicial.")
                return

            # Crear ingredientes
            ingredientes = [
                Ingrediente(nombre="Helado de Vainilla", precio=1000, calorias=150, inventario=20, es_vegetariano=True),
                Ingrediente(nombre="Helado de Chocolate", precio=1200, calorias=200, inventario=20, es_vegetariano=True),
                Ingrediente(nombre="Chispas de Chocolate", precio=500, calorias=50, inventario=30, es_vegetariano=True),
                Ingrediente(nombre="Crema Chantilly", precio=300, calorias=120, inventario=40, es_vegetariano=True)
            ]

            # Agregar ingredientes a la base de datos
            db.session.add_all(ingredientes)
            db.session.commit()

            # Crear productos
            productos = [
                Producto(
                    nombre="Copa Vainilla",
                    precio_publico=5000,
                    tipo="Copa",
                    ingrediente1_id=1,  # Helado de Vainilla
                    ingrediente2_id=3,  # Chispas de Chocolate
                    ingrediente3_id=4   # Crema Chantilly
                ),
                Producto(
                    nombre="Copa Chocolate",
                    precio_publico=5500,
                    tipo="Copa",
                    ingrediente1_id=2,  # Helado de Chocolate
                    ingrediente2_id=3,  # Chispas de Chocolate
                    ingrediente3_id=4   # Crema Chantilly
                ),
                Producto(
                    nombre="Malteada Vainilla",
                    precio_publico=6000,
                    tipo="Malteada",
                    ingrediente1_id=1,  # Helado de Vainilla
                    ingrediente2_id=3,  # Chispas de Chocolate
                    ingrediente3_id=4   # Crema Chantilly
                ),
                Producto(
                    nombre="Malteada Chocolate",
                    precio_publico=6500,
                    tipo="Malteada",
                    ingrediente1_id=2,  # Helado de Chocolate
                    ingrediente2_id=3,  # Chispas de Chocolate
                    ingrediente3_id=4   # Crema Chantilly
                )
            ]

            # Agregar productos a la base de datos
            db.session.add_all(productos)
            db.session.commit()

            print("Datos iniciales insertados correctamente.")
        except Exception as e:
            print(f"Error al poblar la base de datos: {e}")


def inicializar_app():
    """
    Inicializa la aplicación creando la base de datos y poblando datos si es necesario.
    """
    try:
        crear_base_de_datos()  # Crea la base de datos si no existe
        poblar_base_datos()    # Pobla la base de datos si está vacía
    except Exception as e:
        print(f"Error durante la inicialización de la aplicación: {e}")


# Rutas
@app.route('/')
def index():
    """
    Página principal: lista los productos disponibles.
    """
    return HeladeriaController().listar_productos()

@app.route('/vender/<int:producto_id>', methods=['POST'])
def vender(producto_id):
    """
    Maneja la venta de un producto. Captura errores específicos y muestra mensajes flash.
    """
    return HeladeriaController().manejar_venta(producto_id)

@app.route('/resumen-ventas')
def resumen_ventas():
    """
    Muestra el resumen de ventas realizadas.
    """
    return HeladeriaController().mostrar_resumen_ventas()

@app.route('/producto-mas-rentable')
def producto_mas_rentable():
    """
    Calcula y muestra el producto más rentable.
    """
    return HeladeriaController().producto_mas_rentable()

@app.route('/inventario')
def mostrar_inventario():
    """
    Muestra el inventario actual de ingredientes.
    """
    return HeladeriaController().mostrar_inventario()

@app.route('/recargar-inventario/<int:ingrediente_id>', methods=['POST'])
def recargar_inventario(ingrediente_id):
    """
    Recarga el inventario de un ingrediente específico.
    """
    try:
        cantidad = int(request.form['cantidad'])  # Captura la cantidad enviada por el formulario
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        return HeladeriaController().recargar_inventario(ingrediente_id, cantidad)
    except ValueError as ve:
        flash(str(ve), "error")
        return redirect(url_for('mostrar_inventario'))

@app.route('/verificar-inventario-bajo')
def verificar_inventario_bajo():
    """
    Verifica los ingredientes con inventario bajo y genera alertas.
    """
    return HeladeriaController().verificar_inventario_bajo()

if __name__ == '__main__':
    inicializar_app()  # Llamada para crear la base de datos y poblarla si es necesario
    app.run(debug=True)
