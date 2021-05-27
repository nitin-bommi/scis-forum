var darkSwitch = document.getElementById("darkSwitch");
window.addEventListener("load", function () {
  if (darkSwitch) {
    initTheme();
    darkSwitch.addEventListener("change", function () {
      resetTheme();
    });
  }
});

function initTheme() {
  var darkThemeSelected =
    localStorage.getItem("darkSwitch") !== null &&
    localStorage.getItem("darkSwitch") === "dark";
  darkSwitch.checked = darkThemeSelected;
  darkThemeSelected
    ? document.body.setAttribute("data-theme", "dark")
    : document.body.removeAttribute("data-theme");
}

function resetTheme() {
  if (darkSwitch.checked) {
    document.body.setAttribute("data-theme", "dark");
    localStorage.setItem("darkSwitch", "dark");
  } else {
    document.body.removeAttribute("data-theme");
    localStorage.removeItem("darkSwitch");
  }
}




// $(window).ready(function () {
//   console.log("ready!");
//   console.log(localStorage.getItem('theme'));
//   if (localStorage.getItem('theme') == 'dark') {
//     $("body").addClass("dark");
//     $(".inner-switch").text("ON");
//     $("#theme-link").attr("href", "{{ url_for('static', filename='dark-mode.css') }}");
//   }
//   else {
//     $("body").removeClass("dark");
//     $(".inner-switch").text("OFF");
//     $("#theme-link").attr("href", "{{ url_for('static', filename='main.css') }}");
//   }
//   $(".inner-switch").on("click", function () {
//     if ($("body").hasClass("dark")) {
//       $("body").removeClass("dark");
//       $(".inner-switch").text("OFF");
//       localStorage.setItem('theme', 'light');
//       $("#theme-link").attr("href", "{{ url_for('static', filename='main.css') }}");
//     } else {
//       $("body").addClass("dark");
//       $(".inner-switch").text("ON");
//       localStorage.setItem('theme', 'dark');
//       $("#theme-link").attr("href", "{{ url_for('static', filename='dark-mode.css') }}");
//     }
//   });
// });

