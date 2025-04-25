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
    defeat_factor : int
        Default factor used in rate calculations if a factor is not
        explicitly provided. Set to 1000.
    """
    
    def __init__(self):
        """
        Initialize a Rates object.

        Sets the default feature factor (`defeat_factor`) to 1000.
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
        
    def calculate(self, num, den, factor=None):
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
    
class FrequencyRate(Rates):
    """
    Class for calculating the frequency rate of work accidents.

    This class extends the `Rates` class to specifically calculate the frequency 
    rate, which measures the number of accidents per hours worked, scaled by a 
    default factor of 1,000,000 unless another factor is provided.

    Methods
    -------
    calculate(num_accidents, hours_worked, factor=None)
        Computes the frequency rate given the number of accidents and total hours 
        worked, using a default factor of 1,000,000 if not specified.

    See Also
    --------
    Rates : Base class for general rate calculations.
    RateResult : Class to store and format the calculated rate.
    """

    def calculate(self, num_accidents, hours_worked, factor=None):
        """
        Calculate the frequency rate of work accidents.

        The frequency rate is calculated as the number of accidents per hours
        worked, multiplied by a scaling factor (default: 1,000,000).

        Parameters
        ----------
        num_accidents : array_like
            Number of work-related accidents.
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
        Rates.calculate : Method to calculate a general rate.
        RateResult : Class to store rate calculation results.

        Examples
        --------
        >>> freq_rate_calculator = FrequencyRate()
        >>> accidents = np.array([3, 7, 10])
        >>> hours = np.array([50000, 120000, 200000])
        >>> freq_rate_result = freq_rate_calculator.calculate(accidents, hours)
        >>> print(freq_rate_result)
        Frequency Rate: 76.923 accidents per 1000000 work hours.
        >>> print(freq_rate_result.rate_name)
        Frequency Rate
        >>> print(freq_rate_result.factor)
        1000000
        """
        factor_to_use = self._validate_factor(factor) if factor is not None else 10**6
        
        rate_value = super().calculate(num_accidents, hours_worked, factor_to_use)
        
        return RateResult(
            rate_name="Frequency Rate",
            rate_value=rate_value,
            factor=factor_to_use,
            num_unit="accidents",
            den_unit = "work hours"
        )
          
          
class IncidenceRate(Rates):
    """
    Class for calculating the incidence rate of work accidents.

    This class extends the `Rates` base class to specifically calculate the incidence 
    rate, which measures the number of accidents per number of workers, scaled by a 
    default factor of 100,000 unless another factor is provided.

    Methods
    -------
    calculate(num_accidents, num_workers, factor=None)
        Computes the incidence rate given the number of accidents and number of 
        workers, using a default factor of 100,000 if not specified.

    See Also
    --------
    Rates : Base class for general rate calculations.
    RateResult : Class to store and format the calculated rate.
    """
    def calculate(self, num_accidents, num_workers, factor=None):
        """
        Calculate the incidence rate of work accidents.

        The incidence rate is calculated as the number of accidents per number 
        of workers in the reference group and period, multiplied by a scaling factor (default: 100,000).

        Parameters
        ----------
        num_accidents : array_like
            Number of work-related accidents.
        num_workers : array_like
            Number of workers exposed to risk.
        factor : numeric, optional
            Factor to multiply the incidence rate. If None, a default factor 
            of 100,000 is used. Must be positive. Default is None.

        Returns
        -------
        RateResult
            An object containing the calculated incidence rate and related 
            information.

        Raises
        ------
        ValueError
            If `factor` is not a positive numeric value (if provided).
        TypeError
            If elements in `num_accidents` or `num_workers` are not numeric 
            (raised by `_validate_input`).
        ValueError
            If values in `num_accidents` or `num_workers` are not positive 
            or if their sums are not greater than 0 (raised by `_validate_input`).

        See Also
        --------
        Rates.calculate : Method to calculate a general rate.
        RateResult : Class to store rate calculation results.

        Examples
        --------
        >>> inc_rate_calculator = IncidenceRate()
        >>> accidents = np.array([2, 4, 6])
        >>> workers = np.array([100, 200, 300])
        >>> inc_rate_result = inc_rate_calculator.calculate(accidents, workers)
        >>> print(inc_rate_result)
        Incidence Rate: 1333.33 accidents per 100000 number of workers.
        >>> print(inc_rate_result.rate_name)
        Incidence Rate
        >>> print(inc_rate_result.factor)
        100000
        """
        factor_to_use = self._validate_factor(factor) if factor is not None else 10**5
        
        rate_value = super().calculate(num_accidents, num_workers, factor_to_use)
        
        return RateResult(
            rate_name="Incidence Rate",
            rate_value=rate_value,
            factor=factor_to_use,
            num_unit="accidents",
            den_unit="number of workers"
        )
    
    