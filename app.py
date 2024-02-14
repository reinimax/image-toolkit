from flask import Flask, request
import base64, io
from PIL import Image

app = Flask(__name__)

# TODO move this helper
def parse_dimension(str):
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


def resize(image, width=None, height=None):
    """Resize the image to the provided dimensions
    
    If both width and height are given, the image will be resized 
    regardless of aspect ratio.
    If either width or height are given, the image will be scaled to 
    that dimension and aspect ratio will be maintained.
    If the given dimension(s) are bigger tham the original image, or 
    neither width nor heigth are provided, the original image will be 
    returned without resizing.
    """
    width, unit = parse_dimension(width)
    # Get original image dimensions
    orig_w, orig_h = image.size
    # Calculate by how much the image scales down
    scale = width / orig_w
    # Scale the not-provided dimension accordingly
    height = int(orig_h * scale)

    return image.resize((width, height))


# TODO this should go into its own file(s) and become extensible
ALLOWED_OPERATIONS = {
    "resize": resize
}

@app.route("/image-process", methods=["POST"])
def image_process():
    payload = request.json
    operations = payload["operations"]
    original_image_decoded = base64.b64decode(payload["original_image"])
    # Load the bytes of the decoded image directly into memory, without 
    # creating a temporary file.
    raw_image = io.BytesIO(original_image_decoded)
    processed_image = io.BytesIO()
    image = Image.open(raw_image)
    for operation in operations:
        if operation["name"].lower() in ALLOWED_OPERATIONS:
            image = ALLOWED_OPERATIONS[operation["name"]](image, operation["width"])
    image.save(processed_image, format="jpeg")
    width, height = image.size
    procsessed_image_encoded = base64.b64encode(processed_image.getvalue()).decode()
    raw_image.close()
    processed_image.close()
    return {
        "metadata": {
            "width": width,
            "height": height
        },
        "processed_image": procsessed_image_encoded
    }