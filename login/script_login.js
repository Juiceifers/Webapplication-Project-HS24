document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginSection = document.getElementById('login-section');
    const registerSection = document.getElementById('register-section');
    //const closeButton = document.getElementById('close-button');

    // Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            //fetch('http://http://127.0.0.0:5000/login', {
            fetch('http://http://172.23.66.241:5000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const userSession = { username: data.username };
                    localStorage.setItem('loggedInUser', JSON.stringify(userSession));
                    window.location.href = '/index.html';  // Redirect to index.html
                } else {
                    alert(data.message);  // Show message if login failed
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Handle register form submission
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const username = document.getElementById('registerUsername').value;
            const password = document.getElementById('registerPassword').value;

            fetch('http://127.0.0.1:5000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const userSession = { username: data.username };
                    localStorage.setItem('loggedInUser', JSON.stringify(userSession));
                    console.log("pre reroute to index")
                    window.location.href = '/index.html';  // Redirect to index.html on successful registration
                } else {
                    alert(data.message);  // Show the error message if registration fails
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Handle toggle between login and register sections
    const signupToggle = document.getElementById('signup-toggle');
    const loginToggle = document.getElementById('login-toggle');

    if (signupToggle) {
        signupToggle.addEventListener('click', function() {
            loginSection.style.display = 'none';
            registerSection.style.display = 'block';
        });
    }

    if (loginToggle) {
        loginToggle.addEventListener('click', function() {
            registerSection.style.display = 'none';
            loginSection.style.display = 'block';
        });
    }

    // Close button functionality
    const closeButton = document.getElementById('close-button');
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            window.close(); // Or any other functionality you want to implement
        });
    }
});
