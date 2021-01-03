// Constants for the payloadName warning
const payloadNameElement = document.getElementById("payload-name");
const payloadNameWarn = document.getElementById("payloadNameWarning");

// Constants  for the form validation actions
const forms = document.getElementsByClassName("needs-validation");
const loaderElement = document.getElementById("loader");
const messageElement = document.getElementById("messageSentFlash");
const followPopUp = document.getElementById("followPopUp");

// Event listener to warn user the payload name they chose may be incorrect
payloadNameElement.addEventListener(
  "input",
  (e) => {
    if (e.target.value.match(/^.+\.|_$/)) {
      payloadNameWarn.style.display = "block";
    } else {
      payloadNameWarn.style.display = "none";
    }
  },
  false
);

// Form validation for application and email submit and action to do
var validation = Array.prototype.filter.call(forms, (form) => {
  form.addEventListener(
    "submit",
    (e) => {
      if (form.checkValidity() === false) {
        e.preventDefault();
        e.stopPropagation();
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
