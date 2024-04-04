const show = () => {
  let password = document.getElementById("password");
  let visibility = document.querySelector(".visibility");
  if (password.type === "password") {
    password.type = "text";
    visibility.style.color = "rgb(128, 0, 122)";
  } else {
    password.type = "password";
    visibility.style.color = "#fff";
  }
};
var el = document.getElementById("wrapper");
var toggleButton = document.getElementById("menu-toggle");

toggleButton.onclick = function () {
el.classList.toggle("toggled");
};