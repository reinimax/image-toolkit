from typing import Tuple

def parse_dimension(str: str) -> Tuple[int, str]:
    """Parse a string representing an image dimension into value and unit.
    
    The first part of the string must be numeric, and the latter part must 
    be a unit of either pixels ("px") oder percent ("%").
    Returns a tuple of (value, unit) or None if the string could not be parsed.
    """
    str = str.lower()
    if str.endswith("px"):
        # TODO make this an enum?
        unit = "px"
        value = int(str[:-2])
    return (value, unit)
