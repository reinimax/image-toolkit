from typing import Tuple
from enum import Enum, auto

class Unit(Enum):
    PERCENT = auto()
    PIXELS = auto()

def parse_dimension(str: str|int) -> Tuple[int, str]:
    """Parse a string representing an image dimension into value and unit.
    
    The first part of the string must be numeric, and the latter part must 
    be a unit of either pixels ("px") oder percent ("%").
    Returns a tuple of (value, unit). If the string could not be parsed, a 
    value of -1 will be returned.
    """
    # If the string is numeric, we can assume pixels and immediately return.
    if isinstance(str, int):
        return (str, Unit.PIXELS)
    if isinstance(str, float):
        return (int(str), Unit.PIXELS)
    if str.endswith("%"):
        unit = Unit.PERCENT
    # If no percent was given, assume pixels.
    else:
        unit = Unit.PIXELS
    try:
        # Neat trick to remove all non-digits from string.
        # See https://www.tutorialspoint.com/How-to-remove-characters-except-digits-from-string-in-Python
        value = int("".join(i for i in str if i.isdigit()))
    except ValueError:
        value = -1
    return (value, unit)
