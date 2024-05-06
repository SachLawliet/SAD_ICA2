var passwordInput = document.getElementById("password");
var letter = document.getElementById("letter");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var special = document.getElementById("special");
var length = document.getElementById("length");

// When the user clicks on the password field, show the message box
passwordInput.onfocus = function () {
    document.getElementById("message").style.display = "block";
}


// When the user starts to type something inside the password field
passwordInput.onkeyup = function () {
    // Validate lowercase letters
    var lowerCaseLetters = /[a-z]/g;
    if (passwordInput.value.match(lowerCaseLetters)) {
        letter.classList.remove("invalid");
        letter.classList.add("valid");
    } else {
        letter.classList.remove("valid");
        letter.classList.add("invalid");
    }

    // Validate capital letters
    var upperCaseLetters = /[A-Z]/g;
    if (passwordInput.value.match(upperCaseLetters)) {
        capital.classList.remove("invalid");
        capital.classList.add("valid");
    } else {
        capital.classList.remove("valid");
        capital.classList.add("invalid");
    }

    // Validate numbers
    var numbers = /[0-9]/g;
    if (passwordInput.value.match(numbers)) {
        number.classList.remove("invalid");
        number.classList.add("valid");
    } else {
        number.classList.remove("valid");
        number.classList.add("invalid");
    }

    // Validate special symbols
    var specials = /(?=.*[-!@#$%^&*_])/;
    if (passwordInput.value.match(specials)) {
        special.classList.remove("invalid");
        special.classList.add("valid");
    } else {
        special.classList.remove("valid");
        special.classList.add("invalid");
    }

    // Validate length
    if (passwordInput.value.length >= 10) {
        length.classList.remove("invalid");
        length.classList.add("valid");
    } else {
        length.classList.remove("valid");
        length.classList.add("invalid");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const hamburger = document.getElementById('hamburger');
    const nav = document.getElementById('nav');
    const navLinks = document.querySelectorAll('#nav a');

    // Close the hamburger menu and set navbar height to 80px by default
    hamburger.classList.remove('x');
    nav.classList.remove('open');
    nav.style.height = "80px";

    // Function to hide all 'a' elements
    function hideNavLinks() {
        navLinks.forEach(link => {
            link.style.display = "none";
        });
    }

    // Function to show all 'a' elements
    function showNavLinks() {
        navLinks.forEach(link => {
            link.style.display = "block"; // You can set display property according to your CSS
        });
    }

    // Add event listener to toggle hamburger menu and navbar height
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('x');
        nav.classList.toggle('open');

        if (nav.classList.contains('open')) {
            nav.style.height = "100vh";
            showNavLinks(); // Show links when menu is opened
        } else {
            nav.style.height = "80px"; // Set default height
            hideNavLinks(); // Hide links when menu is closed
        }
    });
});

