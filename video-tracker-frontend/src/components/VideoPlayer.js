import React, { useEffect, useState } from "react";
import YouTube from "react-youtube";
import axios from "axios";
import { mergeIntervals } from "../utils/mergeUtils";
import "./VideoPlayer.css";

const VideoPlayer = ({ userId, videoId, videoUrl }) => {
    const [player, setPlayer] = useState(null);
    const [intervals, setIntervals] = useState([]);
    const [startTime, setStartTime] = useState(null);
    const [lastWatched, setLastWatched] = useState(0);

    const videoIdFromUrl = new URL(videoUrl).searchParams.get("v");

    useEffect(() => {
        axios
            .get("http://localhost:8000/progress", {
                params: { user_id: userId, video_id: videoId },
            })
            .then((res) => {
                setIntervals(res.data.watched_intervals || []);
                setLastWatched(res.data.last_watched || 0);
            })
            .catch((err) => console.log("No previous progress found."));
    }, [userId, videoId]);

    const onPlayerReady = (event) => {
        setPlayer(event.target);
        event.target.seekTo(lastWatched, true);
    };

    const onStateChange = (event) => {
        if (event.data === 1) {
            setStartTime(Math.floor(player.getCurrentTime()));
        }

        if (event.data === 2 || event.data === 0) {
            if (startTime !== null) {
                const endTime = Math.floor(player.getCurrentTime());
                if (endTime - startTime >= 1) {
                    const newInterval = [startTime, endTime];
                    const updated = mergeIntervals([...intervals, newInterval]);
                    setIntervals(updated);
                    setLastWatched(Math.max(lastWatched, endTime));

                    // Save to backend
                    axios.post("http://localhost:8000/progress", {
                        user_id: userId,
                        video_id: videoId,
                        watched_intervals: [newInterval],
                        last_watched: endTime,
                    });
                }
                setStartTime(null);
            }
        }
    };

    const startOver = () => {
        player.seekTo(0, true);
        setStartTime(0);
        setLastWatched(0);
        setIntervals([]);
    };

    const videoDuration = player?.getDuration?.() || 1;

    const renderProgressBar = () => (
        <div className="video-progress-bar">
            {intervals.map(([start, end], index) => {
                const left = (start / videoDuration) * 100;
                const width = ((end - start) / videoDuration) * 100;
                return (
                    <div
                        key={index}
                        className="watched-segment"
                        style={{ left: `${left}%`, width: `${width}%` }}
                    />
                );
            })}
        </div>
    );


    return (
        <div>
            <YouTube
                videoId={videoIdFromUrl}
                onReady={onPlayerReady}
                onStateChange={onStateChange}
                opts={{
                    height: "390",
                    width: "640",
                    playerVars: {
                        controls: 1,
                        disablekb: 1,
                        rel: 0,
                    },
                }}
            />
            {renderProgressBar()}
            <button onClick={startOver} style={{ marginTop: "10px" }}>
                <span role="img" aria-label="repeat">🔁</span> Start Over
            </button>
            <div style={{ marginTop: "10px" }}>
                <strong>Watched Intervals:</strong> {JSON.stringify(intervals)}
                <br />
                <strong>Last Watched:</strong> {lastWatched}s
            </div>
        </div>
    );
};

export default VideoPlayer;
