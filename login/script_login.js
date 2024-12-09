document.addEventListener("DOMContentLoaded", function () {
    const loginButton = document.querySelector("#login-section a.btn"); // Button in article div
    const loginSection = document.getElementById("login-section");
    const registerSection = document.getElementById("register-section");
    const closeButton = document.getElementById("close-button");

    // State tracking
    let isLoginMode = true; // Tracks whether the current mode is "Login" or "Sign Up"

    loginButton.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent default link behavior (e.g., page reload)

        // If in "Sign Up" mode and the "Login" button is clicked, do nothing
        if (!isLoginMode && loginButton.textContent === "Login") {
            return; // Exit early and do nothing
        }

        if (isLoginMode) {
            // Switch to "Sign Up" Mode
            loginSection.style.transform = "translateX(123%)"; // Slide out to the left
            registerSection.style.transform = "translateX(-81%)"; // Slide into view
            loginSection.style.backgroundColor = "rgba(180, 140, 10, 1)";
            registerSection.style.backgroundColor = "rgba(51, 133, 155, 0.01)";
            loginSection.style.backdropFilter = "blur(3.5px)";

            // Update texts for "Sign Up" Mode
            document.querySelector("#login-section h1").textContent = "New here?";
            document.querySelector("#login-section p").textContent = "Register to save all your maps!";
            loginButton.textContent = "Sign up";

            document.querySelector("#register-section h2").textContent = "Sign in";

            // Update form inputs in "aside"
            const form = document.querySelector("#register-section form");
            form.innerHTML = `
                <input type="text" placeholder="Username" />
                <input type="password" placeholder="Password" />
                <button type="submit">Login</button>
            `;

            // Set state
            isLoginMode = false;
        } else {
            // Switch back to "Login" Mode
            loginSection.style.transform = "translateX(0)"; // Slide back into view
            registerSection.style.transform = "translateX(0)"; // Slide out of view
            loginSection.style.backgroundColor = "rgb(194, 150, 6)";
            registerSection.style.backgroundColor = "rgba(51, 133, 155, 0.25)";
            loginSection.style.backdropFilter = "blur(3px)";

            // Update texts for "Login" Mode
            document.querySelector("#login-section h1").textContent = "Already Member?";
            document.querySelector("#login-section p").textContent = "Welcome back!";
            loginButton.textContent = "Login";

            document.querySelector("#register-section h2").textContent = "Create Account";

            // Update form inputs in "aside"
            const form = document.querySelector("#register-section form");
            form.innerHTML = `
                <input type="text" placeholder="Username" />
                <input type="password" placeholder="Password" />
                <button type="submit">Sign Up</button>
            `;

            // Set state
            isLoginMode = true;
        }
    });

    closeButton.addEventListener("click", function () {
        window.location.href = "../index.html";
    });
});
