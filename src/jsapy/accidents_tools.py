from .accidents import Rates, FrequencyRate

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
    return FrequencyRate().calculate(num_accidents, hours_worked, factor)