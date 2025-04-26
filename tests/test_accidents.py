import pytest
import numpy as np
from jsapy.accidents import RateResult, Rates, FrequencyRate, IncidenceRate, SeverityRate, LostDaysRate, SafetyRate
from jsapy.accidents_tools import frequency_rate, incidence_rate, severity_rate, lost_days_rate, safety_rate

def test_rate_result_str():
    result = RateResult("Test Rate", 123.4567, 1000, "accidents", "work hours")
    assert str(result) == "123.457"

def test_validate_factor_valid():
    rates = Rates()
    assert rates._validate_factor(1000) == 1000

def test_validate_factor_invalid():
    rates = Rates()
    with pytest.raises(ValueError):
        rates._validate_factor(-1000)
    with pytest.raises(ValueError):
        rates._validate_factor("invalid")

def test_validate_input_valid():
    rates = Rates()
    num = np.array([1, 2, 3])
    den = np.array([4, 5, 6])
    rates._validate_input(num, den)

def test_validate_input_invalid():
    rates = Rates()
    with pytest.raises(ValueError):
        rates._validate_input(np.array([-1, 2, 3]), np.array([4, 5, 6]))
    with pytest.raises(ValueError):
        rates._validate_input(np.array([1, 2, 3]), np.array([0, 0, 0]))
    with pytest.raises(TypeError):
        rates._validate_input(np.array(["a", "b", "c"]), np.array([4, 5, 6]))

def test_calculate():
    rates = Rates()
    num = np.array([3, 7, 10])
    den = np.array([50000, 120000, 200000])
    result = rates.calculate(num, den, factor=1000)
    expected = (np.sum(num) * 1000) / np.sum(den)
    assert pytest.approx(result, rel=1e-5) == expected

# Frecuency rate
def test_calculate_frequency_rate():
    freq_rate = FrequencyRate()
    num = np.array([3, 7, 10])
    den = np.array([50000, 120000, 200000])
    result = freq_rate.calculate(num, den)
    expected_value = (np.sum(num) * 10**6) / np.sum(den)
    assert pytest.approx(result.rate_value, rel=1e-5) == expected_value
    assert result.rate_name == "Frequency Rate"
    assert result.factor == 10**6
    assert result.num_unit == "accidents"
    assert result.den_unit == "work hours"
    
def test_frequency_rate_function():
    num_accidents = np.array([3, 7, 10])
    hours_worked = np.array([50000, 120000, 200000])
    result = frequency_rate(num_accidents, hours_worked)
    expected_value = (np.sum(num_accidents) * 10**6) / np.sum(hours_worked)
    assert isinstance(result, RateResult)
    assert pytest.approx(result.rate_value, rel=1e-5) == expected_value
    assert result.rate_name == "Frequency Rate"
    assert result.factor == 10**6
    assert result.num_unit == "accidents"
    assert result.den_unit == "work hours"


# Incidence rate
def test_calculate_incidence_rate():
    inc_rate = IncidenceRate()
    num = np.array([3, 7, 10])
    den = np.array([100, 150, 200])
    result = inc_rate.calculate(num, den)
    expected_value = (np.sum(num) * 10**5) / np.sum(den)
    assert pytest.approx(result.rate_value, rel=1e-5) == expected_value
    assert result.rate_name == "Incidence Rate"
    assert result.factor == 10**5
    assert result.num_unit == "accidents"
    assert result.den_unit == "number of workers"

def test_incidence_rate_function():
    num_accidents = np.array([3, 7, 10])
    num_workers = np.array([100, 150, 200])
    result = incidence_rate(num_accidents, num_workers)
    expected_value = (np.sum(num_accidents) * 10**5) / np.sum(num_workers)
    assert isinstance(result, RateResult)
    assert pytest.approx(result.rate_value, rel=1e-5) == expected_value
    assert result.rate_name == "Incidence Rate"
    assert result.factor == 10**5
    assert result.num_unit == "accidents"
    assert result.den_unit == "number of workers"
    
# Severity Rate
def test_calculate_severity_rate():
    sev_rate = SeverityRate()
    num = np.array([5000, 10000, 20000])
    den = np.array([50000, 120000, 200000])
    result = sev_rate.calculate(num, den)
    expected_value = (np.sum(num) * 10**5) / np.sum(den)
    assert pytest.approx(result.rate_value, rel=1e-5) == expected_value
    assert result.rate_name == "Severity Rate"
    assert result.factor == 10**5
    assert result.num_unit == "work days lost"
    assert result.den_unit == "work hours"
    
