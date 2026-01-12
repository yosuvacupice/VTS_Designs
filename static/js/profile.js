let sectionCount = 0;

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("add-section-btn");

    if (btn) {
        btn.addEventListener("click", function () {
            sectionCount++;

            const container = document.getElementById("custom-sections");

            const div = document.createElement("div");
            div.style.marginTop = "20px";

            div.innerHTML = `
                <label>Custom Section Title</label>
                <input type="text" name="custom_title_${sectionCount}" placeholder="Enter title">

                <label>Description</label>
                <textarea name="custom_desc_${sectionCount}" rows="4"
                    placeholder="Enter description"></textarea>
            `;

            container.appendChild(div);
        });
    }
});
