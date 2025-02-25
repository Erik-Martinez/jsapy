from .accidents import RateResult

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
