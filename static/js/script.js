document.addEventListener("DOMContentLoaded", function () {
    const mapNameInput = document.getElementById("mapName");
    const previousMapsList = document.getElementById("previousMapsList");
    const uploadFileInput = document.getElementById("uploadFile");
    const progressBar = document.getElementById("progressBar");
    const progressText = document.getElementById("progressText");
    const progressContainer = document.getElementById("progress-container");
    const uploadBox = document.getElementById("uploadBox");
    const mapNameForm = document.getElementById("mapNameForm");
    const processButton = document.getElementById("processBtn");
    const createMapHeader = document.querySelector("main h2");
    const resultsContainer = document.getElementById("results-container");
    const plusButton = document.getElementById("plusButton");
    const mapNameHeading = document.createElement("h2");
    mapNameHeading.id = "mapNameHeading";
    mapNameHeading.style.display = "none";
    resultsContainer.prepend(mapNameHeading);

    // User Profile Handling
    const userProfile = document.querySelector('.userProfile');
    const userName = document.getElementById("user-name");
    const loginRegisterLink = document.getElementById("login-register");
    const logoutLink = document.createElement('a');

    // Check if the user is logged in from localStorage
    const loggedInUser = localStorage.getItem("loggedInUser");
    

    // Clear previous sessions when the page is loaded
    localStorage.removeItem("sessions");
    let sessions = [];

    // Function to reset the upload form
    function resetToUploadForm() {
        createMapHeader.style.display = "block";
        uploadBox.style.display = "block";
        mapNameForm.style.display = "block";
        processButton.style.display = "block";
        resultsContainer.innerHTML = "";
        progressContainer.style.display = "none";
        clearActiveHighlight(); // Clear any active highlights
    }

    // Clear active highlights
    function clearActiveHighlight() {
        const activeItem = previousMapsList.querySelector(".highlight");
        if (activeItem) {
            activeItem.classList.remove("highlight");
        }
    }

    // When the pink plus button is clicked
    plusButton.addEventListener("click", function () {
        resetToUploadForm();
    });

    // When the "Do the magic!" button is clicked
    processButton.addEventListener("click", function () {
        const mapName = mapNameInput.value.trim();
        if (mapName === "" || / /.test(mapName)) {
            alert("Please Enter a map name without spaces!");
            return;
        }

        const files = Array.from(uploadFileInput.files);
        const fileNames = files.map(file => file.name);


        if (files.length === 0) {
            alert("Please upload a file first!");
            return;
        }
        
        let formData = new FormData();
     
        //formData.append("map_name", mapName);
        //formData.append("user_name", userName.textContent);

        const user = JSON.parse(loggedInUser);
        let user_name = user.username;


        formData.append("map_name", mapName || "default_map_name");
        formData.append("user_name", user_name || "default_user_name");

        formData.append("file", files[0]);

        //alert(formData.stringify());

        for (let [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }

        console.log("MapName : " + mapName);

        fetch('http://127.0.0.1:52091/upload', {method: "POST", body: formData});
        const session = {
            name: mapName,
            files: fileNames,
            results: {
                textSummary: { size: "65Mb", pages: 4, percentage: 80 },
                mindMap: { size: "30Mb", nodes: 23, percentage: 30 },
            },
        };

        sessions.push(session);
        addMapToSidebar(session);

        createMapHeader.style.display = "none";
        uploadBox.style.display = "none";
        mapNameForm.style.display = "none";
        processButton.style.display = "none";
        progressContainer.style.display = "block";
        progressBar.value = 0;
        progressText.textContent = "Processing... 0%";

        mapNameInput.value = "";

        let progress = 0;
        const interval = setInterval(function () {
            if (progress < 100) {
                progress += 2;
                progressBar.value = progress;
                progressText.textContent = `Processing... ${progress}%`;
            } else {
                clearInterval(interval);
                progressText.textContent = "Processing complete!";
                progressContainer.style.display = "none";
                displayResults(session);
            }
        }, 50);
    });

    // Function to add the map name to the sidebar list dynamically
    function addMapToSidebar(session) {
        const li = document.createElement("li");
        li.classList.add("map-item"); // Add a class for easier identification
        li.innerHTML = `
            <span class="color-dot dot-gray"></span> 
            <a href="#" class="map-link">${session.name}</a>
        `;
        previousMapsList.appendChild(li);

        // Add event listener to display this session's results
        li.querySelector(".map-link").addEventListener("click", function () {
            highlightActiveMap(li); // Highlight this map in the sidebar
            createMapHeader.style.display = "none";
            uploadBox.style.display = "none";
            mapNameForm.style.display = "none";
            processButton.style.display = "none";
            progressContainer.style.display = "none";
            displayResults(session);
        });

        // Automatically highlight newly created map
        highlightActiveMap(li);
    }

    // Function to highlight the active map in the sidebar
    function highlightActiveMap(activeItem) {
        // Clear any existing highlights
        clearActiveHighlight();

        // Highlight the current map
        activeItem.classList.add("highlight");
    }

    // Function to display the results after processing
    function displayResults(session) {
        // Display the map name heading
        mapNameHeading.textContent = `${session.name}`;
        mapNameHeading.style.color = "#103D4A";
        mapNameHeading.style.display = "block";

        // Clear previous results
        resultsContainer.innerHTML = '';
        resultsContainer.prepend(mapNameHeading); // Ensure heading stays on top

        // Create the uploaded files list section
        const uploadedFilesSection = document.createElement("div");
        uploadedFilesSection.classList.add("uploaded-files-info");
        const fileNames = session.files.join(', ');

        uploadedFilesSection.innerHTML = `
            <p><strong>Files used:</strong> ${fileNames || 'No files uploaded'}</p>
        `;
        resultsContainer.appendChild(uploadedFilesSection);

        // Create a container for the result boxes
        const resultsRow = document.createElement("div");
        resultsRow.classList.add("results-container-row");
        resultsContainer.appendChild(resultsRow);

        // Create the text summary div
        const textSummary = document.createElement("div");
        textSummary.classList.add("result-box");
        textSummary.innerHTML = `
            <h2>Text Summary</h2>
            <p>Document size: ${session.results.textSummary.size}</p>
            <p>Number of pages: ${session.results.textSummary.pages}</p>
            <p>% info represented: ${session.results.textSummary.percentage}%</p>
            <button onclick="openTextSummary()">Open in new tab</button>
            <button onclick="exportToPDF()">Export to .pdf</button>
        `;
        resultsRow.appendChild(textSummary);

        // Create the mind map div
        const mindMap = document.createElement("div");
        mindMap.classList.add("result-box");
        mindMap.innerHTML = `
            <h2>Mind Map</h2>
            <p>Document size: ${session.results.mindMap.size}</p>
            <p>Number of nodes: ${session.results.mindMap.nodes}</p>
            <p>% info represented: ${session.results.mindMap.percentage}%</p>
            <button onclick="openMindMap()">Open in new tab</button>
            <button onclick="exportToSVG()">Export to .svg</button>
        `;
        resultsRow.appendChild(mindMap);
    }

    // Dummy functions for export and open actions
    function openTextSummary() {
        window.open("text-summary-url", "_blank");
    }

    function exportToPDF() {
        console.log("Exporting to PDF...");
    }

    function openMindMap() {
        window.open("mind-map-url", "_blank");
    }

    function exportToSVG() {
        console.log("Exporting to SVG...");
    }


    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            fetch('http://127.0.0.1:52091/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            })
                .then(response => response.text())
                .then(text => {
                    const data = JSON.parse(text);
                    alert(data.message);
                    if (data.message === "Login successful") {
                        localStorage.setItem("loggedInUser", JSON.stringify({ username }));
                        window.location.href = "/index.html";  // Redirect to home page
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const username = document.getElementById('registerUsername').value;
            const password = document.getElementById('registerPassword').value;

            fetch('http://127.0.0.1:5000/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            })
                .then(response => response.text())
                .then(text => {
                    const data = JSON.parse(text);
                    alert(data.message);
                })
                .catch(error => console.error('Error:', error));
        });
    }

    
    // If logged in, update the profile section
    if (loggedInUser) {
        const user = JSON.parse(loggedInUser);

        userName.textContent = `Hello, ${user.username}`;
        loginRegisterLink.innerHTML = '<a href="#" id="logoutLink">Logout</a>';

        // Logout functionality
        document.getElementById('logoutLink').addEventListener('click', function (e) {
            e.preventDefault();
            localStorage.removeItem("loggedInUser");
            window.location.reload();
        });
    } else {
        userName.textContent = "No User :(";
        loginRegisterLink.innerHTML = '<a href="Login/login.html">Login</a>';
    }

});
