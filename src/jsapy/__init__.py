# jsapy/__init__.py
"""
docstring(sin terminar)

Submódulos principales:
    - accidents: Contiene clases y funciones para el cálculo de tasas de accidentes.
    - ... (puedes añadir aquí la descripción de otros submódulos a medida que los crees)
"""

# --- Info of the version ---
from importlib.metadata import version
__version__ = version("jsapy")

# --- Imports from submodules ---
from .accidents_tools import frequency_rate, incidence_rate, severity_rate, lost_days_rate, safety_rate
from .vibration_tools import vibrations_hand_arm
from .tools import display




__all__ = [
    '__version__', # Añade __version__ a la lista __all__ si quieres que sea parte de la API pública
    'display', # Función importada de accidents_tools.py 
    'frequency_rate',  # Función importada de accidents_tools.py 
    'incidence_rate',
    'severity_rate',
    'lost_days_rate',
    'safety_rate',
    'vibrations_hand_arm'
]