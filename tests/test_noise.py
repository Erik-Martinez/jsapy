import pytest
import numpy as np
import math
import warnings
from jsapy.noise import NoiseExposure, NoiseResult
from jsapy.noise_tools import noise_exposure

def test_calculate_laeq_d_correct():
    ne = NoiseExposure()
    laeq_t = 85
    time = 240
    result = ne.calculate_laeq_d("ID001", laeq_t, time)
    expected = laeq_t + 10 * math.log10(time / 480)
    assert pytest.approx(result, rel=1e-5) == expected

def test_calculate_laeq_d_warning_excessive_time():
    ne = NoiseExposure()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        ne.calculate_laeq_d("ID002", 85, 500)
        assert len(w) == 1
        assert issubclass(w[-1].category, UserWarning)
        assert "ID002- Exposure time exceeds 8 hours." in str(w[-1].message)

@pytest.mark.parametrize("laeq_t", ["bad", None])
def test_validate_inputs_invalid_laeq_t_type(laeq_t):
    ne = NoiseExposure()
    with pytest.raises(TypeError, match="ID003: LAeq,T must be a numeric value"):
        ne.calculate_laeq_d("ID003", laeq_t, 60)

@pytest.mark.parametrize("time", ["bad", None])
def test_validate_inputs_invalid_time_type(time):
    ne = NoiseExposure()
    with pytest.raises(TypeError, match="ID004: Exposure time must be a numeric value"):
        ne.calculate_laeq_d("ID004", 80, time)

def test_validate_inputs_negative_laeq_t():
    ne = NoiseExposure()
    with pytest.raises(ValueError, match="ID005: LAeq,T must be greater than zero."):
        ne.calculate_laeq_d("ID005", 0, 60)

def test_validate_inputs_negative_time():
    ne = NoiseExposure()
    with pytest.raises(ValueError, match="ID006: Exposure time must be greater than zero."):
        ne.calculate_laeq_d("ID006", 80, 0)

def test_calculate_total_single_value():
    ne = NoiseExposure()
    result = ne.calculate_total([85.0])
    assert isinstance(result, NoiseResult)
    assert pytest.approx(result.exposure_value, rel=1e-5) == 85.0
    assert not result.exceeds_limit
    assert result.exceeds_sup_action
    assert result.exceeds_inf_action

def test_calculate_total_multiple_values():
    ne = NoiseExposure()
    exposures = np.array([80.0, 83.0, 85.0])
    expected = 10 * math.log10(sum(10**(exposures / 10)))
    result = ne.calculate_total(exposures)
    assert isinstance(result, NoiseResult)
    assert pytest.approx(result.exposure_value, rel=1e-5) == expected

def test_noise_result_with_hearing_protection():
    r = NoiseResult(
        exposure_value=88.0,
        inf_action_value=80,
        sup_action_value=85,
        limit_value=87,
        with_hearing_protection=True,
        protected_laeq_d=85.0
    )
    assert r.exceeds_inf_action
    assert r.exceeds_sup_action
    assert not r.exceeds_limit
    assert r.with_hearing_protection
    assert r.protected_exposure_value == 85.0

def test_noise_result_display_text_exceeds_limit():
    r = NoiseResult(90.0, 80, 85, 87)
    output = r.to_display()
    assert "exceeds the **limit value**" in output
    assert "Immediate action is required." in output

def test_noise_result_display_text_with_protection():
    r = NoiseResult(90.0, 80, 85, 87, with_hearing_protection=True, protected_laeq_d=85.0)
    output = r.to_display()
    assert "Protected LAeq,d" in output
    assert "exceeds the **superior action value**" in output

def test_noise_result_to_dict():
    r = NoiseResult(85.0, 80, 85, 87, True, 83.0)
    d = r.to_dict()
    assert d["exposure_value"] == 85.0
    assert d["protected_exposure_value"] == 83.0
    assert d["with_hearing_protection"]
    assert d["exceeds_inf_action"]
    assert not d["exceeds_limit"]


def test_noise_exposure_single_task():
    tasks = [{"name": "Pulido", "laeq_t": 85, "time": 240}]
    result = noise_exposure(tasks)
    expected = 85 + 10 * math.log10(240 / 480)
    assert isinstance(result, NoiseResult)
    assert pytest.approx(result.exposure_value, rel=1e-5) == expected

def test_noise_exposure_multiple_tasks():
    tasks = [
        {"name": "Metal Grinding", "laeq_t": 90, "time": 60},
        {"name": "Jackhammering", "laeq_t": 87, "time": 120},
        {"laeq_t": 80, "time": 300}  # sin nombre
    ]
    exposures = [90 + 10*math.log10(60/480),
                 87 + 10*math.log10(120/480),
                 80 + 10*math.log10(300/480)]
    expected_total = 10 * math.log10(sum(10**(e/10) for e in exposures))
    result = noise_exposure(tasks)
    assert isinstance(result, NoiseResult)
    assert pytest.approx(result.exposure_value, rel=1e-5) == expected_total

def test_noise_exposure_input_not_list():
    with pytest.raises(TypeError, match="Invalid input: 'tasks' must be a list of dictionaries"):
        noise_exposure("not_a_list")

def test_noise_exposure_task_not_dict():
    with pytest.raises(TypeError, match="Task entry #2 must be a dictionary."):
        noise_exposure([
            {"laeq_t": 85, "time": 60},
            "invalid_entry"
        ])

def test_noise_exposure_exceeding_time_warning():
    tasks = [{"name": "Welding", "laeq_t": 88, "time": 500}]
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        noise_exposure(tasks)
        assert len(w) == 1
        assert issubclass(w[-1].category, UserWarning)
        assert "Welding- Exposure time exceeds 8 hours." in str(w[-1].message)

def test_noise_exposure_with_custom_thresholds():
    tasks = [{"laeq_t": 92, "time": 480}]
    result = noise_exposure(tasks, inf_action_value=70, sup_action_value=80, limit_value=85)
    assert result.exceeds_inf_action is True
    assert result.exceeds_sup_action is True
    assert result.exceeds_limit is True