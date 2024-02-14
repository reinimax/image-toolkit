# IMAGE TOOLKIT
#### Video Demo:  <URL HERE>
#### Description:
Image toolkit  is a service for basic image manipulation. It features a website where the user can upload an image for processing, as well as an API, powered by [Flask](https://flask.palletsprojects.com/).

##### Installation
1. Set up virtual environment: `python3 -m venv .venv`
2. Activate virtual environment: `. .venv/bin/activate`
3. Install dependencies: `python -m pip install -r requirements.txt`

Note: You can exit the virtual environment by typing `deactivate`. [Learn more about virtual environments and package installation](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

##### Run the service locally

Activate the virtual environment and type `flask run`.

##### (Self-) Host the service

tbd. Refer to [Flask's documentation for deploying to production](https://flask.palletsprojects.com/en/3.0.x/deploying/).

##### Usage

tbd

##### Design decisions
- I decided to create just one API-endpoint and make the user provide the wanted operations as JSON payload. This is more user-friendly, because it lets you chain operations together in one single request.
- I tried out autogenerating API documentation using [flaskapi](https://github.com/apiflask/apiflask) and the [OpenAPI spec](https://www.openapis.org/), which is awesome in principle, but didn't convince me in the context of this project.
There is only one API endpoint, which takes a lot of parameters. OpenAPI is great if you have a lot of small endpoints and methods, but that's not the case here. What I really needed was
to document the single image manipulation operations. At the end, I decided to use [pdoc](https://pdoc.dev/), an easy tu use library that generates pretty neat documentation.

##### Acknowledgements
- Huge thanks to [HuggingChat](https://huggingface.co/chat/) for providing suggestions and feeback regarding some initial design decisions ([link to the chat](https://hf.co/chat/r/Oqo8rfK))
and for help with debugging some stuff.

