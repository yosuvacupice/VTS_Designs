let sectionCount = 0;
document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("add-section-btn");
  if (btn) {
    btn.addEventListener("click", function () {
      sectionCount++;
      const container = document.getElementById("custom-sections");
      const div = document.createElement("div");
      div.classList.add("custom_section");
      div.innerHTML = `
        <div class="form_group">
          <label>Custom Section Title</label>
          <input type="text" name="custom_title_${sectionCount}" placeholder="Enter title">
        </div>
        <div class="form_group">
          <label>Description</label>
          <textarea name="custom_desc_${sectionCount}" rows="4"
            placeholder="Enter description"></textarea>
        </div>
      `;
      container.appendChild(div);
    });
  }
});

function openLogoutPopup() {
  document.getElementById("logout-popup").style.display = "flex";
}

function closeLogoutPopup() {
  document.getElementById("logout-popup").style.display = "none";
}

function confirmLogout() {
  window.location.href = "/logout/";
}