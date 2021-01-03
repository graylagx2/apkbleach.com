// Variables for the checkbox event listener
var permissionsCheckBox = document.getElementById("edit-permissions");
var permissionsForm = document.getElementById("permissionsForm");

// Event listener for checkbox change
permissionsCheckBox.addEventListener("change", () => {
  if (permissionsCheckBox.checked == true) {
    permissionsForm.style.display = "block";
  } else {
    permissionsForm.style.display = "none";
  }
});
