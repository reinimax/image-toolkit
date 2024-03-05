"""
This file defines available formats for returning a processed image. 
New functions added here will be automatically picked up when the 
function is added to the ALLOWED_FORMATS dictionary.

Function arguments will be automatically passed when the function is called, 
if they were given via the API. The keys provided in the `return_as` object must 
match the parameter names of the Python function. For example, giving this JSON 
to the API
```
"return_as": {
        "format": "webp",
        "quality": 20
    }
```
would result in this function call: `webp(image, buffer, quality=20)`.

Note that each function automatically gets an image object of class `PIL.Image.Image` 
and a buffer object of class `io.BytesIO` passed as the first two parameters. 
The image should be saved to this buffer.
"""

from io import BytesIO
from PIL import Image

def webp(image:Image.Image, buffer:BytesIO, quality=80, lossless:bool=False) -> None:
    """#Convert image to webp format.

    **Parameters:**
    - image (Image): PIL image object
    - buffer (BytesIO): Buffer to which the image is written
    - quality: Quality of the image. Shoulb be between 0 (lowest quality) and 100 (highest quality).
    If `lossless`is true, this will instead determine the speed of saving the image (0 = fastest, 100 = slowest).
    - lossless (bool): Whether to use lossless compression.
    """
    # If we get a string, try to convert to float
    if isinstance(quality, str):
        try:
            quality = float(quality)
        except:
            # If an invalid argument was provided, use the default instead.
            quality = 80
    # Make sure quality is within the supported range
    if quality < 0 or quality > 100:
        quality = 80
    if not isinstance(lossless, bool):
        lossless = False
    image.save(buffer, format="webp", quality=quality, lossless=lossless)


def jpeg(image:Image.Image, buffer:BytesIO, quality=75) -> None:
    """#Convert image to jpeg format.

    **Parameters:**
    - image (Image): PIL image object
    - buffer (BytesIO): Buffer to which the image is written
    - quality: Quality of the image. Shoulb be between 0 (lowest quality) and 95 (highest quality).
    """
    # If we get a string or float, convert to int. Pillow is picky and accepty only an int here.
    if isinstance(quality, str) or isinstance(quality, float):
        try:
            quality = int(quality)
        except:
            quality = 75
    # Make sure quality is within the supported range
    if quality < 0 or quality > 95:
        quality = 75
    image.save(buffer, format="jpeg", quality=quality)


ALLOWED_FORMATS = {
    "jpeg": jpeg,
    "webp": webp
}
"""@private"""
