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

