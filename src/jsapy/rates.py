def basic_rate(num, den, factor):
    """This function is for internal use to calculate some rates.

    Args:
        num (_type_): _description_
        den (_type_): _description_
        factor (_type_): _description_

    Returns:
        _type_: _description_
    """
    result = (sum(num) * factor) / sum(den)
    return result