// Home page loader is in generateFrom.js

// Contract data submit button
var SubmitBtnElement = document.getElementById("submit-main");


// Contract data button press event listener
SubmitBtnElement.addEventListener(
  "click",
  () => {

    // Make the loader visible by setting the css of element to display block
    document.getElementById("loader").style.display = "block";

    // Event listener to wait for page to finish loading
    window.addEventListener(
      "load",
      () => {
        // Hide the loader element by setting css to display none
        document.getElementById("loader").style.display = "none";
      },
      false
    );

  }
)