from .accidents import RateResult

def display(result):
    """
    Displays formatted output for result objects RateResult, VibraResult
    """
    if hasattr(result, "to_display") and callable(result.to_display):
        print(result.to_display())
    else:
        raise TypeError("Object does not implement a callable `to_display()` method.")
