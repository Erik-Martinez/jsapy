import pytest
import numpy as np
import math
from jsapy.vibrations import HandArmVibrations,  VibraResult
from jsapy.vibration_tools import vibrations_hand_arm

def test_calculate_a8_with_aw():
    hav = HandArmVibrations()
    result = hav.calculate_a8("TestID", aw=3.0, exposure_time_hours=4)
    expected = 3.0 * math.sqrt(4 / 8)
    assert pytest.approx(result, rel=1e-5) == expected
    
def test_calculate_a8_with_axes():
    hav = HandArmVibrations()
    result = hav.calculate_a8("TestID", ax=1.0, ay=2.0, az=2.0, exposure_time_hours=4)
    aw = math.sqrt(1.0**2 + 2.0**2 + 2.0**2)
    expected = aw * math.sqrt(4 / 8)
    assert pytest.approx(result, rel=1e-5) == expected
    
def test_validate_inputs_error_both_aw_and_axes():
    hav = HandArmVibrations()
    with pytest.raises(ValueError, match="Must be provided either 'aw' or 'ax, ay, az', not both."):
        hav.calculate_a8("TestID", aw=2.0, ax=1.0, ay=1.0, az=1.0, exposure_time_hours=4)

def test_validate_inputs_missing_axis():
    hav = HandArmVibrations()
    with pytest.raises(ValueError, match="Missing required axis value: 'ay'"):
        hav.calculate_a8("TestID", ax=1.0, az=2.0, exposure_time_hours=4)

def test_validate_inputs_negative_axis():
    hav = HandArmVibrations()
    with pytest.raises(ValueError, match="'az' must be non-negative"):
        hav.calculate_a8("TestID", ax=1.0, ay=1.0, az=-1.0, exposure_time_hours=4)

def test_validate_inputs_invalid_aw_type():
    hav = HandArmVibrations()
    with pytest.raises(TypeError, match="'aw' must be numeric"):
        hav.calculate_a8("TestID", aw="not_a_number", exposure_time_hours=4)

def test_validate_inputs_negative_exposure_time():
    hav = HandArmVibrations()
    with pytest.raises(ValueError, match="Exposure time must be non-negative"):
        hav.calculate_a8("TestID", aw=2.0, exposure_time_hours=0)

def test_calculate_total_single_value():
    hav = HandArmVibrations()
    result = hav.calculate_total([3.0])
    assert isinstance(result, VibraResult)
    assert pytest.approx(result.exposure_value, rel=1e-5) == 3.0
    assert result.exposure_type == "hand-arm"
    assert result.unit == "m/s²"

def test_calculate_total_multiple_values():
    hav = HandArmVibrations()
    values = np.array([2.0, 3.0, 6.0])
    expected = math.sqrt(np.sum(values**2))
    result = hav.calculate_total(values)
    assert pytest.approx(result.exposure_value, rel=1e-5) == expected
    
# Test Function
def test_vibrations_hand_arm_function():
    machines = [
        {"name": "Taladro", "ax": 2.0, "ay": 1.5, "az": 1.0, "time": 2.0},
        {"name": "Pulidora", "aw": 3.2, "time": 1.5},
        {"aw": 2.0, "time": 0.5}  # sin nombre
    ]
    result = vibrations_hand_arm(machines)
    assert isinstance(result, VibraResult)
    assert result.exposure_type == "hand-arm"
    assert result.unit == "m/s²"
    assert pytest.approx(result.exposure_value, rel=1e-5) == math.sqrt(
        sum([
            (math.sqrt(2.0**2 + 1.5**2 + 1.0**2) * math.sqrt(2.0 / 8))**2,
            (3.2 * math.sqrt(1.5 / 8))**2,
            (2.0 * math.sqrt(0.5 / 8))**2
        ])
    )
