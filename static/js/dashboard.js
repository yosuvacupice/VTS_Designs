document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("dashboardUploadForm");
  const fileInput = document.getElementById("dashboardFileInput");
  const preview = document.getElementById("dashboardPreview");
  fileInput.addEventListener("change", () => {
    preview.innerHTML = "";
    [...fileInput.files].forEach(file => {
      if (file.size > 10 * 1024 * 1024) {
        alert("Image must be under 10MB");
        fileInput.value = "";
        return;
      }
      const img = document.createElement("img");
      img.src = URL.createObjectURL(file);
      img.style.width = "120px";
      img.style.margin = "10px";
      preview.appendChild(img);
    });
  });
  form.addEventListener("submit", function (e) {
    if (fileInput.files.length === 0) {
      e.preventDefault();
      alert("Please select at least one image");
    }
  });

});

function setDashboardAction(action){
  document.getElementById("dashboard_action").value = action;
}