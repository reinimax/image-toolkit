from flask import Flask, request
import base64, io, binascii
from PIL import Image
from operations import ALLOWED_OPERATIONS

app = Flask(__name__)

@app.route("/image-process", methods=["POST"])
def image_process():
    """Process the image using the requested operations and return the processed image."""
    payload = request.json
    # Validate image
    original_image = payload.get("original_image")
    if not original_image:
        return {"error": "No image provided."}
    try:
        original_image_decoded = base64.b64decode(original_image)
    except binascii.Error:
        return {"error": "Image must be base64 encoded."}
    # Validate operations
    operations = payload.get("operations", [])
    if not isinstance(operations, list):
        return {"error": "Operations must be a list."}
    # Load the bytes of the decoded image directly into memory, without 
    # creating a temporary file.
    raw_image = io.BytesIO(original_image_decoded)
    processed_image = io.BytesIO()
    image = Image.open(raw_image)
    for operation in operations:
        if operation.get("name", '').lower() in ALLOWED_OPERATIONS:
            # TODO find a way to pass in the parameters the respective function needs.
            # Or pass in everything and let the function figure it out?
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