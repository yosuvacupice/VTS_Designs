const input = document.getElementById("searchInput");
const results = document.getElementById("searchResults");

input.addEventListener("keyup", () => {
    if (input.value.length === 0) {
        results.style.display = "none";
        return;
    }

    fetch(`/search-users/?q=${input.value}`)
        .then(res => res.json())
        .then(data => {
            results.innerHTML = "";
            data.forEach(user => {
                const div = document.createElement("div");
                div.innerText = user.username;
                div.onclick = () => {
                    window.location.href = `/projects/hire/${user.id}/`;
                };
                results.appendChild(div);
            });
            results.style.display = "block";
        });
});
