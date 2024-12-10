document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginSection = document.getElementById('login-section');
    const registerSection = document.getElementById('register-section');
    const container = document.getElementById("container")
    //const closeButton = document.getElementById('close-button');

    const url_path = window.location.href;

    // Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            fetch('/login', {
            //fetch(url_path +'/login', {
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
                    //window.location.href = '/index.html';  // Redirect to index.html
                    window.location.href = '/';  // Redirect to index.html
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

            //fetch('http://127.0.0.1:5000/register', {
            fetch('/register', {
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
                    window.location.href = '/';  // Redirect to index.html on successful registration
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
            container.style.backgroundColor='rgba(180, 140, 10, 0.6)';
        });
    }

    if (loginToggle) {
        loginToggle.addEventListener('click', function() {
            registerSection.style.display = 'none';
            loginSection.style.display = 'block';
            container.style.backgroundColor='rgba(51, 133, 155, 0.60)';
        });
    }

    // Close button functionality
    const closeButton = document.getElementById('close-button');
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            window.location.uref = '/';
            window.close(); // Or window.history.back(); 
        });
    }
});
