"""
This file defines image manipulation operations that are callable via the API.
New functions added here will be automatically picked up when the function is 
added to the `ALLOWED_OPERATIONS` dictionary.

Function arguments will be automatically passed when the function is called, 
if they were given via the API. The keys provided in the `operations` object 
must match the parameter names of the Python function. For example, giving 
this JSON to the API
```
"operations": [
    {
        "name": "resize",
        "width": "300px"
    }
]
```
would result in this function call: `resize(image, width="300px")`.

Note that every image manipulation function must take an object of class 
`PIL.Image.Image` as its first parameter, which will always be automatically 
passed to the function.
"""

from PIL import Image
from helpers import Unit, parse_dimension

def resize(image:Image.Image, width:str=None, height:str=None):
    """#Resize the image to the provided dimensions
    
    **Parameters:**
    - image (Image): PIL image object
    - width (str): Width to which the image should be resized
    - height (str): Height to which the image should be resized

    **Description:**  
    If both width and height are given, the image will be resized 
    regardless of aspect ratio.  
    If either width or height are given, the image will be scaled to 
    that dimension and aspect ratio will be maintained.  
    If the given dimension(s) are bigger tham the original image, or 
    neither width nor heigth are provided, the original image will be 
    returned without resizing.

    **Returns**:
    PIL Image object
    """
    # If no dimensions were provided, return the original image.
    if not width and not height:
        return image
    
    # Get original image dimensions
    orig_w, orig_h = image.size

    if width:
        width, unit = parse_dimension(width)
        if unit == Unit.PERCENT:
            width = int(orig_w * width / 100)

    if height:
        height, unit = parse_dimension(height)
        if unit == Unit.PERCENT:
            height = int(orig_h * height / 100)

    # Scale the dimension that was not provided
    if not height:
        # Calculate by how much the image scales down
        scale = width / orig_w
        # Scale the height accordingly
        height = int(orig_h * scale)
    elif not width:
        scale = height / orig_h
        width = int(orig_w * scale)

    # Make sure the given dimensions are greater than 0 and don't exceed the original image.
    if width <= 0 or height <= 0 or width > orig_w or height > orig_h:
        return image
    
    return image.resize((width, height))


def rotate(image:Image.Image, degrees, expand:bool=True, clockwise:bool=False):
    """#Rotate the image by the provided degrees
    
    **Parameters:**
    - image (Image): PIL image object
    - degrees (int|float|str): Amount of degrees by which to rotate the image
    - expand (bool): Whether the image dimensions should expand so that the 
    resulting image contains all of the original image. If set to False, the 
    image will remain the same size and parts that would be "outside" the image 
    due to roation will be cut. For rotating by 90 and 270 degrees, leave this 
    setting set to True, since this will allow width and height of the image to 
    switch without producing a border
    - clockwise (bool): Set to True for clockwise rotation. Per default, rotation 
    is counter-clockwise

    **Description:**  
    Rotate the image counter-clockwise by the provided degrees.

    **Returns**:
    PIL Image object
    """
    # If we get a string, try to convert to float
    if isinstance(degrees, str):
        try:
            degrees = float(degrees)
        except:
            return image
    if not isinstance(clockwise, bool):
        clockwise = False
    if not isinstance(expand, bool):
        expand = False
    # Invert degrees if we rotate clockwise.
    degrees = -degrees if clockwise else degrees
    return image.rotate(degrees, expand=expand)


ALLOWED_OPERATIONS = {
    "resize": resize,
    "rotate": rotate
}
"""@private"""
