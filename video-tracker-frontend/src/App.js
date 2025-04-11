// src/App.js
import React from "react";
import VideoPlayer from "./components/VideoPlayer";

function App() {
  return (
    <div>
      <h1>
        <span role="img" aria-label="books">📚</span> Lecture Video Tracker
      </h1>

      <VideoPlayer
        userId="khushi_001"
        videoId="yt_gaXwHThEgGk"
        videoUrl="https://www.youtube.com/watch?v=GaXwHThEgGk"
      />
    </div>
  );
}

export default App;
