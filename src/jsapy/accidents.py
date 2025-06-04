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
        return str(np.round(self.rate_value,3))

    def to_display(self):
        if self.rate_name == "Safety Rate":
            text = [f"{self.rate_name}: {self.rate_value:.3f} {self.num_unit} per each accident and {self.factor} {self.den_unit}."]
        else:
            text = [f"{self.rate_name}: {self.rate_value:.3f} {self.num_unit} per {self.factor} {self.den_unit}."]
            
        return "\n".join(text)
            
    def to_dict(self):
        """
        Return the attributes of the RateResult as a dictionary.

        Returns
        -------
        dict
            Dictionary representation of the rate result.
        """
        return {
            "rate_name": self.rate_name,
            "rate_value": self.rate_value,
            "factor": self.factor,
            "numerator_unit": self.num_unit,
            "denominator_unit": self.den_unit
        }

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
        num_accidents : numeric or array_like
            Number of work-related accidents.
        hours_worked : numeric or array_like
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
        >>> from jsapy.accidents import FrequencyRate()
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
        factor_to_use = super()._validate_factor(factor) if factor is not None else 10**6
        
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
        num_accidents : numeric or array_like
            Number of work-related accidents.
        num_workers : numeric or array_like
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
        >>> from jsapy.accidents import IncidenceRate()
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
        factor_to_use = super()._validate_factor(factor) if factor is not None else 10**5
        
        rate_value = super().calculate(num_accidents, num_workers, factor_to_use)
        
        return RateResult(
            rate_name="Incidence Rate",
            rate_value=rate_value,
            factor=factor_to_use,
            num_unit="accidents",
            den_unit="number of workers"
        )
   
class SeverityRate(Rates):    
    """
    Class for calculating the severity rate of work accidents.

    Methods
    -------
    calculate(days_lost, hours_worked, factor=None)
        Computes the severity rate given the number of lost work days and number of 
        hours worked, using a default factor of 100,000 if not specified.

    See Also
    --------
    Rates : Base class for general rate calculations.
    RateResult : Class to store and format the calculated rate.
    """
    def calculate(self, days_lost, hours_worked, factor=None):
        """
        Calculate the severity rate of work accidents.

        The severity rate is calculated as the the number of lost work days per total number of hours worked in the reference group and period, multiplied by a scaling factor (default: 100,000).

        Parameters
        ----------
        days_lost : numeric or array_like
            Number of work-related accidents.
        hours_worked : numeric or array_like
            Total hours worked by employees.
        factor : numeric, optional
            Factor to multiply the severity rate. If None, a default factor 
            of 100,000 is used. Must be positive. Default is None.

        Returns
        -------
        RateResult
            An object containing the calculated severity rate and related 
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
        >>> from jsapy.accidents import SeverityRate()
        >>> severity_rate_calculator = SeverityRate()
        >>> lost_days = np.array([5, 10, 15])
        >>> total_hours = np.array([10000, 20000, 30000])
        >>> severity_rate_result = severity_rate_calculator.calculate(lost_days, total_hours)
        >>> display(severity_rate_result)
        Severity Rate: 50.00 work days lost per 100000 work hours.
        >>> print(severity_rate_result.rate_name)
        Severity Rate
        >>> print(severity_rate_result)
        100000
        >>> severity_rate_result_custom_factor = severity_rate_calculator.calculate(lost_days, total_hours, factor=1000)
        >>> display(severity_rate_result_custom_factor)
        Severity Rate: 0.50 work days lost per 1000 work hours.
        """
        
        factor_to_use = super()._validate_factor(factor) if factor is not None else 10**5
        
        rate_value = super().calculate(days_lost, hours_worked, factor_to_use)
        
        return RateResult(
            rate_name="Severity Rate",
            rate_value=rate_value,
            factor=factor_to_use,
            num_unit="work days lost",
            den_unit="work hours"
        )
        
