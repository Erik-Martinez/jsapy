from jsapy.accidents import FrequencyRate, IncidenceRate, SeverityRate, LostDaysRate, SafetyRate

def frequency_rate(num_accidents, hours_worked, factor = None):
    """
    Calculate the accident frequency rate (independent function).
    
    The frequency rate represents the number of accidents per 1,000,000 hours worked
    by default, although a custom scaling factor can be provided.

    This function calculates the frequency rate of accidents based on the
    number of accidents and hours worked, using the `FrequencyRate` class for the calculation.

    Parameters
    ----------
    num_accidents : numeric or array_like
        Number of work-related accidents. Can be a single value or a list/array 
        of values.
    hours_worked : numeric or array_like
        Total hours worked by all employees. Can be a single numeric value or an
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
    FrequencyRate : Class used for calculating the frequency rate with extended control.
    RateResult : Class for storing and formatting rate calculation results.

    Examples
    --------
    >>> import jsapy as jsa
    >>> print(jsa.frequency_rate(15, 250000))
    60.0
    >>> jsa.display(jsa.frequency_rate([3, 7, 10], [50000, 120000, 200000]))
    Frequency Rate: 54.054 accidents per 1000000 work hours.
    """
    
    return FrequencyRate().calculate(num_accidents, hours_worked, factor)

def incidence_rate(num_accidents, num_workers, factor=None):
    """
    Calculate the accident incidence rate (independent function).

    The incidence rate represents the number of accidents per 100,000 workers
    by default, although a custom scaling factor can be provided.

    This function calculates the incidence rate of accidents based on the
    number of accidents and the number of workers, using the `IncidenceRate` 
    class for the calculation.

    Parameters
    ----------
    num_accidents : numeric or array_like
        Number of work-related accidents. Can be a single value or a list/array 
        of values.
    num_workers : numeric or array_like
        Number of workers. Can be a single numeric value or an array-like object.
    factor : numeric, optional
        Factor to multiply the incidence rate. If None, a default factor
        of 100,000 is used. Must be positive. Default is None.

    Returns
    -------
    RateResult
        An object of the `RateResult` class containing the calculated
        incidence rate, the scaling factor, and the associated units (accidents, workers).

    See Also
    --------
    IncidenceRate : Class used for calculating the incidence rate with extended control.
    RateResult : Class for storing and formatting rate calculation results.

    Examples
    --------
    >>> import jsapy as jsa
    >>> print(jsa.incidence_rate(15, 500))
    3000.0

    >>> jsa.display(jsa.incidence_rate([3, 7, 10], [100, 150, 200]))
    Incidence Rate: 4444.444 accidents per 100000 number of workers.
    """

    return IncidenceRate().calculate(num_accidents, num_workers, factor)

def severity_rate(days_lost, hours_worked, factor=None):
    """ 
    Calculate the severity rate of work accidents (independent function).

    The severity rate represents the number of work days lost due to accidents
    per 100,000 hours worked by default, although a custom scaling factor
    can be provided.

    This function calculates the severity rate based on the number of lost
    work days and the total number of hours worked, using the `SeverityRate`
    class for the calculation.

    Parameters
    ----------
    days_lost : numeric or array_like
        Total number of work days lost due to work-related accidents.
        Can be a single value or a list/array of values.
    hours_worked : numeric or array_like
        Total number of hours worked by all employees in the reference period.
        Can be a single numeric value or an array-like object.
    factor : numeric, optional
        Factor to multiply the severity rate. If None, a default factor
        of 100,000 is used. Must be positive. Default is None.

    Returns
    -------
    RateResult
        An object of the `RateResult` class containing the calculated
        severity rate, the scaling factor, and the associated units
        (work days lost, work hours).

    See Also
    --------
    SeverityRate : Class used for calculating the severity rate with extended control.
    RateResult : Class for storing and formatting rate calculation results.

    Examples
    --------    
    >>> import jsapy as jsa
    >>> print(jsa.severity_rate(20, 100000))
    20.0
    >>> jsa.display(jsa.severity_rate([5000, 10000, 20000], [50000, 120000, 200000]))
    Severity Rate: 9459.459 work days lost per 100000 work hours.
    """ 
    
    return SeverityRate().calculate(days_lost, hours_worked, factor)

def lost_days_rate(num_accidents, hours_worked, days_lost):
    """
    Calculate the lost days rate of work accidents (independent function).

    The lost days rate represents the average number of work days lost per accident,
    based on standardized severity and frequency scaling factors.
    It provides a concise metric to assess the impact of accidents in the workplace.

    This function internally uses the `LostDaysRate` class to perform the
    calculation with proper validation and scaling.

    Parameters
    ----------
    num_accidents : numeric or array_like
        Number of work-related accidents.
        Can be a single value or a list/array of values.
    hours_worked : numeric or array_like
        Total number of hours worked by employees during the reference period.
        Can be a single numeric value or an array-like object.
    days_lost : numeric or array_like
        Total number of work days lost due to accidents.
        Single value or array-like object.

    Returns
    -------
    RateResult
        An object of the `RateResult` class containing the calculated
        lost days rate, the associated factor (1), and the relevant units
        (work days lost per accident).

    See Also
    --------
    LostDaysRate : Class used for calculating the lost days rate with extended options.
    RateResult : Class for formatting and storing rate calculation results.

    Examples
    --------
    >>> import jsapy as jsa
    >>> print(jsa.lost_days_rate(5, 100000, 50))
    10.0
    >>> jsa.display(jsa.lost_days_rate([5, 10], [100000, 200000], [50, 120]))
    Lost Days Rate: 11.333 work days lost per 1 accident.
    """
    return LostDaysRate().calculate(num_accidents, hours_worked, days_lost)

def safety_rate(num_accidents, num_workers, hours_worked, factor=None):
    """
    Calculate the safety rate of work accidents (independent function).

    The safety rate represents the number of workers per total work hours,
    adjusted by a scaling factor (default: 100,000 work hours).
    It provides an indicator of workforce presence related to hours worked.

    This function uses the `SafetyRate` class internally to perform the
    calculation with proper input validation and scaling.

    Parameters
    ----------
    num_accidents : numeric or array_like
        Total number of work-related accidents.
        Can be a single value or a list/array of values.
    num_workers : numeric or array_like
        Total number of workers involved in the reference period.
        Can be a single numeric value or an array-like object.
    hours_worked : numeric or array_like
        Total number of hours worked during the reference period.
        Single value or array-like object.
    factor : numeric, optional
        Scaling factor to adjust the rate calculation. If None, a default
        factor of 100,000 is used. Must be a positive value. Default is None.

    Returns
    -------
    RateResult
        An object of the `RateResult` class containing the calculated
        safety rate, the scaling factor (equal to `hours_worked`),
        and associated units (workers per work hours).

    See Also
    --------
    SafetyRate : Class for calculating safety rate with advanced options.
    RateResult : Class to format and store the result of rate calculations.

    Examples
    --------
    >>> import jsapy as jsa
    >>> print(jsa.safety_rate(10, 500, 200000))
    25
    >>> jsa.display(jsa.safety_rate([10, 5], [500, 300], [200000, 150000]))
    Safety Rate: 15.238 workers per each accident and 100000 work hours.
    """
    return SafetyRate().calculate(num_accidents, num_workers, hours_worked, factor)