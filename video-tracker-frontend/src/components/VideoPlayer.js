import React, { useEffect, useState, useRef } from "react";
import YouTube from "react-youtube";
import axios from "axios";
import { mergeIntervals } from "../utils/mergeUtils";
import "./VideoPlayer.css";

const VideoPlayer = ({ userId, videoId, videoUrl }) => {
    const [player, setPlayer] = useState(null);
    const [intervals, setIntervals] = useState([]);
    const [watchedSeconds, setWatchedSeconds] = useState(new Set());
    const [lastWatched, setLastWatched] = useState(0);
    const [watchedPercentage, setWatchedPercentage] = useState(0);
    const [videoDuration, setVideoDuration] = useState(1);
    const intervalRef = useRef(null);
    const videoIdFromUrl = new URL(videoUrl).searchParams.get("v");

    // Load previous progress and merge intervals
    useEffect(() => {
        axios
            .get("http://localhost:8000/progress", {
                params: { user_id: userId, video_id: videoId },
            })
            .then((res) => {
                const savedIntervals = res.data.watched_intervals || [];
                const merged = mergeIntervals(savedIntervals);
                setIntervals(merged);
                setLastWatched(res.data.last_watched || 0);

                // Prepare the watchedSeconds set for accurate calculation
                const newSet = new Set();
                merged.forEach(([s, e]) => {
                    for (let i = s; i < e; i++) newSet.add(i);
                });
                setWatchedSeconds(newSet);
            })
            .catch(() => console.log("No previous progress found."));
    }, [userId, videoId]);

    // Track watched time when video is playing
    useEffect(() => {
        if (!player) return;

        const lastTrackedSecond = { current: null };

        intervalRef.current = setInterval(() => {
            if (player.getPlayerState() === 1) {
                const currentTime = Math.floor(player.getCurrentTime());

                if (currentTime !== lastTrackedSecond.current) {
                    setWatchedSeconds((prev) => {
                        const updated = new Set(prev);
                        updated.add(currentTime);
                        return updated;
                    });
                    setLastWatched((prev) => Math.max(prev, currentTime));
                    lastTrackedSecond.current = currentTime;
                }
            }
        }, 200); // 👈 200ms interval ensures accurate tracking even at 2x

        return () => clearInterval(intervalRef.current);
    }, [player]);



    // Update intervals and watched percentage
    useEffect(() => {
        const secondsArray = Array.from(watchedSeconds).sort((a, b) => a - b);
        const tempIntervals = [];
        let start = null;

        for (let i = 0; i < secondsArray.length; i++) {
            if (start === null) start = secondsArray[i];
            if (secondsArray[i + 1] !== secondsArray[i] + 1) {
                tempIntervals.push([start, secondsArray[i] + 1]);
                start = null;
            }
        }

        const merged = mergeIntervals(tempIntervals);
        setIntervals(merged);

        const total = merged.reduce((acc, [s, e]) => acc + (e - s), 0);
        const percent = videoDuration > 0 ? ((total / videoDuration) * 100).toFixed(2) : 0;
        setWatchedPercentage(percent);
    }, [watchedSeconds, videoDuration]);

    // Save progress when video is paused or ended
    const onStateChange = (event) => {
        if (event.data === 2 || event.data === 0) { // Paused or Ended
            axios.post("http://localhost:8000/progress", {
                user_id: userId,
                video_id: videoId,
                watched_intervals: Array.from(intervals),
                last_watched: lastWatched,
            });
        }
    };

    // Set player and initialize video duration
    const onPlayerReady = (event) => {
        const ytPlayer = event.target;
        setPlayer(ytPlayer);

        const duration = ytPlayer.getDuration();
        setVideoDuration(duration);

        ytPlayer.seekTo(lastWatched, true); // Resume from the last watched position
    };

    // Reset progress and start over
    const startOver = () => {
        player.seekTo(0, true);
        setWatchedSeconds(new Set());
        setIntervals([]);
        setLastWatched(0);
        setWatchedPercentage(0);
    };

    // Render the progress bar
    const renderProgressBar = () => (
        <div className="video-progress-bar">
            {intervals.map(([start, end], index) => {
                const left = (start / videoDuration) * 100;
                const width = ((end - start) / videoDuration) * 100;
                return (
                    <div
                        key={index}
                        className="watched-segment"
                        style={{
                            left: `${left}%`,
                            width: `${width}%`,
                            transition: "width 0.3s ease-in-out", // Smooth transition
                        }}
                    />
                );
            })}
        </div>
    );

    return (
        <div className="video-container">
            <YouTube
                videoId={videoIdFromUrl}
                onReady={onPlayerReady}
                onStateChange={onStateChange}
                opts={{
                    height: "390",
                    width: "640",
                    playerVars: {
                        controls: 1,
                        disablekb: 0,
                        rel: 0,
                        modestbranding: 1,
                    },
                }}
            />
            {renderProgressBar()}
            <div className="video-stats">
                <strong>Watched:</strong> {watchedPercentage}%<br />
                <strong>Resume From:</strong> Smart uncompleted spot
            </div>
            <button className="start-over-button" onClick={startOver}>
                <span role="img" aria-label="repeat">🔁</span> Start Over
            </button>
        </div>
    );
};

export default VideoPlayer;
