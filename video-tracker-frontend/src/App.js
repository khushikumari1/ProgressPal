// src/App.js
import React, { useState } from "react";
import VideoPlayer from "./components/VideoPlayer";
import "./App.css";

function App() {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <div className={`app-container ${darkMode ? "dark-mode" : ""}`}>
      <header className="app-header">
        <h1>ProgressPal</h1>
        <p>Smart lecture video progress tracking</p>
        <button
          className="theme-toggle"
          onClick={() => setDarkMode((prev) => !prev)}
        >
          {darkMode ? "🌞 Light Mode" : "🌙 Dark Mode"}
        </button>
      </header>

      <main className="app-main">
        <VideoPlayer
          videoId="yt_gaXwHThEgGk"
          videoUrl="https://www.youtube.com/watch?v=GaXwHThEgGk"
          darkMode={darkMode}
        />
      </main>

      <footer className="app-footer">
        <p>Built by Khushi | © {new Date().getFullYear()} ProgressPal. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
