# jsapy/__init__.py
"""
docstring(sin terminar)

Submódulos principales:
    - accidents: Contiene clases y funciones para el cálculo de tasas de accidentes.
    - ... (puedes añadir aquí la descripción de otros submódulos a medida que los crees)
"""

# --- Información de versión ---
from importlib.metadata import version
__version__ = version("jsapy")

# --- Imports desde el submódulo 'accidents' ---
from .accidents import frequency_rate, Rates, display  # Importa la función y la clase Rates
# from .accidents import otra_funcion_de_accidents, OtraClaseDeAccidents
# ... (añade aquí más imports de 'accidents.py' si los necesitas)

# --- Imports desde otros submódulos (a medida que los crees) ---
# from .otro_submodulo import funcion_de_otro_submodulo, ClaseDeOtroSubmodulo
# ... (añade aquí imports de otros submódulos cuando los crees)


__all__ = [
    '__version__', # Añade __version__ a la lista __all__ si quieres que sea parte de la API pública
    'frequency_rate',  # Función importada de accidents.py
    'Rates',         # Clase importada de accidents.py
    'display'
]