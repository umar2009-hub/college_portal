  window.addEventListener("load", () => {
    const loader = document.getElementById("loader");
    const content = document.getElementById("content");

    loader.classList.add("fade-out");

    setTimeout(() => {
      loader.style.display = "none";
      content.style.display = "block";
    }, 1000); // matches fade-out duration
  });

