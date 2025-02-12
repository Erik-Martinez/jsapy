import numpy as np

class RateResult:
    """
    Class to store rate calculation results.

    Attributes
    ----------
    rate_name : str
        Name of the calculated rate (e.g., "Frequency Rate").
    rate_value : float
        Numerical value of the calculated rate.
    factor : int or float
        Factor used to scale the rate.
    num_unit : str
        Unit of the numerator (e.g., "accidents").
    den_unit : str
        Unit of the denominator (e.g., "work hours").
    """
    def __init__(self, rate_name, rate_value, factor, num_unit, den_unit):
        """
        Initialize a RateResult object.

        Parameters
        ----------
        rate_name : str
            Name of the calculated rate.
        rate_value : float
            Numerical value of the calculated rate.
        factor : float
            Factor used to scale the rate.
        num_unit : str
            Unit of the numerator.
        den_unit : str
            Unit of the denominator.
        """
        self.rate_name = rate_name
        self.rate_value = rate_value
        self.factor = factor
        self.num_unit = num_unit
        self.den_unit = den_unit
              
    def __str__(self):
        """
        Return a string representation of the rate value.

        Returns
        -------
        str
            String representation of the rate value, rounded to two decimal places.
        """
        return str(np.round(self.rate_value,2))


class Rates:
    """
    Base class for calculating rates of work accidents.

    This class provides a foundation for calculating various types of rates
    related to work accidents. It includes methods for validating input data
    and calculating basic rates, which can be extended by subclasses to
    implement specific rate calculations.

    Attributes
    ----------
    feat_factor : int
        Default factor used in rate calculations if a factor is not
        explicitly provided. Set to 1000.
    """
    
    def __init__(self):
        """
        Initialize a Rates object.

        Sets the default feature factor (`feat_factor`) to 1000.
        """
        
        self.defeat_factor = 1000
               
    def _validate_factor(self, factor):
        """
        Validate the input factor for rate calculations.

        Parameters
        ----------
        factor : numeric
            Factor to multiply the rate. Must be a positive numeric value.

        Returns
        -------
        factor : float
            The validated factor.

        Raises
        ------
        ValueError
            If `factor` is not a positive numeric value.
        """
        
        if not isinstance(factor, (int, float)) or factor <= 0:
            raise ValueError("Factor must be a positive numeric value.")
        
        return factor
        
    def _validate_input(self, num, den):
        """
        Validate the 'num' (numerator) and 'den' (denominator) inputs.

        This method ensures that the inputs for rate calculation methods
        are valid NumPy arrays containing numeric, non-negative, and non-zero
        values.

        Parameters
        ----------
        num : array_like
            Numerator for rate calculation. Must be a non-negative and
            non-zero numeric array.
        den : array_like
            Denominator for rate calculation. Must be a non-negative and
            non-zero numeric array.

        Raises
        ------
        TypeError
            If elements in `num` or `den` are not numeric.
        ValueError
            If values in `num` or `den` are not positive or if the sum
            of `num` or `den` is not greater than 0.
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
        """
        Calculate a basic rate.

        This method calculates a basic rate by dividing the sum of the numerator
        (`num`) by the sum of the denominator (`den`) and multiplying by a
        scaling `factor`.

        Parameters
        ----------
        num : array_like
            Numerator for rate calculation.
        den : array_like
            Denominator for rate calculation.
        factor : numeric, optional
            Factor to multiply the rate. If None, the default `feat_factor`
            attribute of the class is used. Must be positive.
            Default is None.

        Returns
        -------
        float
            The calculated basic rate.

        Raises
        ------
        ValueError
            If `factor` is not a positive numeric value (if provided).
        TypeError
            If elements in `num` or `den` are not numeric (raised by
            `_validate_input`).
        ValueError
            If values in `num` or `den` are not positive or if their sums are
            not greater than 0 (raised by `_validate_input`).
        """

        self._validate_input(num, den)
        
        factor_to_use = self._validate_factor(factor) if factor is not None else self.defeat_factor
        
        result = (np.sum(num) * factor_to_use) / np.sum(den)
        return result
    
    def frequency_rate(self, num_accidents, hours_worked, factor = None):
        """
        Calculate the frequency rate of work accidents.

        The frequency rate is calculated as the number of accidents per hours
        worked, multiplied by a scaling factor (typically 1,000,000).

        Parameters
        ----------
        num_accidents : array_like
            Number of accidents occurred.
        hours_worked : array_like
            Total hours worked by employees.
        factor : numeric, optional
            Factor to multiply the frequency rate. If None, a default factor
            of 1,000,000 is used. Must be positive. Default is None.

        Returns
        -------
        RateResult
            An object containing the calculated frequency rate and related
            information.

        Raises
        ------
        ValueError
            If `factor` is not a positive numeric value (if provided).
        TypeError
            If elements in `num_accidents` or `hours_worked` are not numeric
            (raised by `_validate_input`).
        ValueError
            If values in `num_accidents` or `hours_worked` are not positive
            or if their sums are not greater than 0 (raised by `_validate_input`).

        See Also
        --------
        basic_rate : Method to calculate a basic rate.
        RateResult : Class to store rate calculation results.

        Examples
        --------
        >>> rates_calculator = Rates()
        >>> accidents = np.array([5, 8, 12])
        >>> hours = np.array([100000, 120000, 150000])
        >>> freq_rate_result = rates_calculator.frequency_rate(accidents, hours)
        >>> print(freq_rate_result)
        67.57
        >>> print(freq_rate_result.rate_name)
        Frequency Rate
        >>> print(freq_rate_result.factor)
        1000000
        """
        
        factor_to_use = self._validate_factor(factor) if factor is not None else 10**6
        
        rate_value = self.basic_rate(num_accidents, hours_worked, factor_to_use)
        
        return RateResult(
            rate_name="Frequency Rate",
            rate_value=rate_value,
            factor=factor_to_use,
            num_unit="accidents",
            den_unit = "work hours"
        )
        

        
def display(rate_result):
    """
    Display the rate result in a formatted string.

    This function takes a `RateResult` object and prints a formatted string
    to the console, showing the rate name, value, units, and factor.

    Parameters
    ----------
    rate_result : RateResult
        An object of the `RateResult` class containing the rate calculation
        results.

    Raises
    ------
    TypeError
        If `rate_result` is not an instance of the `RateResult` class.

    Examples
    --------
    >>> rate_result = RateResult("Frequency Rate", 67.57, 1000000, "accidents", "work hours")
    >>> display(rate_result)
    Frequency Rate: 67.570 accidents per 1000000 work hours.
    """
    
    if not isinstance(rate_result, RateResult):
        raise TypeError("Display only works with RateResult class.")
    
    print(f"{rate_result.rate_name}: {rate_result.rate_value:.3f} {rate_result.num_unit} per {rate_result.factor} {rate_result.den_unit}.")


#wrapped functions  
def frequency_rate(num_accidents, hours_worked, factor = None):
    """
    Calculate the accident frequency rate (independent function).

    This function calculates the frequency rate of accidents based on the
    number of accidents and hours worked. It uses the `Rates` class internally
    to perform the calculation.

    Parameters
    ----------
    num_accidents : numeric or array_like
        Number of accidents occurred. Can be a single numeric value or an
        array-like object.
    hours_worked : numeric or array_like
        Total hours worked by employees. Can be a single numeric value or an
        array-like object.
    factor : numeric, optional
        Factor to multiply the frequency rate. If None, a default factor
        of 1,000,000 is used in the `Rates` class. Must be positive.
        Default is None.

    Returns
    -------
    RateResult
        An object of the `RateResult` class containing the calculated
        frequency rate and related information.

    See Also
    --------
    Rates : Class used to perform rate calculations.
    Rates.frequency_rate : Method within the `Rates` class that performs the
        frequency rate calculation.
    RateResult : Class to store rate calculation results.

    Examples
    --------
    >>> freq_rate_result = frequency_rate(15, 250000)
    >>> print(freq_rate_result)
    60.0
    >>> print(freq_rate_result.rate_name)
    Frequency Rate
    """
    
    calculator = Rates()
    return calculator.frequency_rate(num_accidents, hours_worked, factor)
    