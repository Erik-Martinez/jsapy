import numpy as np

def basic_rate(num, den, factor):
    """
    Calculates a basic rate given a numerator, denominator, and factor.

    This function takes a numerator (num), a denominator (den), and a factor to calculate a rate.
    It is designed to handle lists or single numeric values for num and den.

    Args:
        num (numeric or list of numeric): Numerator value(s). Must be non-negative.
        den (numeric or list of numeric): Denominator value(s). Must be non-negative and non-zero.
        factor (numeric): Factor to multiply the rate. Must be positive.

    Returns:
        float: The calculated basic rate.

    Raises:
        TypeError: If num, den or factor are not numeric or if num or den contains non-numeric elements.
        ValueError: If num, den or factor are negative or zero.
        ZeroDivisionError: If the denominator is zero.

    Examples:
        >>> basic_rate(1000, 100, 10)
        100.0
        >>> basic_rate([1000, 2000], [100, 200], 10)
        100.0
    """
    
    num = np.atleast_1d(num)
    den = np.atleast_1d(den)
    
    #check data type
    if not np.issubdtype(num.dtype, np.number):
        raise TypeError("All elements in 'num' must be numeric.")
    if not np.issubdtype(den.dtype, np.number):
        raise TypeError("All elements in 'den' must be numeric.")
    if not isinstance(factor, (int, float)):
        raise TypeError("'factor' must be a numeric value.")
    
    #check values
    if not np.all(num >= 0) or not np.all(den >= 0):
        raise ValueError("All values must be positive.")
    if factor <= 0:
        raise ValueError("Factor mus be positive numeric value.")
    
    
    result = (sum(num) * factor) / sum(den)
    return result


class RateResult:
    "Class to store rate calculation results"
    def __init__(self, rate_name, rate_value, factor, num_unit, den_unit):
        self.rate_name = rate_name
        self.rate_value = rate_value
        self.factor = factor
        self.num_unit = num_unit
        self.den_unit = den_unit
              
    def __str__(self):
        return str(np.round(self.rate_value,2))

class Rates:
    "Base class for calculating rates of work accidentes"
    
    def __init__(self):
        self.feat_factor = 1000
               
    def _validate_factor(self, factor):
        """ 
        Initializes the Rates class with a factor 
       
        Args:
            factor (numeric): Factor to multiply the rate. Must be positive.
        """
        if not isinstance(factor, (int, float)) or factor <= 0:
            raise ValueError("Factor must be a positive numeric value.")
        
        return factor
        
    def _validate_input(self, num, den):
        """
        Validate the 'num' and 'den' inputs for rate calculation methods.

        Args:
            num (_type_): Numerator. Must be non-negative and non-zero. 
            den (_type_): Denominator. Must be non-negative and non-zero.
        """

        num = np.atleast_1d(num)
        den = np.atleast_1d(den)
        
        if not np.issubdtype(num.dtype, np.number):
            raise TypeError("All elements in 'num' must be numeric.")
        if not np.issubdtype(den.dtype, np.number):
            raise TypeError("All elements in 'den' must be numeric.")
        if not np.all(num >= 0) or not np.all(den>=0):
            raise ValueError("All values must be positive.")
        if not np.sum(num) > 0 or not np.sum(den) > 0:
            raise ValueError("The sum of num and the sum of den values must be superior to 0.")
        
    def basic_rate(self, num, den, factor=None):
        self._validate_input(num, den)
        
        factor_to_use = self._validate_factor(factor) if factor is not None else self.defeat_factor
        
        result = (np.sum(num) * factor_to_use) / np.sum(den)
        return result
    
    def frequency_rate(self, num_accidents, hours_worked, factor = None):
        
        factor_to_use = self._validate_factor(factor) if factor is not None else 10**6
        
        rate_value = self.basic_rate(num_accidents, hours_worked, factor_to_use)
        
        return RateResult(
            rate_name="Frequency Rate",
            rate_value=rate_value,
            factor=factor_to_use,
            num_unit="accidents",
            den_unit = "work hours"
        )
        
#function to display        
def display(rate_result):
    
    if not isinstance(rate_result, RateResult):
        raise TypeError("Display only works with RateResult class.")
    
    print(f"{rate_result.rate_name}: {rate_result.rate_value:.3f} {rate_result.num_unit} per {rate_result.factor} {rate_result.den_unit}.")
    
def frequency_rate(num_accidents, hours_worked, factor = None):
    """
    Calculates the accident frequency rate (independent function).

    Args:
        num_accidents (numeric or array-like): Number of accidents.
        hours_worked (numeric or array-like): Hours worked.
        factor (numeric, optional): Factor to multiply (default 1,000,000).

    Returns:
        RateResult Class
    """
    
    calculator = Rates()
    return calculator.frequency_rate(num_accidents, hours_worked, factor)
    