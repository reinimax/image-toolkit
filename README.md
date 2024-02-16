# IMAGE TOOLKIT
#### Video Demo:  <URL HERE>
## Description:
Image toolkit  is a service for basic image manipulation. It features a website where the user can upload an image for processing, as well as an API, powered by [Flask](https://flask.palletsprojects.com/).

### Installation
1. Set up virtual environment: `python3 -m venv .venv`
2. Activate virtual environment: `. .venv/bin/activate`
3. Install dependencies: `python -m pip install -r requirements.txt`

Note: You can exit the virtual environment by typing `deactivate`. [Learn more about virtual environments and package installation](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

### Run the service locally

Activate the virtual environment and type `flask run`.

### (Self-) Host the service

tbd. Refer to [Flask's documentation for deploying to production](https://flask.palletsprojects.com/en/3.0.x/deploying/).

### Usage

#### via the web-interface (upload form)
tbd

#### via the API
There is one API endpoint, `/image-process`, which expects a `POST` request with a `JSON` payload.

Except the obligatory `Content-Type: application/json`, no additional headers and no authentication are required.

The `JSON` payload has two mandatory fields:

- `original_image`: base64-encoded image.
- `operations`: array of objects that define the operations to be performed on the image. Operations will be performed in order. If an invalid operation is given,
or a valid operation fails, the other operations will still be performed.

An `operation` object itself consists of a mandatory `name` field which specifies the operation that should be performed. The name is the same as the name of the processing function
that will be called to do the work.

Optionally, each operation accepts arguments that specify how the image should be processed, e.g. a width and/or height for resizing an image. Dimensions like width or height can be given to the API in different ways: Generally, it will accept units of pixels and percent. If the unit is pixels, it can be omitted, since this is assumed as the standard. These would all be valid arguments:
```
"width": "300px"
"width": "300" // 300px, as above
"width": 300
"width": 300.0 // this works too, but is considered bad practice
"width": "50%" // 50 percent
```

A complete payload might look like this:
```
{
    "operations": [
        {
            "name": "rotate",
            "degrees": 180
        },
        {
            "name": "resize",
            "width": "50%",
        },
        // ... any other operations you like to perform.
    ],
    "original_image": "..." // base64-encoded image
}
```

##### API response

A successful response from the API will look like this:
```
{
    "metadata": {
        // width and height of the processed image
        "height": 374,
        "width": 300
    },
    "processed_image": "..." // base64-encoded image
}
```

If you get back the original image, or some operations were not performed, this probably means you provided invalid/incomplete parameters to some operation(s). If you found a bug, feel free to [open an issue](https://github.com/reinimax/image-toolkit/issues).

If you really messed up the `JSON` payload or did not provide a correctly encoded image, you will get an error response instead:
```
{
    "error": "No image provided." // The error message will try to explain what caused the error.
}
```
However, I tried to design this API pretty robust and forgiving, so (hopefully) what you'll see more often is just some operation not being performed if you forgot an argument or mistyped something.

You can look up the available processing functions and the arguments they expect in the [API documentation](/api/operations/) (ignore the `image` argument, as this will be passed in automatically).

##### Accepted file formats
tbd (refer to the [pillow documentation](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html))

### Design decisions
- I decided to create just one API-endpoint and make the user provide the wanted operations as JSON payload. This is more user-friendly, because it lets you chain operations together in one single request.
- I tried out autogenerating API documentation using [flaskapi](https://github.com/apiflask/apiflask) and the [OpenAPI spec](https://www.openapis.org/), which is awesome in principle, but didn't convince me in the context of this project.
There is only one API endpoint, which takes a lot of parameters. OpenAPI is great if you have a lot of small endpoints and methods, but that's not the case here. What I really needed was
to document the single image manipulation operations. At the end, I decided to use [pdoc](https://pdoc.dev/), an easy tu use library that generates pretty neat documentation and integrate it with [mkdocs](https://www.mkdocs.org/), linking this README file to the generated documentations index file using [pymdown-extensions](https://github.com/facelessuser/pymdown-extensions).

### Acknowledgements
- Huge thanks to [HuggingChat](https://huggingface.co/chat/) for providing suggestions and feeback regarding some initial design decisions ([link to the chat](https://hf.co/chat/r/Oqo8rfK))
and for help with debugging some stuff.
- This project would not have been possible without some amazing libraries. See below for a list of projects this project relies on.

### Powerd by
tbd list used libraries
