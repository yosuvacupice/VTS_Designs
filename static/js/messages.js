// ---------- TAB FILTER ----------
document.querySelectorAll(".tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(t =>
      t.classList.remove("active")
    );
    tab.classList.add("active");

    const type = tab.dataset.tab;

    document.querySelectorAll(".msg-row").forEach(row => {
      if (type === "new" && row.dataset.read === "1") {
        row.style.display = "none";
      } else {
        row.style.display = "flex";
      }
    });
  });
});

// ---------- MESSAGE PREVIEW ----------
document.querySelectorAll(".msg-row").forEach(row => {
  row.addEventListener("click", () => {
    const id = row.dataset.id;

    fetch(`/messages/${id}/?ajax=1`)
      .then(res => res.json())
      .then(data => {
        document.getElementById("message-preview").innerHTML = `
          <h3>${data.sender}</h3>
          <p>${data.text}</p>
          <small>${data.time}</small>
        `;

        row.classList.remove("unread");
        row.dataset.read = "1";
      });
  });
});
