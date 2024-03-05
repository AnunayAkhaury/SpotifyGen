import React, { useState, useEffect } from "react";
import { useSpring, animated } from "react-spring";
import { FaSpotify } from "react-icons/fa";
import "./App.css"; // Ensure App.css is correctly imported

function App() {
  const [generatedPlaylist, setGeneratedPlaylist] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");

  const fade = useSpring({ from: { opacity: 0 }, opacity: 1 });

  const [btnAnimation, setBtnAnimation] = useSpring(() => ({
    transform: "scale(1)",
    from: { transform: "scale(1)" },
  }));

  const getQueryParams = () => {
    const queryParams = new URLSearchParams(window.location.search);
    return queryParams.get("message");
  };

  const fetchPlaylist = () => {
    setIsLoading(true);

    setBtnAnimation({ transform: "scale(1.1)" });
    window.location.href = "http://127.0.0.1:8000/spotify/check_auth";
    setTimeout(() => setBtnAnimation({ transform: "scale(1)" }), 150);
  };

  useEffect(() => {
    const msg = getQueryParams();
    if (msg) {
      setMessage(msg);
    }
  }, []);

  return (
    <animated.div style={fade} className="App">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            <FaSpotify className="logo" /> Spotify Playlist Generator
          </a>
          {}
        </div>
      </nav>

      <div className="container text-center mt-5">
        {message && <div className="alert alert-info">{message}</div>}

        <animated.button
          onClick={fetchPlaylist}
          className="btn btn-success btn-lg generate-btn"
          style={btnAnimation}
        >
          Generate Playlist
        </animated.button>

        {isLoading && (
          <div className="spinner-border text-success" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        )}

        {}
      </div>
    </animated.div>
  );
}

export default App;
