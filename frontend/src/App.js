import React, { useState, useEffect } from "react";

function App() {
  const [generatedPlaylist, setGeneratedPlaylist] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");

  const getQueryParams = () => {
    const queryParams = new URLSearchParams(window.location.search);
    return queryParams.get("message");
  };

  const fetchPlaylist = () => {
    setIsLoading(true);
    window.location.href = "http://127.0.0.1:8000/spotify/check_auth";
  };

  useEffect(() => {
    const msg = getQueryParams();
    if (msg) {
      setMessage(msg);
    }
  }, []);

  return (
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container">
          <span className="navbar-brand mb-0 h1">
            Spotify Playlist Generator
          </span>
        </div>
      </nav>

      <div className="container mt-4">
        {message && <div className="alert alert-info">{message}</div>}

        <div className="d-flex justify-content-center mb-3">
          <button onClick={fetchPlaylist} className="btn btn-success btn-lg">
            Generate Playlist
          </button>
        </div>

        {isLoading && (
          <div className="text-center">
            <div className="spinner-grow text-primary" role="status">
              <span className="sr-only">Loading...</span>
            </div>
          </div>
        )}

        {generatedPlaylist.length > 0 && (
          <div>
            <h2 className="mb-3">Generated Playlist:</h2>
            <div className="row">
              {generatedPlaylist.map((song, index) => (
                <div key={index} className="col-md-4 mb-3">
                  <div className="card">
                    <div className="card-body">
                      <h5 className="card-title">{song}</h5>
                      {/* Additional song details can go here */}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
