function removeDataUrlPrefix(str, mimeType) {
    return str.replace(`data:${mimeType};base64,`, "");
}

function addDataUrlPrefix(str, mimeType) {
    return `data:${mimeType};base64,` + str;
}

function previewImage(base64Str, mimeType) {
    const preview = document.querySelector("#image-preview");
    preview.src = addDataUrlPrefix(base64Str, mimeType);
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

document.addEventListener("DOMContentLoaded", e => {
    document.querySelector("#image-upload-form").addEventListener("submit", handleImageUpload)
});