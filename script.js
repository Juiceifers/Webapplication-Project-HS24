document.addEventListener("DOMContentLoaded", function () {
    const processBtn = document.getElementById("processBtn");
    const mapNameInput = document.getElementById("mapName");
    const previousMapsList = document.getElementById("previousMapsList");

    // When the "Do the magic!" button is clicked
    processBtn.addEventListener("click", function () {
        const mapName = mapNameInput.value.trim();
        if (mapName === "") {
            alert("Please enter a map name!");
            return;
        }

        // Add the map name to the sidebar
        addMapToSidebar(mapName);

        // Clear the input field after adding it to the sidebar
        mapNameInput.value = "";

        // You can store this map name for future use (in backend or local storage)
        // Example: storeMapName(mapName);
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
});
