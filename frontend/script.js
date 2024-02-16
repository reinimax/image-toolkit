function removeDataUrlPrefix(str, mimeType) {
    return str.replace(`data:${mimeType};base64,`, "");
}

function addDataUrlPrefix(str, mimeType) {
    return `data:${mimeType};base64,` + str;
}

function previewImage(base64Str, mimeType) {
    const preview = document.querySelector("#image-preview");
    preview.src = addDataUrlPrefix(base64Str, mimeType);
    // Save mime type for later.
    preview.dataset.mimeType = mimeType;
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

async function resize(e) {
    e.preventDefault();
    // Get formdata, see https://stackoverflow.com/a/66407161
    const formData = new FormData(e.target);
    const formProps = Object.fromEntries(formData);
    const size = formProps.size + formProps.unit
    const dimension = `${formProps.dimension}`;
    const operation = {
        "name": "resize",
    }
    operation[dimension] = size;
    const response = await makeRequest(operation);
    const mimeType = "image/" + response.metadata.format;
    previewImage(response.processed_image, mimeType);
}

document.addEventListener("DOMContentLoaded", e => {
    document.querySelector("#image-upload-form").addEventListener("submit", handleImageUpload)
    document.querySelector("#resize").addEventListener("submit", resize)
});