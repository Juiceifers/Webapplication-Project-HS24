document.addEventListener("DOMContentLoaded", function () {
    const mapNameInput = document.getElementById("mapName");
    const previousMapsList = document.getElementById("previousMapsList");
    const uploadFileInput = document.getElementById('uploadFile');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const progressContainer = document.getElementById('progress-container');
    const uploadBox = document.getElementById("uploadBox");
    const mapNameForm = document.getElementById("mapNameForm");
    const processButton = document.getElementById("processBtn");
    const createMapHeader = document.querySelector("main h2");
    const resultsContainer = document.getElementById('results-container');
    const plusButton = document.getElementById("plusButton");
    const mapNameHeading = document.createElement("h2"); // Element to display map name
    mapNameHeading.id = "mapNameHeading";
    mapNameHeading.style.display = "none"; // Hidden initially
    resultsContainer.prepend(mapNameHeading);

    // Clear previous sessions when the page is loaded
    localStorage.removeItem("sessions"); // Clear any stored sessions
    let sessions = []; // Start fresh with an empty session array

    // Function to reset to the upload form
    function resetToUploadForm() {
        createMapHeader.style.display = 'block';
        uploadBox.style.display = 'block';
        mapNameForm.style.display = 'block';
        processButton.style.display = 'block';
        resultsContainer.innerHTML = '';
        progressContainer.style.display = 'none';
    }

    // When the pink plus button is clicked
    plusButton.addEventListener("click", function () {
        resetToUploadForm();
    });

    // When the "Do the magic!" button is clicked
    processButton.addEventListener("click", function () {
        const mapName = mapNameInput.value.trim();
        if (mapName === "") {
            alert("Please enter a map name!");
            return;
        }

        // Retrieve the uploaded files
        const files = Array.from(uploadFileInput.files);
        const fileNames = files.map(file => file.name);

        if (files.length === 0) {
            alert('Please upload a file first!');
            return;
        }

        // Create a session object for this map
        const session = {
            name: mapName,
            files: fileNames, // Store the uploaded file names
            results: {
                textSummary: {
                    size: "65Mb",
                    pages: 4,
                    percentage: 80,
                },
                mindMap: {
                    size: "30Mb",
                    nodes: 23,
                    percentage: 30,
                }
            }
        };

        // Save the session
        sessions.push(session);

        // Add the map name to the sidebar
        addMapToSidebar(session);

        // Hide form and show progress bar
        createMapHeader.style.display = 'none';
        uploadBox.style.display = 'none';
        mapNameForm.style.display = 'none';
        processButton.style.display = 'none';
        progressContainer.style.display = 'block';
        progressBar.value = 0;
        progressText.textContent = "Processing... 0%";

        // Clear input
        mapNameInput.value = "";

        // Simulate progress
        let progress = 0;
        const interval = setInterval(function () {
            if (progress < 100) {
                progress += 2;
                progressBar.value = progress;
                progressText.textContent = `Processing... ${progress}%`;
            } else {
                clearInterval(interval);
                progressText.textContent = 'Processing complete!';
                progressContainer.style.display = 'none';
                displayResults(session); // Pass the session object
            }
        }, 50);
    });

    // Function to add the map name to the sidebar list dynamically
    function addMapToSidebar(session) {
        const li = document.createElement("li");
        li.innerHTML = `
            <span class="color-dot dot-gray"></span> 
            <a href="#" class="map-link">${session.name}</a>
        `;
        previousMapsList.appendChild(li);

        // Add event listener to display this session's results
        li.querySelector(".map-link").addEventListener("click", function () {
            displayResults(session);
        });
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
        const uploadedFilesSection = document.createElement('div');
        uploadedFilesSection.classList.add('uploaded-files-info');
        const fileNames = session.files.join(', ');

        uploadedFilesSection.innerHTML = `
            <p><strong>Files used:</strong> ${fileNames || 'No files uploaded'}</p>
        `;
        resultsContainer.appendChild(uploadedFilesSection);

        // Create the text summary div
        const textSummary = document.createElement('div');
        textSummary.classList.add('result-box');
        textSummary.innerHTML = `
            <h2>Text Summary</h2>
            <p>Document size: ${session.results.textSummary.size}</p>
            <p>Number of pages: ${session.results.textSummary.pages}</p>
            <p>% info represented: ${session.results.textSummary.percentage}%</p>
            <button onclick="openTextSummary()">Open in new tab</button>
            <button onclick="exportToPDF()">Export to .pdf</button>
        `;
        resultsContainer.appendChild(textSummary);

        // Create the mind map div
        const mindMap = document.createElement('div');
        mindMap.classList.add('result-box');
        mindMap.innerHTML = `
            <h2>Mind Map</h2>
            <p>Document size: ${session.results.mindMap.size}</p>
            <p>Number of nodes: ${session.results.mindMap.nodes}</p>
            <p>% info represented: ${session.results.mindMap.percentage}%</p>
            <button onclick="openMindMap()">Open in new tab</button>
            <button onclick="exportToSVG()">Export to .svg</button>
        `;
        resultsContainer.appendChild(mindMap);
    }

    // Dummy functions for export and open actions
    function openTextSummary() {
        window.open('text-summary-url', '_blank');
    }

    function exportToPDF() {
        console.log('Exporting to PDF...');
    }

    function openMindMap() {
        window.open('mind-map-url', '_blank');
    }

    function exportToSVG() {
        console.log('Exporting to SVG...');
    }
});