class LostDaysRate(Rates):
    """
    Class for calculating the lost days rate in work accident analysis.

    This rate is computed by combining the severity and frequency rates of work accidents,
    offering a standardized metric to evaluate the average number of lost days per accident.

    Methods
    -------
    calculate(num_accidents, hours_worked, days_lost)
        Calculates the lost days rate using number of accidents, hours worked,
        and days lost due to work-related incidents.

    See Also
    --------
    Rates : Base class for general rate calculations.
    RateResult : Class to store and format the calculated rate.
    """
    def calculate(self, num_accidents, hours_worked, days_lost):
        """
        Calculate the lost days rate of work accidents.

        This metric represents the average number of work days lost per accident, adjusted
        based on standard frequency and severity factors. It is derived by dividing the
        severity rate (days lost per 1,000 hours) by the frequency rate (accidents per 
        1,000,000 hours), scaled appropriately.

        Parameters
        ----------
        num_accidents : numeric or array_like
            Number of work-related accidents.
        hours_worked : numeric or array_like
            Total number of hours worked by employees in the reference period.
        days_lost : numeric or array_like
            Total number of work days lost due to accidents.

        Returns
        -------
        RateResult
            An object containing the calculated lost days rate and relevant metadata.

        Raises
        ------
        TypeError
            If inputs are not numeric or array_like (raised by `_validate_input` in base class).
        ValueError
            If input values are negative or their total sums are not greater than zero
            (raised by `_validate_input` in base class).

        See Also
        --------
        Rates.calculate : Base method to compute a generic rate.
        RateResult : Container class for results of rate calculations.

        Examples
        --------
        >>> from jsapy.accidents import LostDaysRate()
        >>> lost_days_rate_calculator = LostDaysRate()
        >>> accidents = [3, 2]
        >>> hours = [50000, 60000]
        >>> lost_days = [45, 30]
        >>> result = lost_days_rate_calculator.calculate(accidents, hours, lost_days)
        >>> display(result)
        Lost Days Rate: 15.000 work days lost per 1 accident.
        >>> print(result)
        15.0
        """
        
        factor_freq = 10**6
        factor_sev = 10**3
        
        freq_rate = super().calculate(num_accidents, hours_worked,  factor_freq)
        sev_rate = super().calculate(days_lost, hours_worked, factor_sev)
        
        rate_value = (sev_rate * 10**3) / freq_rate
        
        return RateResult(
            rate_name="Lost Days Rate",
            rate_value=rate_value,
            factor=1,
            num_unit="work days lost",
            den_unit = "accident"
        )
        
class SafetyRate(Rates):
    """
    Class for calculating the safety rate in workplace environments.

    The safety rate is a measure that relates the number of workers to the 
    number of accidents and hours worked, offering insights into operational 
    safety over a specific period.

    Methods
    -------
    calculate(num_accidents, num_workers, hours_worked, factor=None)
        Calculates the safety rate using the number of accidents, workers, 
        and hours worked, with an optional scaling factor.

    See Also
    --------
    Rates : Base class for general rate calculations.
    RateResult : Class to store and format the calculated rate.
    """
    def calculate(self, num_accidents, num_workers, hours_worked, factor=None):
        """
        Calculate the safety rate of work operations.

        The safety rate is calculated by first determining a normalized rate 
        of workers relative to accidents, scaled by a factor (default: 100,000), 
        and then adjusting by the total hours worked. It offers an understanding 
        of how the workforce size relates to accident occurrence over time.

        Parameters
        ----------
        num_accidents : numeric or array_like
            Number of recorded work-related accidents.
        num_workers : numeric or array_like
            Total number of workers affected by the risk.
        hours_worked : numeric or array_like
            Total number of hours worked by the employees.
        factor : numeric, optional
            Factor to scale the initial normalization between workers and 
            accidents. If None, a default factor of 100,000 is used. Must be positive.

        Returns
        -------
        RateResult
            An object containing the calculated safety rate and related information.

        Raises
        ------
        ValueError
            If `factor` is not a positive numeric value (if provided).
        TypeError
            If elements in `num_accidents`, `num_workers`, or `hours_worked` 
            are not numeric.
        ValueError
            If values in `num_accidents`, `num_workers`, or `hours_worked` are negative 
            or their sums are not greater than zero.

        See Also
        --------
        Rates.calculate : Base method for general rate computation.
        RateResult : Container for formatted rate calculation results.

        Examples
        --------
        >>> from jsapy.accidents import SafetyRate
        >>> safety_rate_calculator = SafetyRate()
        >>> accidents = [2, 3]
        >>> workers = [100, 150]
        >>> hours = [40000, 60000]
        >>> result = safety_rate_calculator.calculate(accidents, workers, hours)
        >>> display(result)
        Safety Rate: 50.000 workers per each accident and 100000 work hours.
        >>> print(result)
        50.0
        """
        factor_to_use = super()._validate_factor(factor) if factor is not None else 10**5
        
        num_rate = super().calculate(num_workers, num_accidents, factor_to_use)
        super()._validate_input(num_rate, hours_worked)
        den = np.sum(hours_worked)
        
        rate_value = num_rate / den
        
        return RateResult(
            rate_name="Safety Rate",
            rate_value=rate_value,
            factor=factor_to_use,
            num_unit="workers",
            den_unit="work hours"
        )
        
   
        
        