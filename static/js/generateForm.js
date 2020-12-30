// Fetch all the forms we want to apply custom Bootstrap validation styles to
var forms = document.getElementsByClassName('needs-validation');

// Make the loader visible by setting the css of element to display block
var loaderElement = document.getElementById("loader");

// Contact us message element
var messageElement = document.getElementById("messageSentFlash");

var payloadNameElement = document.getElementById("payload-name");

var followPopUp = document.getElementById("followPopUp");

payloadNameElement.addEventListener(
  'input',
  (event) => {
    if (payloadNameElement.value.match(/^.+\.(apk)$/)) {
        document.getElementById("payloadNameWarning").style.display = "block";
    } else {
      document.getElementById("payloadNameWarning").style.display = "none";

    }

  }, false);

// Loop over them and prevent submission
var validation = Array.prototype.filter.call(forms, (form) => {
  form.addEventListener(
    'submit',
    (event) => {
      if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
        form.scrollIntoView();
      }
      form.classList.add('was-validated');

      if (form.checkValidity() === true) {
        messageElement.style.display = "block";

        if(form.id == 'generateForm'){
          loaderElement.scrollIntoView();
          loaderElement.style.display = "block";
          form.style.display = "none";
          followPopUp.style.display = "block";
        }

      }
    }, false);
  });

