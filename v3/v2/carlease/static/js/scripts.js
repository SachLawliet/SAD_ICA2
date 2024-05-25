// Prevent "Confirm Resubmission" pop up
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}
// --------------------------------------------!-------------------------------------------- //

// JS for "NEWS" section in welcome page
$(document).ready(function() {
    currentNewsIndex = 0;
    newsContainers = $('.news-container');

    $('#prevBtn').click(function() {
        newsContainers.eq(currentNewsIndex).removeClass('active');
        currentNewsIndex = (currentNewsIndex - 1 + newsContainers.length) % newsContainers.length;
        newsContainers.eq(currentNewsIndex).addClass('active');
    });

    $('#nextBtn').click(function() {
        newsContainers.eq(currentNewsIndex).removeClass('active');
        currentNewsIndex = (currentNewsIndex + 1) % newsContainers.length;
        newsContainers.eq(currentNewsIndex).addClass('active');
    });
});
// --------------------------------------------!-------------------------------------------- //

// JS for "PASSWORD REQUIREMENTS" in registration page
document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('examplePasswordInput1');
    const passwordRequirements = document.getElementById('passwordRequirements');
    const minLength = document.getElementById('minLength');
    const uppercase = document.getElementById('uppercase');
    const lowercase = document.getElementById('lowercase');
    const number = document.getElementById('number');
    const special = document.getElementById('symbol');

    // Initially hide the password requirements
    if (passwordRequirements) {
        passwordRequirements.style.display = 'none';
    } else {
        console.error('Element with id "passwordRequirements" not found.');
    }

    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const value = passwordInput.value;

            if (value.length > 0) {
                passwordRequirements.style.display = 'block';
            } else {
                passwordRequirements.style.display = 'none';
            }

            // Minimum length check
            if (value.length >= 8) {
                minLength.classList.remove('text-danger');
                minLength.classList.add('text-success');
            } else {
                minLength.classList.remove('text-success');
                minLength.classList.add('text-danger');
            }

            // Uppercase letter check
            if (/[A-Z]/.test(value)) {
                uppercase.classList.remove('text-danger');
                uppercase.classList.add('text-success');
            } else {
                uppercase.classList.remove('text-success');
                uppercase.classList.add('text-danger');
            }

            // Lowercase letter check
            if (/[a-z]/.test(value)) {
                lowercase.classList.remove('text-danger');
                lowercase.classList.add('text-success');
            } else {
                lowercase.classList.remove('text-success');
                lowercase.classList.add('text-danger');
            }

            // Number check
            if (/\d/.test(value)) {
                number.classList.remove('text-danger');
                number.classList.add('text-success');
            } else {
                number.classList.remove('text-success');
                number.classList.add('text-danger');
            }

            // Special character check
            if (/[!@#$%^&*(),.?":{}|<>]/.test(value)) {
                special.classList.remove('text-danger');
                special.classList.add('text-success');
            } else {
                special.classList.remove('text-success');
                special.classList.add('text-danger');
            }
        });
    } else {
        console.error('Element with id "examplePasswordInput1" not found.');
    }

    // Form submission handler
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(event) {
            const value = passwordInput.value;

            // Check if password meets requirements
            if (!(value.length >= 8 && /[A-Z]/.test(value) && /[a-z]/.test(value) && /\d/.test(value) && /[!@#$%^&*(),.?":{}|<>]/.test(value))) {
                // Prevent form submission
                event.preventDefault();
                
                // Display error message
                alert('Password does not meet requirements.');
            }
        });
    } else {
        console.error('Element with id "registrationForm" not found.');
    }
});
// --------------------------------------------!-------------------------------------------- //

// JS code for "ACCOUNT PAGE"
document.addEventListener('DOMContentLoaded', function() {
    const selectedSection = sessionStorage.getItem('selectedSection');
    if (selectedSection) {
        loadContent(selectedSection);
    } else {
        loadContent('/verification');
    }
});

function loadContent(page) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("main-content").innerHTML = this.responseText;
            sessionStorage.setItem('selectedSection', page);
        }
    };
    xhttp.open("GET", page, true);
    xhttp.send();
    return false;
}

document.getElementById('phone').addEventListener('input', function() {
    const phoneInput = this.value;
    const phoneFeedback = document.getElementById('phoneFeedback');
    const phoneRegex = /^\+?[1-9]\d{1,14}$/;
        
    if (!phoneRegex.test(phoneInput)) {
        this.classList.add('is-invalid');
        phoneFeedback.style.display = 'block';
    } else {
        this.classList.remove('is-invalid');
        phoneFeedback.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', (event) => {
    const notificationsForm = document.getElementById('notificationsForm');
    notificationsForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(notificationsForm);
        fetch('/notifications', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById('main-content').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
    });
});
