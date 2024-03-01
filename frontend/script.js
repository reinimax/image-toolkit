function removeDataUrlPrefix(str, mimeType) {
    return str.replace(`data:${mimeType};base64,`, "");
}

function addDataUrlPrefix(str, mimeType) {
    return `data:${mimeType};base64,` + str;
}

async function updateImageViewLink(dataUrl, mimeType) {
    // Essentially, we need to convert the base64 data-url, because it is too long to open in a new tab.
    // There are multiple approaches, but using fetch to get to the blob, creating a File from it and 
    // a URL from the File seems to be the easiest and most concise.
    // @see https://stackoverflow.com/a/47497249
    response = await fetch(dataUrl);
    blob = await response.blob();
    const file = new File([blob], "File name",{ type: mimeType })
    document.querySelector("#image-view-btn").href = URL.createObjectURL(file);
}

function previewImage(base64Str, mimeType) {
    const preview = document.querySelector("#image-preview");
    const dataUrl = addDataUrlPrefix(base64Str, mimeType);
    preview.src = dataUrl;
    // Save mime type for later.
    preview.dataset.mimeType = mimeType;
    // Update the view and download links
    document.querySelector("#image-download-btn").href = dataUrl;
    updateImageViewLink(dataUrl, mimeType);
}

function handleImageUpload(e) {
    e.preventDefault();
    const image = e.currentTarget.querySelector('[name="original_image"]').files[0];
    const mimeType = image.type;
    const reader = new FileReader();
    reader.readAsDataURL(image)
    // When the file reader has loaded the image, it is accessible via the result property.
    // See https://developer.mozilla.org/en-US/docs/Web/API/FileReader#events for more related events.
    // TODO: handle progress/errors
    reader.addEventListener("load", e => {
        const dataUrl = reader.result;
        const base64Img = removeDataUrlPrefix(dataUrl, mimeType);
        previewImage(base64Img, mimeType);
    });
}

async function makeRequest(operation) {
    // Get the image from the preview
    const img = document.querySelector("#image-preview")
    const mimeType = img.dataset.mimeType
    const imgBase64 = removeDataUrlPrefix(img.src, mimeType)
    // Build the payload
    const payload = {
        "operations": [
            operation
        ],
        "original_image": imgBase64
    }
    // Actually make the request to the API
    // TODO change this to the real URL 
    const response = await fetch('http://127.0.0.1:5000/image-process', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload)
    });
    return await response.json();
}

async function resize(size, unit, dimension) {
    // Validate that size is a positive number
    const errorbox = document.querySelector("#resize-wrapper .form-error");
    if (size <= 1) {
        errorbox.textContent = "Size is required and must be positive number.";
    } else {
        errorbox.textContent = "";
    }

    const operation = {
        "name": "resize",
    }
    operation[dimension] = size + unit;
    const response = await makeRequest(operation);
    const mimeType = "image/" + response.metadata.format;
    previewImage(response.processed_image, mimeType);
}

async function rotate(degrees, expand, clockwise) {
    console.log(degrees);
    console.log(Boolean(expand));
    console.log(Boolean(clockwise));
}

function processImage(e) {
    e.preventDefault();

    // Validate if there is actually an image to submit
    const img = document.querySelector("#image-preview")
    const errorbox = document.querySelector("#image-upload-form .form-error");
    if (!img.src) {
        const errorbox = document.querySelector("#image-upload-form .form-error");
        errorbox.textContent = "You must first upload an image!";
    } 
    // If there is an image, get rid of any previously displayed error message.
    else {
        errorbox.textContent = "";
    }

    // Map of supported functions and their arguments
    const processingFunctions = {
        resize: {
            callback: resize,
            args: ["resize_size", "resize_unit", "resize_dimension"]
        },
        rotate: {
            callback: rotate,
            args: ["rotate_degrees", "rotate_expand", "rotate_clockwise"]
        }
    }

    // Get formdata, see https://stackoverflow.com/a/66407161
    const formData = new FormData(e.target);
    const formProps = Object.fromEntries(formData);
    
    for (functionName in processingFunctions) {
        if (formProps[functionName] && typeof processingFunctions[functionName]["callback"] === "function") {
            const args = [];
            for (arg of processingFunctions[functionName]["args"]) {
                args.push(formProps[arg]);
            }
            processingFunctions[functionName]["callback"](...args)
        }
    }
}

document.addEventListener("DOMContentLoaded", e => {
    document.querySelector("#image-upload-form").addEventListener("submit", handleImageUpload)
    document.querySelector("#image-process").addEventListener("submit", processImage)
});