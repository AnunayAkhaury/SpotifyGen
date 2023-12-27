import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [generatedPlaylist, setGeneratedPlaylist] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Function to parse query parameters
  const getQueryParams = () => {
    const queryParams = new URLSearchParams(window.location.search);
    return queryParams.get('message');
  };

  // Fetch playlist function
  const fetchPlaylist = () => {
    setIsLoading(true);
    // Adjust the URL as needed
    window.location.href = 'http://127.0.0.1:8000/spotify/check_auth';
  };

  // Effect to check for messages in query parameters
  useEffect(() => {
    const msg = getQueryParams();
    if (msg) {
      setMessage(msg);
    }
  }, []);

  return (
    <div className="App">
      <header className="App-header bg-primary text-white p-4">
        <h1>Spotify Playlist Generator</h1>
      </header>
      <div className="container mt-4">
        {message && <div className="alert alert-info">{message}</div>}
        <button onClick={fetchPlaylist} className="btn btn-primary mb-3">
          Generate Playlist
        </button>
        {isLoading && <p className="text-center">Generating Playlist...</p>}
        {generatedPlaylist.length > 0 && (
          <div>
            <h2 className="mb-3">Generated Playlist:</h2>
            <ul className="list-group">
              {generatedPlaylist.map((song, index) => (
                <li key={index} className="list-group-item">
                  {song}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
