"""
jsapy: Tools for Occupational Safety and Health Statistics and Risk Assessment

jsapy is a Python library designed to support professionals and researchers in the field 
of occupational safety and health. It provides a structured set of tools for calculating 
accident rates, assessing human exposure to mechanical vibrations, and generating 
standardized risk indicators based on international norms and regulations 
(e.g., ISO 5349, ISO 2631, ILO guidelines).

This package emphasizes transparency, traceability, and clarity in risk quantification, 
with consistent units, structured return objects, and fully documented methods.

Main Submodules
---------------
accidents_tools :
    Functions for calculating frequency rate, incidence rate, severity rate, lost days rate, 
    and safety performance index. Each function returns a `RateResult` object and supports 
    array-like inputs for batch evaluation.

vibration_tools :
    Functions to assess daily exposure to mechanical vibrations, including:
        - `vibrations_hand_arm` : for hand-arm transmitted vibrations.
        - `vibrations_body` : for whole-body vibration exposure.
    Both functions compute A(8) values and compare them against legal action and limit values,
    returning results as `VibraResult` objects.

tools :
    Includes utility functions such as `display`, which prints formatted summaries of result objects.
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