document.addEventListener("DOMContentLoaded", function () {
    var cookiePopup = document.getElementById('cookie-popup');
    var acceptCookiesBtn = document.getElementById('accept-cookies');
    var rejectCookiesBtn = document.getElementById('reject-cookies');
    var managePreferencesBtn = document.getElementById('manage-preferences');

    // Load saved cookie preferences from local storage
    var savedPreferences = JSON.parse(localStorage.getItem('cookiePreferences')) || {};

    // Event listener for accepting cookies
    acceptCookiesBtn.addEventListener('click', function () {
        setCookiePreferences(true);
        cookiePopup.style.display = 'none'; // Hide the popup after accepting cookies
    });

    // Event listener for rejecting cookies
    rejectCookiesBtn.addEventListener('click', function () {
        setCookiePreferences(false);
        cookiePopup.style.display = 'none'; // Hide the popup after rejecting cookies
    });

    // Event listener for managing cookie preferences
    managePreferencesBtn.addEventListener('click', function () {
        // Show preferences management interface (e.g., checkboxes)
        // Example:
        var cookieContent = document.querySelector('.cookie-content');
        cookieContent.innerHTML = `
            <p>Manage your cookie preferences:</p>
            <div id="cookie-options">
                <label><input type="checkbox" name="analytics-cookies" ${savedPreferences['analytics-cookies'] ? 'checked' : ''}> Analytics Cookies</label><br>
                <label><input type="checkbox" name="advertising-cookies" ${savedPreferences['advertising-cookies'] ? 'checked' : ''}> Advertising Cookies</label><br>
                <!-- Add more checkboxes for different types of cookies -->
            </div>
            <div class="cookie-buttons">
                <button id="save-preferences">Save Preferences</button>
            </div>
        `;

        // Event listener for saving cookie preferences
        var savePreferencesBtn = document.getElementById('save-preferences');
        savePreferencesBtn.addEventListener('click', function () {
            var preferences = {};
            var cookieOptions = document.querySelectorAll('#cookie-options input[type="checkbox"]');
            cookieOptions.forEach(function (checkbox) {
                preferences[checkbox.getAttribute('name')] = checkbox.checked;
            });
            localStorage.setItem('cookiePreferences', JSON.stringify(preferences));
            cookiePopup.style.display = 'none'; // Hide the popup after saving preferences
        });
    });

    // Function to set cookie preferences (accept or reject)
    function setCookiePreferences(accept) {
        var preferences = {};
        preferences['analytics-cookies'] = accept;
        preferences['advertising-cookies'] = accept;
        // Add more cookie types as needed
        localStorage.setItem('cookiePreferences', JSON.stringify(preferences));
    }
});

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

mapboxgl.accessToken = 'pk.eyJ1IjoidGdsYXp6IiwiYSI6ImNsZjZ0aGo4ZzFxMGUzb3IwcmloZHYzZWgifQ.sfSpvq6ZevT5lUO45bZf5w';

let loc = [14.432920703901994, 50.08725860834356];

var map = new mapboxgl.Map({
    container: 'map',
    center: loc,
    zoom: 14,
    style: 'mapbox://styles/tglazz/clhg9sguk01c001qyhwwi8xy0'
});

map.scrollZoom.disable();
map.addControl(new mapboxgl.NavigationControl());

let marker = document.createElement('div');
marker.id = 'marker';

let popup = new mapboxgl.Popup({ offset: 70 })
    .setHTML('<div id="hello">Prague City University</div>');

new mapboxgl.Marker(marker, { anchor: 'bottom' })
    .setLngLat(loc)
    .addTo(map)
    .setPopup(popup);

