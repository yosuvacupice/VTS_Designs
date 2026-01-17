const input = document.getElementById("searchInput");
const results = document.getElementById("searchResults");
let lastResults = [];
input.addEventListener("keyup", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        if (lastResults.length > 0) {
            window.location.href = `/projects/hire/${lastResults[0].id}/`;
        }
        return;
    }
    if (input.value.trim().length === 0) {
        results.style.display = "none";
        return;
    }
    fetch(`/search-users/?q=${input.value}`)
        .then(res => res.json())
        .then(data => {
            results.innerHTML = "";
            lastResults = data;
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