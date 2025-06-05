import pytest
import numpy as np
import math
import warnings
from jsapy.vibrations import HandArmVibrations,  VibraResult, CompleteBodyVibrations
from jsapy.vibration_tools import vibrations_hand_arm, vibrations_body

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
    
# test body
def test_calculate_A_vertex_correct():
    cbv = CompleteBodyVibrations()
    ax, ay, az = 0.5, 0.4, 0.3
    t = 4
    Ax, Ay, Az = cbv.calculate_A_vertex("ID001", ax, ay, az, t)
    factor = math.sqrt(t / 8)
    assert pytest.approx(Ax, rel=1e-5) == 1.4 * ax * factor
    assert pytest.approx(Ay, rel=1e-5) == 1.4 * ay * factor
    assert pytest.approx(Az, rel=1e-5) == az * factor

def test_calculate_total_correct():
    cbv = CompleteBodyVibrations()
    x = np.array([0.4, 0.5])
    y = np.array([0.3, 0.3])
    z = np.array([0.6, 0.2])
    result = cbv.calculate_total(x, y, z)
    expected_x = math.sqrt(np.sum(x**2))
    expected_y = math.sqrt(np.sum(y**2))
    expected_z = math.sqrt(np.sum(z**2))
    expected_max = max([expected_x, expected_y, expected_z])
    
    assert isinstance(result, VibraResult)
    assert pytest.approx(result.exposure_value, rel=1e-5) == expected_max
    assert result.exposure_type == "body"
    assert result.unit == "m/s²"

def test_validate_inputs_missing_axis():
    cbv = CompleteBodyVibrations()
    with pytest.raises(ValueError, match="ID002- Missing required axis value: 'ay'"):
        cbv.calculate_A_vertex("ID002", ax=0.5, ay=None, az=0.3, exposure_time_hours=4)

def test_validate_inputs_negative_axis():
    cbv = CompleteBodyVibrations()
    with pytest.raises(ValueError, match="ID003-'az' must be non-negative."):
        cbv.calculate_A_vertex("ID003", ax=0.2, ay=0.2, az=-0.1, exposure_time_hours=2)

def test_validate_inputs_non_numeric_axis():
    cbv = CompleteBodyVibrations()
    with pytest.raises(TypeError, match="ID004- 'ax' must be numeric."):
        cbv.calculate_A_vertex("ID004", ax="bad", ay=0.2, az=0.3, exposure_time_hours=4)

def test_validate_inputs_zero_exposure_time():
    cbv = CompleteBodyVibrations()
    with pytest.raises(ValueError, match="ID005-  Exposure time must be non-negative."):
        cbv.calculate_A_vertex("ID005", ax=0.2, ay=0.2, az=0.2, exposure_time_hours=0)

def test_warning_exposure_time_above_8():
    cbv = CompleteBodyVibrations()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        cbv.calculate_A_vertex("ID006", ax=0.3, ay=0.3, az=0.3, exposure_time_hours=9)
        assert len(w) == 1
        assert issubclass(w[-1].category, UserWarning)
        assert "ID006- Exposure time exceeds 8 hours." in str(w[-1].message)
        


def test_vibrations_body_function():
    machines = [
        {"name": "Pistola neumática", "ax": 1.0, "ay": 1.2, "az": 0.9, "time": 3},
        {"name": "Taladro", "ax": 2.0, "ay": 1.5, "az": 1.0, "time": 2.0},
        {"ax": 1.0, "ay": 1.0, "az": 1.0, "time": 1.0}  # sin nombre
    ]
    result = vibrations_body(machines)
    assert isinstance(result, VibraResult)
    assert result.exposure_type == "body"
    assert result.unit == "m/s²"

    def expected_component(a, factor=1.4):  # az no se multiplica por 1.4
        return a * factor * math.sqrt(1.0 / 8)
    
    values = []
    for m in machines:
        ax, ay, az = m["ax"], m["ay"], m["az"]
        time = m["time"]
        factor = math.sqrt(time / 8)
        Ax = 1.4 * ax * factor
        Ay = 1.4 * ay * factor
        Az = az * factor
        values.append((Ax, Ay, Az))
    
    xs = [v[0] for v in values]
    ys = [v[1] for v in values]
    zs = [v[2] for v in values]

    expected_x = math.sqrt(sum(x**2 for x in xs))
    expected_y = math.sqrt(sum(y**2 for y in ys))
    expected_z = math.sqrt(sum(z**2 for z in zs))
    expected_total = max([expected_x, expected_y, expected_z])
    
    assert pytest.approx(result.exposure_value, rel=1e-5) == expected_total
