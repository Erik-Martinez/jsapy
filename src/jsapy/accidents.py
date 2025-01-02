import numpy as np

def basic_rate(num, den, factor):
    """This function is for internal use to calculate some rates."""
    
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