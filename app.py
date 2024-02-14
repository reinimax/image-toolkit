from flask import Flask, request
import base64, io
from PIL import Image
from typing import Tuple
from operations import ALLOWED_OPERATIONS

app = Flask(__name__)

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