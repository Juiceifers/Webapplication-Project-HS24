document.addEventListener("DOMContentLoaded", function () {
    const processBtn = document.getElementById("processBtn");
    const mapNameInput = document.getElementById("mapName");
    const previousMapsList = document.getElementById("previousMapsList");
    const uploadFileInput = document.getElementById('uploadFile');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const progressContainer = document.getElementById('progress-container');
    const uploadBox = document.getElementById("uploadBox"); // The upload box to hide
    const mapNameForm = document.getElementById("mapNameForm"); // The map name form to hide
    const processButton = document.getElementById("processBtn"); // The "Do the magic!" button
    const createMapHeader = document.querySelector("main h2"); // "Create a new map" heading

    // When the "Do the magic!" button is clicked
    processBtn.addEventListener("click", function () {
        const mapName = mapNameInput.value.trim();
        if (mapName === "") {
            alert("Please enter a map name!");
            return;
        }

        // Hide the "Create a new map" heading, map name input form, upload box, and "Do the magic!" button
        createMapHeader.style.display = 'none';  // Hide the "Create a New Map!" heading
        uploadBox.style.display = 'none';       // Hide the file upload section
        mapNameForm.style.display = 'none';     // Hide the map name input form
        processButton.style.display = 'none';   // Hide the "Do the magic!" button

        // Add the map name to the sidebar
        addMapToSidebar(mapName);

        // Show progress bar
        progressContainer.style.display = 'block';
        progressBar.value = 0;
        progressText.textContent = "Processing... 0%";

        // Clear the input field after adding it to the sidebar
        mapNameInput.value = "";

        // Store the map name for future use (in backend or local storage)
        storeMapName(mapName);

        // Upload the files (this part can be integrated with backend later)
        const files = uploadFileInput.files;
        if (files.length === 0) {
            alert('Please upload a file first!');
            return;
        }

        // Create FormData and append the files
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('file' + i, files[i]);
        }

        // Start a dummy progress update (5 seconds duration for demo)
        let progress = 0;
        const interval = setInterval(function () {
            if (progress < 100) {
                progress += 2; // Increase progress by 2% every 50ms
                progressBar.value = progress;
                progressText.textContent = `Processing... ${progress}%`;
            } else {
                clearInterval(interval); // Stop the progress after reaching 100%
                progressText.textContent = 'Processing complete!';
                // Call the function to display the results after processing
                displayResults(); // You can replace this with actual backend response later
            }
        }, 50); // Update progress every 50ms (this results in 100 updates over 5 seconds)

    });

    // Function to add the map name to the sidebar list dynamically
    function addMapToSidebar(mapName) {
        const li = document.createElement("li");
        li.innerHTML = `
            <span class="color-dot dot-gray"></span> 
            <a href="#" class="map-link">${mapName}</a>
        `;
        previousMapsList.appendChild(li);

        // Add event listener for the new map name to revisit
        li.querySelector(".map-link").addEventListener("click", function () {
            alert(`You clicked on map: ${mapName}`);
            // Handle revisiting the map result logic here (e.g., load saved map results from local storage or server)
        });
    }

    // Optional: Store the map names in LocalStorage for persistence across page refreshes
    function storeMapName(mapName) {
        let storedMaps = JSON.parse(localStorage.getItem("maps")) || [];
        storedMaps.push(mapName);
        localStorage.setItem("maps", JSON.stringify(storedMaps));
    }

    // Optional: Retrieve stored maps on page load
    document.addEventListener("DOMContentLoaded", function () {
        const storedMaps = JSON.parse(localStorage.getItem("maps")) || [];
        storedMaps.forEach(mapName => addMapToSidebar(mapName));
    });

    // Function to display the results after processing
    function displayResults() {
        const textSummary = document.createElement('div');
        textSummary.classList.add('result-box');
        textSummary.innerHTML = `
            <h2>Text Summary</h2>
            <p>Document size: 65Mb</p>
            <p>Number of pages: 4</p>
            <p>% info represented: 80%</p>
            <button onclick="openTextSummary()">Open in new tab</button>
            <button onclick="exportToPDF()">Export to .pdf</button>
        `;
        document.body.appendChild(textSummary);

        const mindMap = document.createElement('div');
        mindMap.classList.add('result-box');
        mindMap.innerHTML = `
            <h2>Mind Map</h2>
            <p>Document size: 30Mb</p>
            <p>Number of nodes: 23</p>
            <p>% info represented: 30%</p>
            <button onclick="openMindMap()">Open in new tab</button>
            <button onclick="exportToSVG()">Export to .svg</button>
        `;
        document.body.appendChild(mindMap);
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
