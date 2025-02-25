import pytest
import numpy as np
from jsapy.accidents import basic_rate  

# Test Classes (no terminado)

class TestBasicRate:
    def test_basic_rate_with_numbers(self):
        "Test basic_rate with individual integer numbers."
        expected_result = 10000.0
        result = basic_rate(10000, 10, 10)
        assert np.isclose(result, expected_result), "Error with individual numbers."

    def test_basic_rate_with_lists(self):
        "Test basic_rate with lists as inputs."
        num = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
        den = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        expected_result = 10000.0
        result = basic_rate(num, den, 10)
        assert np.isclose(result, expected_result), "Error with lists."

    def test_basic_rate_with_numpy_arrays(self):
        "Test basic_rate with NumPy arrays as inputs."
        num = np.array([100, 200, 300])
        den = np.array([10, 20, 30])
        factor = 5
        expected_result = (600 * 5) / 60
        result = basic_rate(num, den, factor)
        assert np.isclose(result, 50.0), "Error with NumPy arrays."

    def test_basic_rate_type_error_num(self):
        "Test basic_rate raises TypeError when num contains non-numeric elements."
        num = ["a", 2, 3]
        den = [1, 2, 3]
        factor = 100
        with pytest.raises(TypeError):
            basic_rate(num, den, factor)

    def test_basic_rate_type_error_den(self):
        "Test basic_rate raises TypeError when den is not numeric."
        num = [1, 2, 3]
        den = ["a", 2, 3]
        factor = 100
        with pytest.raises(TypeError):
            basic_rate(num, den, factor)

    def test_basic_rate_type_error_factor(self):
        "Test basic_rate raises TypeError when factor is not numeric."
        num = [1, 2, 3]
        den = [1, 2, 3]
        factor = "a"
        with pytest.raises(TypeError):
            basic_rate(num, den, factor)

    def test_basic_rate_value_error_negative_num(self):
        "Test basic_rate raises ValueError when num contains negative values."
        num = [-1, 2, 3]
        den = [1, 2, 3]
        factor = 100
        with pytest.raises(ValueError):
            basic_rate(num, den, factor)

    def test_basic_rate_value_error_negative_den(self):
        "Test basic_rate raises ValueError when den contains negative values."
        num = [1, 2, 3]
        den = [-1, 2, 3]
        factor = 100
        with pytest.raises(ValueError):
            basic_rate(num, den, factor)

    def test_basic_rate_value_error_zero_factor(self):
        "Test basic_rate raises ValueError when factor is zero."
        num = [1, 2, 3]
        den = [1, 2, 3]
        factor = 0
        with pytest.raises(ValueError):
            basic_rate(num, den, factor)

    def test_basic_rate_value_error_factor_negative(self):
        "Test basic_rate raises ValueError when factor is negative."
        num = 1000
        den = 100
        factor = -1
        with pytest.raises(ValueError):
            basic_rate(num, den, factor)