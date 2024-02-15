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
PIL.Image.Image as its first parameter, which will always be automatically 
passed to the function.
"""

from PIL import Image
from helpers import parse_dimension

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
    width, unit = parse_dimension(width)
    # Get original image dimensions
    orig_w, orig_h = image.size
    # Calculate by how much the image scales down
    scale = width / orig_w
    # Scale the not-provided dimension accordingly
    height = int(orig_h * scale)

    return image.resize((width, height))


ALLOWED_OPERATIONS = {
    "resize": resize
}
"""@private"""
