// Variable for the home button
var homeBtnElement = document.getElementById("home-btn");

// Event listener for home button click
homeBtnElement.addEventListener(
  "click",
  () => {
    window.location = "/";
  },
  false
);
