document.addEventListener("DOMContentLoaded", function () {
  const cookieNotice = document.getElementById("cookie-notice");
  const acceptButton = document.getElementById("accept-cookies");

  if (localStorage.getItem("cookiesAccepted")) {
    cookieNotice.style.display = "none";
  }

  function acceptCookies() {
    localStorage.setItem("cookiesAccepted", true);
    cookieNotice.classList.add("notice-hidden");
    setTimeout(() => {
      cookieNotice.style.display = "none";
    }, 500);
  }

  acceptButton.addEventListener("click", acceptCookies);
});

// Theme stuff (it was fun)

function applyTheme(theme) {
  document.documentElement.classList.toggle("light-theme", theme === "light");
}

function getSystemTheme() {
  return window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: light)").matches
    ? "light"
    : "dark";
}

function setButtonIcon(theme) {
  const button = document.getElementById("theme-toggle");
  button.innerHTML =
    theme === "light" ? "light_mode" : theme === "dark" ? "dark_mode" : "sync";
}

function toggleTheme() {
  let currentTheme = localStorage.getItem("theme");
  let newTheme;
  if (currentTheme === "light") {
    newTheme = "dark";
  } else if (currentTheme === "dark") {
    newTheme = null; // System default
  } else {
    newTheme = "light";
  }

  if (newTheme) {
    localStorage.setItem("theme", newTheme);
  } else {
    localStorage.removeItem("theme");
  }

  applyTheme(newTheme || getSystemTheme());
  setButtonIcon(newTheme);
}

(function () {
  let savedTheme = localStorage.getItem("theme");
  applyTheme(savedTheme ? savedTheme : getSystemTheme());
  setButtonIcon(savedTheme);

  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", (e) => {
      if (!localStorage.getItem("theme")) {
        applyTheme(e.matches ? "dark" : "light");
      }
    });
})();

/*  
    This makes NO sense??
    This is why i hate javascript, only the first one applies unless i use this weird timeout.
    x~x
*/
const toggleNavbarClass = () => {
  const atTop = window.scrollY === 0;
  setTimeout(
    () => document.querySelector(".btn-bar").classList.toggle("at-top", atTop),
    0
  );
  setTimeout(
    () => document.querySelector(".navbar").classList.toggle("at-top", atTop),
    0
  );
};

window.addEventListener("scroll", toggleNavbarClass);
