// Variables for the payloadName warning
var payloadNameElement = document.getElementById("payload-name");

// Variables for the form validation actions
var forms = document.getElementsByClassName("needs-validation");
var loaderElement = document.getElementById("loader");
var messageElement = document.getElementById("messageSentFlash");
var followPopUp = document.getElementById("followPopUp");

// Event listener to warn user the payload name they chose may be incorrect
payloadNameElement.addEventListener(
  "input",
  () => {
    if (payloadNameElement.value.match(/^.+\.|_$/)) {
      document.getElementById("payloadNameWarning").style.display = "block";
    } else {
      document.getElementById("payloadNameWarning").style.display = "none";
    }
  },
  false
);

// Form validation for application and email submit and action to do
var validation = Array.prototype.filter.call(forms, (form) => {
  form.addEventListener(
    "submit",
    (event) => {
      if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
        form.scrollIntoView();
      }
      form.classList.add("was-validated");

      if (form.checkValidity() === true) {
        if (form.id == "contactUs") {
          messageElement.style.display = "block";
          messageElement.scrollIntoView({
            behavior: "smooth",
            block: "end",
            inline: "nearest",
          });
        }

        if (form.id == "generateForm") {
          loaderElement.scrollIntoView({
            behavior: "smooth",
            block: "start",
            inline: "nearest",
          });
          loaderElement.style.display = "block";
          form.style.display = "none";
          followPopUp.style.display = "block";
        }
      }
    },
    false
  );
});
