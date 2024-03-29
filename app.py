from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import base64, io, binascii
from PIL import Image
from operations import ALLOWED_OPERATIONS
from formats import ALLOWED_FORMATS
from helpers import get_func_args

app = Flask(__name__)
CORS(app)

@app.route("/image-process", methods=["POST"])
def image_process():
    """Process the image using the requested operations and return the processed image."""
    payload = request.get_json()
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
    # Load the bytes of the decoded image directly into memory, without creating a temporary file.
    raw_image = io.BytesIO(original_image_decoded)
    try:
        image = Image.open(raw_image)
        # Remember image format
        image_format = image.format.lower()
    except:
        return {"error": "Unuspported image format."}
    # Perform image manipulation operations.
    for operation in operations:
        # Ignore keys that don't follow the format of a dict.
        if not isinstance(operation, dict):
            continue
        if operation.get("name", '').lower() in ALLOWED_OPERATIONS:
            # Get the function from the allowed operations dict.
            func = ALLOWED_OPERATIONS[operation["name"]]
            # Get a list of the arguments it takes.
            provided_args = get_func_args(func, operation, ["image"])
            # Call the requested function. If anything goes wrong, we just skip the operation.
            try:
                # Use the unpacking operator to pass the named arguments to the function from the dict.
                image = func(image, **provided_args)
            except:
                continue
    # Create a buffer in memory and save the processed image to it.
    processed_image = io.BytesIO()
    saving_options = payload.get("return_as")
    if saving_options and saving_options.get("format", "").lower() in ALLOWED_FORMATS:
        # Update image format
        image_format = saving_options.get("format", "").lower()
        func = ALLOWED_FORMATS[image_format]
        provided_args = get_func_args(func, saving_options, ["image", "buffer"])
        # Try to call the saving function. If something goes wrong, 
        # save the image instead without the provided args.
        try:
            func(image, processed_image, **provided_args)
        except:
            image.save(processed_image, format=image_format)
    else:
        image.save(processed_image, format=image_format)
    width, height = image.size
    procsessed_image_encoded = base64.b64encode(processed_image.getvalue()).decode()
    raw_image.close()
    processed_image.close()
    return {
        "metadata": {
            "format": image_format,
            "width": width,
            "height": height
        },
        "processed_image": procsessed_image_encoded
    }


# Taken from https://hf.co/chat/r/rQ-g0NB
# Define custom error handler for all exceptions, returning them as JSON instead of text/html.
@app.errorhandler(Exception)
def handle_exception(e):
    response = make_response(jsonify({"error": str(e)}))
    response.status_code = getattr(e, "code", 500)
    return response
