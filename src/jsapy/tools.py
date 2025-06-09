from .accidents import RateResult

def display(result):
    """
    Display formatted output for result objects with a `to_display()` method.

    This function prints a human-readable representation of results from `RateResult`, `VibraResult`, and `NoiseResult`.
    It delegates the formatting to the object's `to_display()` method.

    Parameters
    ----------
    result : object
        An instance of a result class (e.g., `RateResult`, `VibraResult`, `NoiseResult`)
        that implements a callable method `to_display()`.

    Raises
    ------
    TypeError
        If the provided object does not implement a callable `to_display()` method.
    """
    
    if hasattr(result, "to_display") and callable(result.to_display):
        print(result.to_display())
    else:
        raise TypeError("Object does not implement a callable `to_display()` method.")
