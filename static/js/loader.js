// Home page loader is in generateFrom.js

// Variables for submit button event listener
var SubmitBtnElement = document.getElementById("submit-main");

// Contract data button press event listener
SubmitBtnElement.addEventListener("click", () => {
  document.getElementById("loader").style.display = "block";

  // Event listener to wait for page to finish loading
  window.addEventListener(
    "load",
    () => {
      document.getElementById("loader").style.display = "none";
    },
    false
  );
});
