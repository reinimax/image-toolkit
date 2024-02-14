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
