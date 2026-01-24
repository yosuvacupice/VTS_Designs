document.addEventListener("DOMContentLoaded", () => {

  document.querySelectorAll(".like-btn").forEach(btn => {
    btn.addEventListener("click", function () {
      const projectId = this.dataset.id;

      fetch(`/projects/like/${projectId}/`)
        .then(res => res.json())
        .then(data => {
          if (data.likes_count !== undefined) {
            document.getElementById(
              `like-count-${projectId}`
            ).innerText = data.likes_count;

            this.classList.toggle("active", data.liked);
          }
        });
    });
  });

  document.querySelectorAll(".appreciate-btn").forEach(btn => {
    btn.addEventListener("click", function () {
      const projectId = this.dataset.id;

      fetch(`/projects/appreciate/${projectId}/`)
        .then(res => res.json())
        .then(data => {
          if (data.appreciations_count !== undefined) {
            document.getElementById(
              `appreciate-count-${projectId}`
            ).innerText = data.appreciations_count;

            this.classList.toggle("active", data.appreciated);
          }
        });
    });
  });

});
