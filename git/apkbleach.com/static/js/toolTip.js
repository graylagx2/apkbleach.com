// Variables for tooltip icon and tooltip message
var toolTip = document.getElementById("toolTip");
var toolTipMessage = document.getElementById("toolTipMessage");

// Detecting if the device is a touch screen or not
const is_touch_device = () => {
  return (
    "ontouchstart" in window || // works on most browsers
    "onmsgesturechange" in window
  ); // works on IE10 with some false positives
};

// Variable return value from touch screen detection function (true/false)
var isTouchDevice = is_touch_device();

// If device is touch screen
if (isTouchDevice) {
  var identifier;
  var isTouching = false;

  //   Since the device is a touch screen this is a event listener for when
  // touch starts
  toolTip.addEventListener(
    "touchstart",
    (event) => {
      // dismiss after-touches
      if (isTouching) {
        return;
      }
      event.preventDefault();
      // only care about the first touch
      var touch = event.changedTouches[0];
      identifier = touch.identifier;
      toolTipMessage.style.display = "block";
      window.addEventListener("touchend", onTouchEnd, false);
      isTouching = true;
    },
    false
  );

  const getTouch = (event) => {
    // cycle through every change touch and get one that matches
    for (var i = 0, len = event.changedTouches.length; i < len; i++) {
      var touch = event.changedTouches[i];
      if (touch.identifier === identifier) {
        return touch;
      }
    }
  };

  const onTouchEnd = (event) => {
    var touch = getTouch(event);
    if (!touch) {
      return;
    }
    toolTipMessage.style.display = "none";
    window.removeEventListener("touchend", onTouchEnd, false);
    isTouching = false;
  };
  // Since the device is not a touch screen
} else {
  toolTip.addEventListener(
    "click",
    () => {
      if (toolTipMessage.style.display == "none") {
        toolTipMessage.style.display = "block";
      } else {
        toolTipMessage.style.display = "none";
      }
    },
    false
  );
}
