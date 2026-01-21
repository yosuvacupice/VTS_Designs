const dropArea = document.getElementById("edit-drop-area");
const fileInput = document.getElementById("editFileInput");
const oldImages = document.getElementById("oldImages");
const newPreview = document.getElementById("newPreview");
dropArea.addEventListener("click", () => {
  fileInput.click();
});
fileInput.addEventListener("change", () => {
  if (oldImages) {
    oldImages.style.display = "none";
  }
  newPreview.innerHTML = "";
  Array.from(fileInput.files).forEach(file => {
    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    img.classList.add("preview-img");
    newPreview.appendChild(img);
  });
});
