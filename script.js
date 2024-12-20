document.addEventListener("DOMContentLoaded", function () {
  const button = document.querySelector(".btn-submit");

  // Button scale effect on hover
  button.addEventListener("mouseenter", () => {
    button.style.transform = "scale(1.05)";
  });

  button.addEventListener("mouseleave", () => {
    button.style.transform = "scale(1)";
  });

  // Smooth scroll to result section after form submission
  document.querySelector("form").addEventListener("submit", (event) => {
    event.preventDefault();
    setTimeout(() => {
      document.querySelector(".result-card").scrollIntoView({ behavior: "smooth" });
    }, 200);
  });
});
