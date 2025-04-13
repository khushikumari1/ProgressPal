// src/hooks/useVideoTracker.js
import { useEffect, useRef, useState } from 'react';
import { fetchProgress, saveProgress } from '../api/progress';
import { mergeIntervals } from '../utils/mergeUtils';

export const useVideoTracker = ({ userId, videoId }) => {
    const videoRef = useRef(null);
    const [intervals, setIntervals] = useState([]);
    const [lastWatched, setLastWatched] = useState(0);
    const [loading, setLoading] = useState(true);

    const updateBackend = async (start, end) => {
        const newInterval = [start, end];
        const merged = mergeIntervals([...intervals, newInterval]);

        try {
            await saveProgress({
                user_id: userId,
                video_id: videoId,
                watched_intervals: merged,
                last_watched: end
            });
            setIntervals(merged);
            setLastWatched(end);
        } catch (err) {
            console.error("Progress save failed:", err);
        }
    };

    const handleTimeUpdate = () => {
        const video = videoRef.current;
        const current = video.currentTime;

        // Skip prevention: rewind if jumped ahead
        if (current - lastWatched > 12) {
            video.currentTime = lastWatched;
            return;
        }

        if (current - lastWatched >= 5) {
            updateBackend(lastWatched, current);
        }
    };

    useEffect(() => {
        const fetchAndSet = async () => {
            try {
                const data = await fetchProgress(userId, videoId);
                setIntervals(data.watched_intervals);
                setLastWatched(data.last_watched);
                if (videoRef.current) {
                    videoRef.current.currentTime = data.last_watched;
                }
            } catch {
                console.log("No prior progress. Starting fresh.");
            } finally {
                setLoading(false);
            }
        };

        fetchAndSet();
    }, [userId, videoId]);

    return { videoRef, loading, handleTimeUpdate };
};