def test_severity_rate_function():
    lost_days = np.array([5000, 10000, 20000])
    hours_worked = np.array([50000, 120000, 200000])
    result = severity_rate(lost_days, hours_worked)
    expected_value = (np.sum(lost_days) * 10**5) / np.sum(hours_worked)
    assert isinstance(result, RateResult)
    assert pytest.approx(result.rate_value, rel=1e-5) == expected_value
    assert result.rate_name == "Severity Rate"
    assert result.factor == 10**5
    assert result.num_unit == "work days lost"
    assert result.den_unit == "work hours"
    
# Lost Days Rate
def test_lost_days_rate_calculate():
    lost_rate = LostDaysRate()
    num_accidents = np.array([5, 10, 7])
    hours_worked = np.array([100000, 200000, 150000])
    days_lost = np.array([50, 120, 80])
    result = lost_rate.calculate(num_accidents, hours_worked, days_lost)

    total_accidents = np.sum(num_accidents)
    total_hours = np.sum(hours_worked)
    total_lost_days = np.sum(days_lost)

    frequency_rate = (total_accidents * 10**6) / total_hours
    severity_rate = (total_lost_days * 10**3) / total_hours
    expected_value = (severity_rate * 10**3) / frequency_rate

    assert isinstance(result, RateResult)
    assert pytest.approx(result.rate_value, rel=1e-5) == expected_value
    assert result.rate_name == "Lost Days Rate"
    assert result.factor == 1
    assert result.num_unit == "work days lost"
    assert result.den_unit == "accident"
    
def test_lost_days_rate_function():
    num_accidents = np.array([3, 8, 5])
    hours_worked = np.array([80000, 150000, 120000])
    days_lost = np.array([30, 90, 60])
    result = lost_days_rate(num_accidents, hours_worked, days_lost)

    total_accidents = np.sum(num_accidents)
    total_hours = np.sum(hours_worked)
    total_lost_days = np.sum(days_lost)

    frequency_rate = (total_accidents * 10**6) / total_hours
    severity_rate = (total_lost_days * 10**3) / total_hours
    expected_value = (severity_rate * 10**3) / frequency_rate

    assert isinstance(result, RateResult)
    assert pytest.approx(result.rate_value, rel=1e-5) == expected_value
    assert result.rate_name == "Lost Days Rate"
    assert result.factor == 1
    assert result.num_unit == "work days lost"
    assert result.den_unit == "accident"
    
# Safety Rate
def test_safety_rate_calculate():
    safety_rate = SafetyRate()
    num_accidents = np.array([2, 3])
    num_workers = np.array([100, 150])
    hours_worked = np.array([40000, 60000])
    result = safety_rate.calculate(num_accidents, num_workers, hours_worked)

    factor = 10**5

    total_accidents = np.sum(num_accidents)
    total_workers = np.sum(num_workers)
    total_hours = np.sum(hours_worked)

    num_rate = (total_workers * factor) / total_accidents
    expected_value = num_rate / total_hours

    assert isinstance(result, RateResult)
    assert pytest.approx(result.rate_value, rel=1e-5) == expected_value
    assert result.rate_name == "Safety Rate"
    assert result.factor == total_hours
    assert result.num_unit == "workers"
    assert result.den_unit == "work hours"
    
def test_safety_rate_function():
    num_accidents = np.array([1, 4])
    num_workers = np.array([80, 120])
    hours_worked = np.array([30000, 70000])
    result = safety_rate(num_accidents, num_workers, hours_worked)

    factor = 10**5

    total_accidents = np.sum(num_accidents)
    total_workers = np.sum(num_workers)
    total_hours = np.sum(hours_worked)

    num_rate = (total_workers * factor) / total_accidents
    expected_value = num_rate / total_hours

    assert isinstance(result, RateResult)
    assert pytest.approx(result.rate_value, rel=1e-5) == expected_value
    assert result.rate_name == "Safety Rate"
    assert result.factor == total_hours
    assert result.num_unit == "workers"
    assert result.den_unit == "work hours"