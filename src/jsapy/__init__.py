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
from .vibration_tools import vibrations_hand_arm, vibrations_body
from .tools import display




__all__ = [
    '__version__', 
    'display', 
    'frequency_rate',  
    'incidence_rate',
    'severity_rate',
    'lost_days_rate',
    'safety_rate',
    'vibrations_hand_arm',
    'vibrations_body'
]