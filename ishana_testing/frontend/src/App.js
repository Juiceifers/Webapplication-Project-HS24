import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Fetch data from the Flask API
    fetch('http://172.23.66.241:52091/api/hello')
      .then(response => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then(data => {
        setData(data.message); // Assuming your API returns { message: "Hello from Flask!" }
      })
      .catch(error => {
        console.error("There was a problem with the fetch operation:", error);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Data from Flask API:</h1>
        {data ? <p>{data}</p> : <p>Loading...</p>}
      </header>
    </div>
  );
}

export default App;
