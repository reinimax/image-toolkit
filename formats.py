"""
This file defines available formats for returning a processed image.
"""

from io import BytesIO
from PIL import Image

def webp(image:Image.Image, buffer:BytesIO, quality=80, lossless:bool=False):
    # TODO add validation
    image.save(buffer, format="webp", quality=quality, lossless=lossless)

ALLOWED_FORMATS = {
    "webp": webp
}
"""@private"""