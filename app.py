from flask import Flask, request
import base64, io

app = Flask(__name__)

# TODO this should go into its own file(s) and become extensible
ALLOWED_OPERATIONS = ["resize"]

def resize(original_image, width=None, height=None):
    """Resize the image to the provided dimensions
    
    If both width and height are given, the image will be resized 
    regardless of aspect ratio.
    If either width or height are given, the image will be scaled to 
    that dimension and aspect ratio will be maintained.
    If the given dimension(s) are bigger tham the original image, or 
    neither width nor heigth are provided, the original image will be 
    returned without resizing.
    """

@app.route("/image-process", methods=["POST"])
def image_process():
    payload = request.json
    operations = payload["operations"]
    original_image_decoded = base64.b64decode(payload["original_image"])
    # Load the bytes of the decoded image directly into memory, without 
    # creating a temporary file.
    image = io.BytesIO(original_image_decoded)
    # for operation in operations:
        
    procsessed_image_encoded = base64.b64encode(image.read()).decode()
    image.close()
    return {
        "processed_image": procsessed_image_encoded
    }