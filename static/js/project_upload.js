const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileElem");
const preview = document.getElementById("preview");

dropArea.addEventListener("click", () => fileInput.click());

["dragenter", "dragover"].forEach(eventName => {
    dropArea.addEventListener(eventName, e => {
        e.preventDefault();
        dropArea.classList.add("highlight");
    });
});

["dragleave", "drop"].forEach(eventName => {
    dropArea.addEventListener(eventName, e => {
        e.preventDefault();
        dropArea.classList.remove("highlight");
    });
});

dropArea.addEventListener("drop", e => {
    const files = e.dataTransfer.files;
    fileInput.files = files;
    showPreview(files);
});

fileInput.addEventListener("change", () => {
    showPreview(fileInput.files);
});

function showPreview(files) {
    preview.innerHTML = "";
    [...files].forEach(file => {
        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.style.width = "120px";
        img.style.margin = "10px";
        preview.appendChild(img);
    });
}

function saveDraft(){
  document.getElementById("is_draft").value = "true";
  document.querySelector("form").submit();
}

const tagsInput = document.getElementById("tagsInput");
const error = document.getElementById("tagError");
const existingTags = ["ui design", "mobile app", "minimalist"];
tagsInput.addEventListener("blur", () => {
  const value = tagsInput.value.trim().toLowerCase();
  if (value.length < 3 || existingTags.includes(value)) {
    error.style.display = "block";
  } else {
    error.style.display = "none";
  }
});

if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}

window.addEventListener("pageshow", function (event) {
  if (event.persisted) {
    document.querySelector("form").reset();
    preview.innerHTML = "";
  }
});